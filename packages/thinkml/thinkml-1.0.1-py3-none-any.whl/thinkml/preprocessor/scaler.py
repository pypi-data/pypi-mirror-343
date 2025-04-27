"""
Scaler module for ThinkML.

This module provides functionality for scaling numerical features and handling extreme values.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import List, Optional, Dict, Any, Union, Tuple
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, MaxAbsScaler, Normalizer
import logging
from scipy import stats
import scipy.sparse
import warnings
import psutil

# Configure logging
logger = logging.getLogger(__name__)

def scale_features(data: Union[pd.DataFrame, dd.DataFrame], columns: Optional[List[str]] = None, 
                  method: str = 'standard', chunk_size: Optional[int] = None, 
                  distributed: bool = False, **kwargs) -> Union[pd.DataFrame, dd.DataFrame]:
    """
    Scale features using various scaling methods with support for large datasets.

    Args:
        data: Input DataFrame (pandas or dask)
        columns: List of columns to scale (default: all numeric columns)
        method: Scaling method ('standard', 'minmax', 'robust', 'normalizer', 'log')
        chunk_size: Size of chunks for processing large datasets
        distributed: Whether to use Dask for distributed processing
        **kwargs: Additional arguments for specific scalers

    Returns:
        DataFrame with scaled features
    """
    if not isinstance(data, (pd.DataFrame, dd.DataFrame)):
        raise TypeError("Input must be a pandas or dask DataFrame")

    # Convert to Dask DataFrame for distributed processing
    if distributed and not isinstance(data, dd.DataFrame):
        # Estimate optimal chunk size if not provided
        if chunk_size is None:
            available_memory = psutil.virtual_memory().available
            row_size = data.memory_usage(deep=True).sum() / len(data)
            chunk_size = max(1, int(available_memory * 0.1 / row_size))
        data = dd.from_pandas(data, npartitions=max(1, len(data) // chunk_size))

    # Make a copy to avoid modifying the original data
    result = data.copy()

    # If no columns specified, use all numeric columns
    if columns is None:
        if isinstance(data, dd.DataFrame):
            columns = [col for col, dtype in data.dtypes.items() 
                      if np.issubdtype(dtype, np.number)]
        else:
            columns = result.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Validate method
    valid_methods = ['standard', 'minmax', 'robust', 'normalizer', 'log']
    if method not in valid_methods:
        raise ValueError(f"Unsupported scaling method. Must be one of {valid_methods}")

    # Handle sparse matrices
    if scipy.sparse.issparse(result):
        result = pd.DataFrame(result.toarray(), columns=result.columns)

    # Scale features
    if distributed:
        if method == 'standard':
            from dask_ml.preprocessing import StandardScaler
            scaler = StandardScaler()
        elif method == 'minmax':
            from dask_ml.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()
        elif method == 'robust':
            # Dask doesn't have RobustScaler, fallback to StandardScaler
            logger.warning("RobustScaler not available in dask-ml, using StandardScaler")
            from dask_ml.preprocessing import StandardScaler
            scaler = StandardScaler()
        elif method == 'normalizer':
            from dask_ml.preprocessing import Normalizer
            scaler = Normalizer()
        elif method == 'log':
            # Handle log transformation for distributed data
            for col in columns:
                min_val = result[col].min().compute()
                if min_val <= 0:
                    warnings.warn(f"Column {col} contains non-positive values. Using log1p transformation.")
                    result[col] = result[col].map_partitions(np.log1p)
                else:
                    result[col] = result[col].map_partitions(np.log)
            return result

        if method != 'log':
            result[columns] = scaler.fit_transform(result[columns])
    else:
        if method == 'standard':
            scaler = StandardScaler()
            result[columns] = scaler.fit_transform(result[columns])
        elif method == 'minmax':
            scaler = MinMaxScaler()
            result[columns] = scaler.fit_transform(result[columns])
        elif method == 'robust':
            scaler = RobustScaler()
            result[columns] = scaler.fit_transform(result[columns])
        elif method == 'normalizer':
            scaler = Normalizer()
            result[columns] = scaler.fit_transform(result[columns])
        elif method == 'log':
            # Check for non-positive values
            for col in columns:
                if (result[col] <= 0).any():
                    warnings.warn(f"Column {col} contains non-positive values. Using log1p transformation.")
                    result[col] = np.log1p(result[col])
                else:
                    result[col] = np.log(result[col])

    return result

def detect_outliers(data: Union[pd.DataFrame, dd.DataFrame], columns: Optional[List[str]] = None,
                   method: str = 'zscore', threshold: float = 3.0, chunk_size: Optional[int] = None,
                   distributed: bool = False, **kwargs) -> Dict[str, Any]:
    """
    Detect outliers in numerical features using various methods with support for large datasets.

    Args:
        data: Input DataFrame (pandas or dask)
        columns: List of columns to check for outliers (default: all numeric columns)
        method: Detection method ('zscore', 'iqr', 'isolation_forest', 'local_outlier_factor')
        threshold: Threshold for outlier detection (z-score or IQR multiplier)
        chunk_size: Size of chunks for processing large datasets
        distributed: Whether to use Dask for distributed processing
        **kwargs: Additional arguments for specific outlier detection methods

    Returns:
        Dictionary containing:
            - outlier_indices: Indices of detected outliers
            - outlier_scores: Outlier scores for each observation
            - summary: Summary statistics of outliers per column
    """
    if not isinstance(data, (pd.DataFrame, dd.DataFrame)):
        raise TypeError("Input must be a pandas or dask DataFrame")

    # Convert to Dask DataFrame for distributed processing if needed
    if distributed and not isinstance(data, dd.DataFrame):
        if chunk_size is None:
            available_memory = psutil.virtual_memory().available
            row_size = data.memory_usage(deep=True).sum() / len(data)
            chunk_size = max(1, int(available_memory * 0.1 / row_size))
        data = dd.from_pandas(data, npartitions=max(1, len(data) // chunk_size))

    # If no columns specified, use all numeric columns
    if columns is None:
        if isinstance(data, dd.DataFrame):
            columns = [col for col, dtype in data.dtypes.items() 
                      if np.issubdtype(dtype, np.number)]
        else:
            columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Validate method
    valid_methods = ['zscore', 'iqr', 'isolation_forest', 'local_outlier_factor']
    if method not in valid_methods:
        raise ValueError(f"Unsupported outlier detection method. Must be one of {valid_methods}")

    outlier_indices = []
    outlier_scores = pd.Series(index=data.index)
    summary = {}

    if distributed:
        if method == 'zscore':
            for col in columns:
                # Compute statistics in a distributed manner
                mean = data[col].mean().compute()
                std = data[col].std().compute()
                z_scores = data[col].map_partitions(lambda x: (x - mean) / std)
                outliers = z_scores.abs() > threshold
                outlier_indices.extend(data[outliers].index.compute().tolist())
                outlier_scores[outliers.compute()] = z_scores[outliers.compute()]
                summary[col] = {
                    'n_outliers': outliers.sum().compute(),
                    'mean': mean,
                    'std': std,
                    'threshold': threshold
                }
        
        elif method == 'iqr':
            for col in columns:
                # Compute quartiles in a distributed manner
                q1 = data[col].quantile(0.25).compute()
                q3 = data[col].quantile(0.75).compute()
                iqr = q3 - q1
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                outliers = (data[col] < lower_bound) | (data[col] > upper_bound)
                outlier_indices.extend(data[outliers].index.compute().tolist())
                outlier_scores[outliers.compute()] = data[col][outliers.compute()].map_partitions(
                    lambda x: np.minimum(np.abs(x - lower_bound), np.abs(x - upper_bound))
                )
                summary[col] = {
                    'n_outliers': outliers.sum().compute(),
                    'q1': q1,
                    'q3': q3,
                    'iqr': iqr,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        
        elif method in ['isolation_forest', 'local_outlier_factor']:
            # These methods require scikit-learn and don't have direct Dask implementations
            # We'll process in chunks using pandas
            logger.warning(f"{method} doesn't support distributed processing. Processing in chunks...")
            data_pd = data.compute() if isinstance(data, dd.DataFrame) else data
            chunk_size = min(chunk_size or 10000, len(data_pd))
            
            for i in range(0, len(data_pd), chunk_size):
                chunk = data_pd.iloc[i:i+chunk_size]
                if method == 'isolation_forest':
                    from sklearn.ensemble import IsolationForest
                    clf = IsolationForest(**kwargs)
                else:
                    from sklearn.neighbors import LocalOutlierFactor
                    clf = LocalOutlierFactor(**kwargs)
                
                scores = clf.fit_predict(chunk[columns])
                chunk_outliers = scores == -1
                outlier_indices.extend(chunk.index[chunk_outliers].tolist())
                if hasattr(clf, 'score_samples'):
                    outlier_scores[chunk.index] = -clf.score_samples(chunk[columns])
                else:
                    outlier_scores[chunk.index] = chunk_outliers.astype(float)
            
            summary['total'] = {
                'n_outliers': len(outlier_indices),
                'method': method,
                'parameters': kwargs
            }
    
    else:
        # Non-distributed processing using pandas
        if method == 'zscore':
            for col in columns:
                z_scores = stats.zscore(data[col])
                outliers = np.abs(z_scores) > threshold
                outlier_indices.extend(data.index[outliers].tolist())
                outlier_scores[outliers] = z_scores[outliers]
                summary[col] = {
                    'n_outliers': np.sum(outliers),
                    'mean': data[col].mean(),
                    'std': data[col].std(),
                    'threshold': threshold
                }
        
        elif method == 'iqr':
            for col in columns:
                q1 = data[col].quantile(0.25)
                q3 = data[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                outliers = (data[col] < lower_bound) | (data[col] > upper_bound)
                outlier_indices.extend(data.index[outliers].tolist())
                outlier_scores[outliers] = np.minimum(
                    np.abs(data[col][outliers] - lower_bound),
                    np.abs(data[col][outliers] - upper_bound)
                )
                summary[col] = {
                    'n_outliers': np.sum(outliers),
                    'q1': q1,
                    'q3': q3,
                    'iqr': iqr,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        
        elif method == 'isolation_forest':
            from sklearn.ensemble import IsolationForest
            clf = IsolationForest(**kwargs)
            scores = clf.fit_predict(data[columns])
            outliers = scores == -1
            outlier_indices = data.index[outliers].tolist()
            outlier_scores[outliers] = -clf.score_samples(data[columns])
            summary['total'] = {
                'n_outliers': np.sum(outliers),
                'method': 'isolation_forest',
                'parameters': kwargs
            }
        
        elif method == 'local_outlier_factor':
            from sklearn.neighbors import LocalOutlierFactor
            clf = LocalOutlierFactor(**kwargs)
            scores = clf.fit_predict(data[columns])
            outliers = scores == -1
            outlier_indices = data.index[outliers].tolist()
            outlier_scores[outliers] = -clf.negative_outlier_factor_
            summary['total'] = {
                'n_outliers': np.sum(outliers),
                'method': 'local_outlier_factor',
                'parameters': kwargs
            }

    return {
        'outlier_indices': outlier_indices,
        'outlier_scores': outlier_scores,
        'summary': summary
    } 
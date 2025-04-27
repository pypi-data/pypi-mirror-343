"""
Data description module for ThinkML.
This module provides functionality to analyze and describe datasets.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, Union, List
import dask.dataframe as dd
from dask.diagnostics import ProgressBar


def describe_data(
    X: pd.DataFrame,
    y: Optional[Union[pd.Series, np.ndarray]] = None,
    chunk_size: int = 100000
) -> Dict[str, Any]:
    """
    Generate a comprehensive description of the dataset including features and target variable.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame containing features.
    y : Optional[Union[pd.Series, np.ndarray]], default=None
        Target variable. Can be categorical or numerical.
    chunk_size : int, default=100000
        Number of rows to process at a time for memory efficiency.
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing dataset description with the following keys:
        - 'num_samples': Total rows in X
        - 'num_features': Total columns in X
        - 'feature_types': Data types for each column
        - 'missing_values': Total missing values
        - 'memory_usage': Memory usage in KB
        - 'duplicate_rows': Number of duplicate rows
        - 'feature_summary': Summary statistics for each feature
        - 'correlation_matrix': Correlation matrix for numerical features
        - 'target_summary': Target variable analysis (if y provided)
        - 'class_balance': Class distribution (if classification)
        - 'imbalance_status': Dataset balance status (if classification)
        
    Raises
    ------
    ValueError
        If X is not a pandas DataFrame or is empty.
        If y is provided but has different length than X.
    """
    # Input validation
    if not isinstance(X, pd.DataFrame):
        raise ValueError("X must be a pandas DataFrame")
    
    if X.empty:
        raise ValueError("Input DataFrame cannot be empty")
    
    if y is not None:
        # Convert y to pandas Series if it's not already
        if not isinstance(y, pd.Series):
            y = pd.Series(y)
        
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
    
    # Check if dataset is large enough to use Dask
    if len(X) > 1_000_000:
        return _describe_data_dask(X, y)
    
    # Process in chunks for memory efficiency
    if len(X) > chunk_size:
        return _describe_data_chunks(X, y, chunk_size)
    
    # For small datasets, process directly
    return _describe_data_direct(X, y)


def _describe_data_direct(
    X: pd.DataFrame,
    y: Optional[pd.Series] = None
) -> Dict[str, Any]:
    """
    Generate dataset description directly for small datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    y : Optional[pd.Series], default=None
        Target variable.
        
    Returns
    -------
    Dict[str, Any]
        Dataset description.
    """
    description = {}
    
    # Basic dataset information
    description['num_samples'] = len(X)
    description['num_features'] = len(X.columns)
    
    # Feature types
    description['feature_types'] = {
        col: 'numerical' if pd.api.types.is_numeric_dtype(X[col]) else 'categorical'
        for col in X.columns
    }
    
    # Missing values
    missing_values = {
        'features': X.isnull().sum().to_dict()
    }
    if y is not None:
        missing_values['target'] = y.isnull().sum()
    description['missing_values'] = missing_values
    
    # Memory usage
    description['memory_usage'] = X.memory_usage(deep=True).sum() / 1024  # KB
    
    # Duplicate rows
    description['duplicate_rows'] = X.duplicated().sum()
    
    # Feature summary
    feature_summary = {}
    for col in X.columns:
        if pd.api.types.is_numeric_dtype(X[col]):
            stats = X[col].describe()
            feature_summary[col] = {
                'type': 'numerical',
                'min': stats['min'],
                'max': stats['max'],
                'mean': stats['mean'],
                'std': stats['std'],
                'median': stats['50%']
            }
        else:
            value_counts = X[col].value_counts()
            feature_summary[col] = {
                'type': 'categorical',
                'unique_count': len(value_counts),
                'top': value_counts.index[0] if not value_counts.empty else None,
                'frequency': value_counts.iloc[0] if not value_counts.empty else 0
            }
    description['feature_summary'] = feature_summary
    
    # Correlation matrix for numerical features
    numerical_cols = [col for col in X.columns if pd.api.types.is_numeric_dtype(X[col])]
    if numerical_cols:
        description['correlation_matrix'] = X[numerical_cols].corr().to_dict()
    else:
        description['correlation_matrix'] = {}
    
    # Target variable analysis
    if y is not None:
        target_summary = {}
        
        # Determine target type
        is_categorical = (
            not pd.api.types.is_numeric_dtype(y) or
            pd.api.types.is_integer_dtype(y)
        )
        target_summary['type'] = 'categorical' if is_categorical else 'numerical'
        
        # Basic statistics
        target_summary['unique_count'] = len(y.unique())
        target_summary['distribution'] = y.value_counts().to_dict()
        
        description['target_summary'] = target_summary
        
        # Class balance analysis for classification tasks
        if is_categorical:
            class_counts = y.value_counts()
            total_samples = len(y)
            
            class_balance = {
                'counts': class_counts.to_dict(),
                'percentages': (class_counts / total_samples * 100).to_dict()
            }
            description['class_balance'] = class_balance
            
            # Determine imbalance status
            max_class_percentage = max(class_balance['percentages'].values())
            description['imbalance_status'] = (
                'imbalanced' if max_class_percentage > 60 else 'balanced'
            )
    
    return description


def _describe_data_chunks(
    X: pd.DataFrame,
    y: Optional[pd.Series],
    chunk_size: int
) -> Dict[str, Any]:
    """
    Generate dataset description in chunks for medium-sized datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    y : Optional[pd.Series]
        Target variable.
    chunk_size : int
        Number of rows to process at a time.
        
    Returns
    -------
    Dict[str, Any]
        Dataset description.
    """
    description = {}
    
    # Basic dataset information (can be computed directly)
    description['num_samples'] = len(X)
    description['num_features'] = len(X.columns)
    description['feature_types'] = {
        col: 'numerical' if pd.api.types.is_numeric_dtype(X[col]) else 'categorical'
        for col in X.columns
    }
    
    # Initialize aggregators
    missing_counts = {col: 0 for col in X.columns}
    duplicate_count = 0
    numerical_stats = {
        col: {'sum': 0, 'sum_sq': 0, 'min': float('inf'), 'max': float('-inf')}
        for col in X.columns if pd.api.types.is_numeric_dtype(X[col])
    }
    categorical_counts = {
        col: {}
        for col in X.columns if not pd.api.types.is_numeric_dtype(X[col])
    }
    
    # Process chunks
    for i in range(0, len(X), chunk_size):
        chunk_X = X.iloc[i:i+chunk_size]
        chunk_y = y.iloc[i:i+chunk_size] if y is not None else None
        
        # Missing values
        for col in X.columns:
            missing_counts[col] += chunk_X[col].isnull().sum()
        
        # Duplicate rows (within chunk)
        duplicate_count += chunk_X.duplicated().sum()
        
        # Numerical statistics
        for col in numerical_stats:
            chunk_data = chunk_X[col].dropna()
            if not chunk_data.empty:
                numerical_stats[col]['sum'] += chunk_data.sum()
                numerical_stats[col]['sum_sq'] += (chunk_data ** 2).sum()
                numerical_stats[col]['min'] = min(
                    numerical_stats[col]['min'],
                    chunk_data.min()
                )
                numerical_stats[col]['max'] = max(
                    numerical_stats[col]['max'],
                    chunk_data.max()
                )
        
        # Categorical value counts
        for col in categorical_counts:
            counts = chunk_X[col].value_counts()
            for val, count in counts.items():
                if val in categorical_counts[col]:
                    categorical_counts[col][val] += count
                else:
                    categorical_counts[col][val] = count
    
    # Compile results
    description['missing_values'] = {
        'features': missing_counts
    }
    if y is not None:
        description['missing_values']['target'] = y.isnull().sum()
    
    description['memory_usage'] = X.memory_usage(deep=True).sum() / 1024  # KB
    description['duplicate_rows'] = duplicate_count
    
    # Feature summary
    feature_summary = {}
    for col in X.columns:
        if col in numerical_stats:
            n = len(X[col].dropna())
            mean = numerical_stats[col]['sum'] / n if n > 0 else 0
            variance = (
                numerical_stats[col]['sum_sq'] / n - mean ** 2
                if n > 0 else 0
            )
            feature_summary[col] = {
                'type': 'numerical',
                'min': numerical_stats[col]['min'],
                'max': numerical_stats[col]['max'],
                'mean': mean,
                'std': np.sqrt(max(0, variance)),
                'median': X[col].median()  # Approximate
            }
        else:
            counts = categorical_counts[col]
            top_item = max(counts.items(), key=lambda x: x[1])
            feature_summary[col] = {
                'type': 'categorical',
                'unique_count': len(counts),
                'top': top_item[0],
                'frequency': top_item[1]
            }
    description['feature_summary'] = feature_summary
    
    # Correlation matrix (approximate using sample)
    numerical_cols = [col for col in X.columns if pd.api.types.is_numeric_dtype(X[col])]
    if numerical_cols:
        sample_size = min(chunk_size, len(X))
        description['correlation_matrix'] = (
            X[numerical_cols].sample(sample_size).corr().to_dict()
        )
    else:
        description['correlation_matrix'] = {}
    
    # Target variable analysis
    if y is not None:
        target_summary = {}
        is_categorical = (
            not pd.api.types.is_numeric_dtype(y) or
            pd.api.types.is_integer_dtype(y)
        )
        target_summary['type'] = 'categorical' if is_categorical else 'numerical'
        target_summary['unique_count'] = len(y.unique())
        target_summary['distribution'] = y.value_counts().to_dict()
        description['target_summary'] = target_summary
        
        if is_categorical:
            class_counts = y.value_counts()
            total_samples = len(y)
            class_balance = {
                'counts': class_counts.to_dict(),
                'percentages': (class_counts / total_samples * 100).to_dict()
            }
            description['class_balance'] = class_balance
            max_class_percentage = max(class_balance['percentages'].values())
            description['imbalance_status'] = (
                'imbalanced' if max_class_percentage > 60 else 'balanced'
            )
    
    return description


def _describe_data_dask(
    X: pd.DataFrame,
    y: Optional[pd.Series]
) -> Dict[str, Any]:
    """
    Generate dataset description using Dask for large datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    y : Optional[pd.Series]
        Target variable.
        
    Returns
    -------
    Dict[str, Any]
        Dataset description.
    """
    description = {}
    
    # Convert to Dask DataFrame/Series
    ddf_X = dd.from_pandas(X, npartitions=max(1, len(X) // 100000))
    ddf_y = dd.from_pandas(y, npartitions=max(1, len(y) // 100000)) if y is not None else None
    
    # Basic dataset information
    description['num_samples'] = len(X)
    description['num_features'] = len(X.columns)
    description['feature_types'] = {
        col: 'numerical' if pd.api.types.is_numeric_dtype(X[col]) else 'categorical'
        for col in X.columns
    }
    
    # Missing values
    with ProgressBar():
        missing_values = {
            'features': ddf_X.isnull().sum().compute().to_dict()
        }
        if ddf_y is not None:
            missing_values['target'] = ddf_y.isnull().sum().compute()
    description['missing_values'] = missing_values
    
    # Memory usage
    description['memory_usage'] = X.memory_usage(deep=True).sum() / 1024  # KB
    
    # Duplicate rows (approximate using sample)
    sample_size = min(100000, len(X))
    description['duplicate_rows'] = X.sample(sample_size).duplicated().sum()
    
    # Feature summary
    feature_summary = {}
    with ProgressBar():
        for col in X.columns:
            if pd.api.types.is_numeric_dtype(X[col]):
                stats = ddf_X[col].describe().compute()
                feature_summary[col] = {
                    'type': 'numerical',
                    'min': stats['min'],
                    'max': stats['max'],
                    'mean': stats['mean'],
                    'std': stats['std'],
                    'median': stats['50%']
                }
            else:
                value_counts = ddf_X[col].value_counts().compute()
                feature_summary[col] = {
                    'type': 'categorical',
                    'unique_count': len(value_counts),
                    'top': value_counts.index[0] if not value_counts.empty else None,
                    'frequency': value_counts.iloc[0] if not value_counts.empty else 0
                }
    description['feature_summary'] = feature_summary
    
    # Correlation matrix (approximate using sample)
    numerical_cols = [col for col in X.columns if pd.api.types.is_numeric_dtype(X[col])]
    if numerical_cols:
        sample_size = min(100000, len(X))
        description['correlation_matrix'] = (
            X[numerical_cols].sample(sample_size).corr().to_dict()
        )
    else:
        description['correlation_matrix'] = {}
    
    # Target variable analysis
    if y is not None:
        target_summary = {}
        is_categorical = (
            not pd.api.types.is_numeric_dtype(y) or
            pd.api.types.is_integer_dtype(y)
        )
        target_summary['type'] = 'categorical' if is_categorical else 'numerical'
        
        with ProgressBar():
            value_counts = ddf_y.value_counts().compute()
            target_summary['unique_count'] = len(value_counts)
            target_summary['distribution'] = value_counts.to_dict()
        
        description['target_summary'] = target_summary
        
        if is_categorical:
            total_samples = len(y)
            class_balance = {
                'counts': value_counts.to_dict(),
                'percentages': (value_counts / total_samples * 100).to_dict()
            }
            description['class_balance'] = class_balance
            max_class_percentage = max(class_balance['percentages'].values())
            description['imbalance_status'] = (
                'imbalanced' if max_class_percentage > 60 else 'balanced'
            )
    
    return description
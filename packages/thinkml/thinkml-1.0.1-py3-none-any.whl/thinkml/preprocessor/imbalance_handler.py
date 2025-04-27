"""
Imbalance handling module for ThinkML.
This module provides functionality to handle imbalanced datasets.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict, Any, Union, List
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


def handle_imbalance(
    X: pd.DataFrame, 
    y: pd.Series,
    method: str = 'smote',
    chunk_size: int = 100000,
    random_state: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Handle imbalanced datasets using various resampling methods.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame containing features.
    y : pd.Series
        Target variable (class labels).
    method : str, default='smote'
        Method to use for handling imbalance.
        Options: 'smote', 'oversample', 'undersample', 'none'.
    chunk_size : int, default=100000
        Number of rows to process at a time for memory efficiency.
    random_state : Optional[int], default=None
        Random state for reproducibility.
        
    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        Tuple containing:
        - Resampled feature DataFrame
        - Resampled target Series
        
    Raises
    ------
    ValueError
        If method is invalid, target is not categorical, or input is empty.
    """
    # Input validation
    if not isinstance(X, pd.DataFrame) or not isinstance(y, pd.Series):
        raise ValueError("X must be a pandas DataFrame and y must be a pandas Series")
    
    if X.empty or y.empty:
        raise ValueError("Input data cannot be empty")
    
    if len(X) != len(y):
        raise ValueError("X and y must have the same length")
    
    valid_methods = ['smote', 'oversample', 'undersample', 'none']
    if method not in valid_methods:
        raise ValueError(f"Method must be one of {valid_methods}")
    
    # Check if target is categorical
    if pd.api.types.is_numeric_dtype(y) and not pd.api.types.is_integer_dtype(y):
        raise ValueError("Target variable must be categorical")
    
    # If method is 'none', return original data
    if method == 'none':
        return X, y
    
    # Check if dataset is large enough to use Dask
    if len(X) > 1_000_000:
        return _handle_imbalance_dask(X, y, method, random_state)
    
    # Process in chunks for memory efficiency
    if len(X) > chunk_size:
        return _handle_imbalance_chunks(X, y, method, chunk_size, random_state)
    
    # For small datasets, process directly
    return _handle_imbalance_direct(X, y, method, random_state)


def _handle_imbalance_direct(
    X: pd.DataFrame, 
    y: pd.Series,
    method: str,
    random_state: Optional[int]
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Handle imbalanced datasets directly for small datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    y : pd.Series
        Target variable.
    method : str
        Method to use.
    random_state : Optional[int]
        Random state for reproducibility.
        
    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        Resampled data.
    """
    if method == 'smote':
        sampler = SMOTE(random_state=random_state)
    elif method == 'oversample':
        sampler = RandomOverSampler(random_state=random_state)
    else:  # undersample
        sampler = RandomUnderSampler(random_state=random_state)
    
    # Apply resampling
    X_resampled, y_resampled = sampler.fit_resample(X, y)
    
    # Convert back to pandas types
    X_resampled = pd.DataFrame(X_resampled, columns=X.columns)
    y_resampled = pd.Series(y_resampled, name=y.name)
    
    return X_resampled, y_resampled


def _handle_imbalance_chunks(
    X: pd.DataFrame, 
    y: pd.Series,
    method: str,
    chunk_size: int,
    random_state: Optional[int]
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Handle imbalanced datasets in chunks for medium-sized datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    y : pd.Series
        Target variable.
    method : str
        Method to use.
    chunk_size : int
        Number of rows to process at a time.
    random_state : Optional[int]
        Random state for reproducibility.
        
    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        Resampled data.
    """
    # For SMOTE and undersampling, we need to process the entire dataset at once
    # because these methods require access to all samples
    if method in ['smote', 'undersample']:
        return _handle_imbalance_direct(X, y, method, random_state)
    
    # For random oversampling, we can process in chunks
    result_X_chunks = []
    result_y_chunks = []
    
    # Calculate target distribution
    class_counts = y.value_counts()
    majority_class = class_counts.index[0]
    majority_count = class_counts[0]
    
    # Process each chunk
    for i in range(0, len(X), chunk_size):
        chunk_X = X.iloc[i:i+chunk_size].copy()
        chunk_y = y.iloc[i:i+chunk_size].copy()
        
        # Calculate sampling strategy for this chunk
        chunk_class_counts = chunk_y.value_counts()
        sampling_strategy = {
            cls: majority_count // len(class_counts) 
            for cls in chunk_class_counts.index
        }
        
        # Apply oversampling
        sampler = RandomOverSampler(
            sampling_strategy=sampling_strategy,
            random_state=random_state
        )
        X_resampled, y_resampled = sampler.fit_resample(chunk_X, chunk_y)
        
        result_X_chunks.append(X_resampled)
        result_y_chunks.append(y_resampled)
    
    # Combine chunks
    X_resampled = pd.concat(result_X_chunks, axis=0, ignore_index=True)
    y_resampled = pd.concat(result_y_chunks, axis=0, ignore_index=True)
    
    return X_resampled, y_resampled


def _handle_imbalance_dask(
    X: pd.DataFrame, 
    y: pd.Series,
    method: str,
    random_state: Optional[int]
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Handle imbalanced datasets using Dask for large datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    y : pd.Series
        Target variable.
    method : str
        Method to use.
    random_state : Optional[int]
        Random state for reproducibility.
        
    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        Resampled data.
    """
    # For SMOTE and undersampling, we need to process the entire dataset at once
    # because these methods require access to all samples
    if method in ['smote', 'undersample']:
        return _handle_imbalance_direct(X, y, method, random_state)
    
    # For random oversampling, we can use Dask
    # Convert to Dask DataFrame/Series
    ddf_X = dd.from_pandas(X, npartitions=max(1, len(X) // 100000))
    ddf_y = dd.from_pandas(y, npartitions=max(1, len(y) // 100000))
    
    # Calculate target distribution
    class_counts = y.value_counts()
    majority_count = class_counts.max()
    target_count = majority_count // len(class_counts)
    
    # Define a function to apply oversampling to each partition
    def oversample_partition(df_X, df_y):
        sampling_strategy = {
            cls: target_count for cls in df_y.unique()
        }
        sampler = RandomOverSampler(
            sampling_strategy=sampling_strategy,
            random_state=random_state
        )
        X_resampled, y_resampled = sampler.fit_resample(df_X, df_y)
        return pd.DataFrame(X_resampled, columns=df_X.columns), pd.Series(y_resampled)
    
    # Apply the function to each partition
    result_ddf_X = ddf_X.map_partitions(
        lambda x, y: oversample_partition(x, y)[0],
        ddf_y
    )
    result_ddf_y = ddf_y.map_partitions(
        lambda x, y: oversample_partition(x, y)[1],
        ddf_X
    )
    
    # Convert back to pandas DataFrame/Series
    with ProgressBar():
        X_resampled = result_ddf_X.compute()
        y_resampled = result_ddf_y.compute()
    
    return X_resampled, y_resampled 
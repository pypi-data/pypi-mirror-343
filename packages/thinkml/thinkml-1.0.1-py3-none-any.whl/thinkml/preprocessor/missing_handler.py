"""
Missing value handling module for ThinkML.
This module provides functionality to handle missing values in datasets.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, Dict, Any, List
import dask.dataframe as dd
from dask.diagnostics import ProgressBar


def handle_missing_values(
    X: pd.DataFrame, 
    method: str = 'mean', 
    fill_value: Optional[Union[float, str, Dict[str, Union[float, str]]]] = None,
    chunk_size: int = 100000
) -> pd.DataFrame:
    """
    Handle missing values in the dataset using various methods.

    Args:
        X (pd.DataFrame): Input DataFrame containing features with missing values.
        method (str, optional): Method to handle missing values. 
            Options: 'mean', 'median', 'mode', 'constant', 'drop'.
            Default is 'mean'.
        fill_value (Optional[Union[float, str, Dict[str, Union[float, str]]]], optional): 
            Value to use when method is 'constant'. Can be a single value or a dictionary
            mapping column names to fill values. Default is None.
        chunk_size (int, optional): Number of rows to process at a time for memory efficiency.
            Default is 100000.

    Returns:
        pd.DataFrame: DataFrame with missing values handled according to the specified method.

    Raises:
        ValueError: If method is not one of the supported options.
        ValueError: If method is 'constant' but fill_value is not provided.
        ValueError: If input DataFrame is empty.
    """
    # Input validation
    if not isinstance(X, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    if X.empty:
        raise ValueError("Empty dataset provided")
    
    valid_methods = ['mean', 'median', 'mode', 'constant', 'drop']
    if method not in valid_methods:
        raise ValueError(f"Method must be one of {valid_methods}")
    
    if method == 'constant' and fill_value is None:
        raise ValueError("fill_value must be provided when method is 'constant'")
    
    # Check if dataset is large enough to use Dask
    if len(X) > 1_000_000:
        return _handle_missing_values_dask(X, method, fill_value)
    
    # Process in chunks for memory efficiency
    if len(X) > chunk_size:
        return _handle_missing_values_chunks(X, method, fill_value, chunk_size)
    
    # For small datasets, process directly
    return _handle_missing_values_direct(X, method, fill_value)


def _handle_missing_values_direct(
    X: pd.DataFrame, 
    method: str, 
    fill_value: Optional[Union[float, str, Dict[str, Union[float, str]]]]
) -> pd.DataFrame:
    """
    Handle missing values directly for small datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    method : str
        Method to use.
    fill_value : Optional[Union[float, str, Dict[str, Union[float, str]]]]
        Value to use for 'constant' method.
        
    Returns
    -------
    pd.DataFrame
        DataFrame with missing values handled.
    """
    result = X.copy()
    
    if method == 'drop':
        return result.dropna()
    
    # For other methods, handle each column appropriately
    for col in result.columns:
        if result[col].isna().any():
            if method == 'mean' and pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].fillna(result[col].mean())
            elif method == 'median' and pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].fillna(result[col].median())
            elif method == 'mode':
                result[col] = result[col].fillna(result[col].mode().iloc[0])
            elif method == 'constant':
                if isinstance(fill_value, dict) and col in fill_value:
                    result[col] = result[col].fillna(fill_value[col])
                else:
                    result[col] = result[col].fillna(fill_value)
    
    return result


def _handle_missing_values_chunks(
    X: pd.DataFrame, 
    method: str, 
    fill_value: Optional[Union[float, str, Dict[str, Union[float, str]]]],
    chunk_size: int
) -> pd.DataFrame:
    """
    Handle missing values in chunks for medium-sized datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    method : str
        Method to use.
    fill_value : Optional[Union[float, str, Dict[str, Union[float, str]]]]
        Value to use for 'constant' method.
    chunk_size : int
        Number of rows to process at a time.
        
    Returns
    -------
    pd.DataFrame
        DataFrame with missing values handled.
    """
    # For 'drop' method, we need to process the entire dataset at once
    if method == 'drop':
        return X.dropna()
    
    # For other methods, we can process in chunks
    result_chunks = []
    
    # Calculate statistics for numeric columns if needed
    stats = {}
    if method in ['mean', 'median']:
        for col in X.columns:
            if pd.api.types.is_numeric_dtype(X[col]) and X[col].isna().any():
                if method == 'mean':
                    stats[col] = X[col].mean()
                else:  # median
                    stats[col] = X[col].median()
    
    # Process each chunk
    for i in range(0, len(X), chunk_size):
        chunk = X.iloc[i:i+chunk_size].copy()
        
        for col in chunk.columns:
            if chunk[col].isna().any():
                if method == 'mean' and pd.api.types.is_numeric_dtype(chunk[col]):
                    chunk[col] = chunk[col].fillna(stats[col])
                elif method == 'median' and pd.api.types.is_numeric_dtype(chunk[col]):
                    chunk[col] = chunk[col].fillna(stats[col])
                elif method == 'mode':
                    # For mode, we need to calculate it on the entire column
                    mode_value = X[col].mode().iloc[0]
                    chunk[col] = chunk[col].fillna(mode_value)
                elif method == 'constant':
                    if isinstance(fill_value, dict) and col in fill_value:
                        chunk[col] = chunk[col].fillna(fill_value[col])
                    else:
                        chunk[col] = chunk[col].fillna(fill_value)
        
        result_chunks.append(chunk)
    
    # Combine chunks
    return pd.concat(result_chunks, axis=0, ignore_index=True)


def _handle_missing_values_dask(
    X: pd.DataFrame, 
    method: str, 
    fill_value: Optional[Union[float, str, Dict[str, Union[float, str]]]]
) -> pd.DataFrame:
    """
    Handle missing values using Dask for large datasets.
    
    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame.
    method : str
        Method to use.
    fill_value : Optional[Union[float, str, Dict[str, Union[float, str]]]]
        Value to use for 'constant' method.
        
    Returns
    -------
    pd.DataFrame
        DataFrame with missing values handled.
    """
    # Convert to Dask DataFrame
    ddf = dd.from_pandas(X, npartitions=max(1, len(X) // 100000))
    
    if method == 'drop':
        # Drop rows with any missing values
        result_ddf = ddf.dropna()
    else:
        # For other methods, handle each column appropriately
        result_ddf = ddf.copy()
        
        # Calculate statistics for numeric columns if needed
        stats = {}
        if method in ['mean', 'median']:
            for col in X.columns:
                if pd.api.types.is_numeric_dtype(X[col]) and X[col].isna().any():
                    if method == 'mean':
                        stats[col] = X[col].mean()
                    else:  # median
                        stats[col] = X[col].median()
        
        # Apply the appropriate method to each column
        for col in result_ddf.columns:
            if method == 'mean' and pd.api.types.is_numeric_dtype(X[col]):
                result_ddf[col] = result_ddf[col].fillna(stats[col])
            elif method == 'median' and pd.api.types.is_numeric_dtype(X[col]):
                result_ddf[col] = result_ddf[col].fillna(stats[col])
            elif method == 'mode':
                # For mode, we need to calculate it on the entire column
                mode_value = X[col].mode().iloc[0]
                result_ddf[col] = result_ddf[col].fillna(mode_value)
            elif method == 'constant':
                if isinstance(fill_value, dict) and col in fill_value:
                    result_ddf[col] = result_ddf[col].fillna(fill_value[col])
                else:
                    result_ddf[col] = result_ddf[col].fillna(fill_value)
    
    # Convert back to pandas DataFrame
    with ProgressBar():
        result = result_ddf.compute()
    
    return result 
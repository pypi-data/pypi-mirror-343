"""
Missing values handler module for ThinkML.

This module provides functionality for detecting and handling missing values in datasets.
"""

import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any, Union
import logging
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
import scipy.sparse
import re
import json

# Configure logging
logger = logging.getLogger(__name__)

def clean_column_names(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names to ensure they are valid Python identifiers.
    
    Args:
        data: Input DataFrame
        
    Returns:
        DataFrame with cleaned column names
    """
    # Create a mapping of old to new column names
    name_mapping = {}
    for col in data.columns:
        # Replace special characters with underscore
        new_name = re.sub(r'[^a-zA-Z0-9_]', '_', str(col))
        # Ensure name starts with letter or underscore
        if not new_name[0].isalpha() and new_name[0] != '_':
            new_name = '_' + new_name
        # Handle duplicates
        base_name = new_name
        counter = 1
        while new_name in name_mapping.values():
            new_name = f"{base_name}_{counter}"
            counter += 1
        name_mapping[col] = new_name
    
    # Rename columns
    return data.rename(columns=name_mapping)

def flatten_nested_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten nested data structures in the DataFrame.

    Args:
        data: Input DataFrame

    Returns:
        DataFrame with flattened columns
    """
    result = data.copy()
    
    # Find columns with nested structures
    nested_columns = []
    for col in result.columns:
        if result[col].apply(lambda x: isinstance(x, (list, dict))).any():
            nested_columns.append(col)

    # Flatten nested columns
    for col in nested_columns:
        # Convert lists to string representation
        result[col] = result[col].apply(lambda x: str(x) if isinstance(x, (list, dict)) else x)

    return result

def handle_missing_values(
    data: pd.DataFrame,
    method: str = 'mean',
    columns: Optional[List[str]] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Handle missing values in the dataset.

    Args:
        data: Input DataFrame
        method: Method to handle missing values ('mean', 'median', 'mode', 'ffill', 'bfill', 'drop', 'knn')
        columns: List of columns to process (if None, process all columns)
        **kwargs: Additional arguments for specific methods

    Returns:
        DataFrame with handled missing values

    Raises:
        ValueError: If method is not supported
        TypeError: If input is not a pandas DataFrame
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Make a copy to avoid modifying the original
    result = data.copy()

    # Sanitize column names
    result.columns = [col.replace(' ', '_').replace('-', '_').replace('@', '_').replace('#', '_').replace('$', '_') for col in result.columns]

    # Flatten nested data structures
    result = flatten_nested_columns(result)

    # If no columns specified, use all columns
    if columns is None:
        columns = result.columns.tolist()

    # Handle missing values based on method
    if method == 'mean':
        for col in columns:
            if col not in result.columns:
                continue
            if pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].fillna(result[col].mean())
            else:
                logging.warning(f"Column {col} is not numeric. Using mode instead.")
                result[col] = result[col].fillna(result[col].mode().iloc[0])
    elif method == 'median':
        for col in columns:
            if col not in result.columns:
                continue
            if pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].fillna(result[col].median())
            else:
                logging.warning(f"Column {col} is not numeric. Using mode instead.")
                result[col] = result[col].fillna(result[col].mode().iloc[0])
    elif method == 'mode':
        for col in columns:
            if col not in result.columns:
                continue
            result[col] = result[col].fillna(result[col].mode().iloc[0])
    elif method == 'ffill':
        result[columns] = result[columns].fillna(method='ffill')
    elif method == 'bfill':
        result[columns] = result[columns].fillna(method='bfill')
    elif method == 'drop':
        result = result.dropna(subset=columns)
    elif method == 'knn':
        from sklearn.impute import KNNImputer
        imputer = KNNImputer(n_neighbors=kwargs.get('k', 5))
        numeric_cols = result.select_dtypes(include=['int64', 'float64']).columns
        result[numeric_cols] = imputer.fit_transform(result[numeric_cols])
    else:
        raise ValueError(f"Unsupported method: {method}")

    # Remove duplicate rows if requested
    if kwargs.get('remove_duplicates', False):
        result = result.drop_duplicates()

    # Remove duplicate columns if requested
    if kwargs.get('remove_duplicate_columns', False):
        result = result.loc[:, ~result.columns.duplicated()]

    return result

def detect_missing_patterns(
    X: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Detect patterns in missing values.
    
    Args:
        X (pd.DataFrame): Input DataFrame.
        columns (Optional[List[str]], optional): List of columns to analyze.
            If None, all columns will be analyzed. Default is None.
            
    Returns:
        Dict[str, Any]: Dictionary containing:
            - missing_counts: Number of missing values per column
            - missing_ratios: Ratio of missing values per column
            - total_missing: Total number of missing values
            - total_missing_ratio: Overall ratio of missing values
            - missing_patterns: Common patterns of missingness
            - correlation_matrix: Correlation matrix of missingness
    """
    if not isinstance(X, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    if X.empty:
        raise ValueError("Empty dataset provided")
    
    # Select columns to analyze
    if columns is None:
        columns = X.columns.tolist()
    else:
        invalid_cols = [col for col in columns if col not in X.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataset: {invalid_cols}")
    
    # Calculate basic missing value statistics
    missing_mask = X[columns].isnull()
    missing_counts = missing_mask.sum()
    missing_ratios = missing_counts / len(X)
    total_missing = missing_counts.sum()
    total_missing_ratio = total_missing / (len(X) * len(columns))
    
    # Find common patterns of missingness
    pattern_counts = missing_mask.value_counts()
    top_patterns = pattern_counts.head(10)  # Get top 10 most common patterns
    
    # Calculate correlation matrix of missingness
    correlation_matrix = missing_mask.corr()
    
    return {
        'missing_counts': missing_counts,
        'missing_ratios': missing_ratios,
        'total_missing': total_missing,
        'total_missing_ratio': total_missing_ratio,
        'missing_patterns': top_patterns,
        'correlation_matrix': correlation_matrix
    } 
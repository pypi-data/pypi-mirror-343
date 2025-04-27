"""
Encoding module for ThinkML.

This module provides functionality for encoding categorical variables.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Union
import logging
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import category_encoders as ce
import json
import networkx as nx

# Configure logging
logger = logging.getLogger(__name__)

def _convert_to_string(value: Any) -> str:
    """
    Convert a value to string while handling special types.
    
    Args:
        value: Value to convert
        
    Returns:
        String representation of the value
    """
    if pd.isna(value):
        return "NaN"
    elif isinstance(value, (list, dict)):
        return str(value)
    else:
        # Normalize unicode characters
        return str(value).encode('utf-8', errors='ignore').decode('utf-8')

def _is_mixed_type_column(series: pd.Series) -> bool:
    """
    Check if a column contains mixed data types.
    
    Args:
        series: pandas Series to check
        
    Returns:
        True if the column contains mixed types, False otherwise
    """
    # Get unique types excluding None/NaN
    types = set(type(x) for x in series.dropna().unique())
    return len(types) > 1

def detect_cyclic_features(data: pd.DataFrame) -> List[str]:
    """
    Detect cyclic features in the dataset.

    Args:
        data: Input DataFrame

    Returns:
        List of column names that are cyclic features
    """
    cyclic_columns = []
    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            # Check if values are cyclic (e.g., angles, hours, days)
            unique_vals = data[col].dropna().unique()
            if len(unique_vals) > 0:
                min_val, max_val = unique_vals.min(), unique_vals.max()
                if min_val == 0 and max_val in [23, 59, 359, 360, 365, 366]:
                    cyclic_columns.append(col)
    return cyclic_columns

def encode_categorical_variables(data: pd.DataFrame, columns: Optional[List[str]] = None, 
                               method: str = 'onehot', target_column: Optional[str] = None) -> pd.DataFrame:
    """
    Encode categorical variables using various encoding methods.

    Args:
        data: Input DataFrame
        columns: List of columns to encode (default: all categorical columns)
        method: Encoding method ('onehot', 'label', 'target', 'binary', 'frequency')
        target_column: Target column for target encoding

    Returns:
        DataFrame with encoded features
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Make a copy to avoid modifying the original data
    result = data.copy()

    # If no columns specified, use all categorical columns
    if columns is None:
        columns = result.select_dtypes(include=['object', 'category']).columns.tolist()

    # Validate method
    valid_methods = ['onehot', 'label', 'target', 'binary', 'frequency']
    if method not in valid_methods:
        raise ValueError(f"Unsupported encoding method. Must be one of {valid_methods}")

    # Check for target column if using target encoding
    if method == 'target' and target_column is None:
        raise ValueError("Target variable is required for target encoding")

    # Detect cyclic features
    cyclic_columns = detect_cyclic_features(result)
    for col in cyclic_columns:
        if col in columns:
            # Create cyclic features
            result[f"{col}_sin"] = np.sin(result[col])
            result[f"{col}_cos"] = np.cos(result[col])
            columns.remove(col)  # Remove from encoding list

    # Encode remaining columns
    for col in columns:
        if col not in result.columns:
            continue

        if method == 'onehot':
            # One-hot encoding
            encoded = pd.get_dummies(result[col], prefix=col)
            result = pd.concat([result, encoded], axis=1)
            result.drop(columns=[col], inplace=True)

        elif method == 'label':
            # Label encoding
            result[col] = LabelEncoder().fit_transform(result[col].astype(str))

        elif method == 'target':
            # Target encoding
            if target_column not in result.columns:
                raise ValueError(f"Target column '{target_column}' not found in data")
            result[col] = result.groupby(col)[target_column].transform('mean')

        elif method == 'binary':
            # Binary encoding
            result[col] = (result[col].astype('category').cat.codes > 0).astype(int)

        elif method == 'frequency':
            # Frequency encoding
            result[col] = result[col].map(result[col].value_counts(normalize=True))

    return result 
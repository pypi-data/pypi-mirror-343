import re
import pandas as pd
import numpy as np
from typing import Dict, Any

def inspect_data(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Inspect data for potential issues and provide summary statistics.

    Args:
        data: Input DataFrame

    Returns:
        Dictionary containing inspection results
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    inspection_results = {
        'shape': data.shape,
        'dtypes': data.dtypes.to_dict(),
        'missing_values': data.isnull().sum().to_dict(),
        'special_characters': {},
        'duplicate_columns': data.columns[data.columns.duplicated()].tolist(),
        'constant_columns': []
    }

    # Check for special characters in column names
    for col in data.columns:
        special_chars = re.findall(r'[^\w\s]', col)
        if special_chars:
            inspection_results['special_characters'][col] = special_chars

    # Check for constant columns
    for col in data.columns:
        if data[col].nunique() == 1:
            inspection_results['constant_columns'].append(col)

    # Add summary statistics for numeric columns
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        inspection_results['numeric_summary'] = {
            'mean': data[numeric_cols].mean().to_dict(),
            'std': data[numeric_cols].std().to_dict(),
            'min': data[numeric_cols].min().to_dict(),
            'max': data[numeric_cols].max().to_dict()
        }

    # Add value counts for categorical columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        inspection_results['categorical_summary'] = {
            col: data[col].value_counts().to_dict() for col in categorical_cols
        }

    return inspection_results 
"""
Data description functionality for ThinkML.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union
from scipy import stats

def describe_data(
    data: pd.DataFrame,
    include_correlations: bool = True,
    include_missing: bool = True,
    include_distributions: bool = True
) -> Dict[str, Any]:
    """
    Provide a comprehensive description of the dataset.

    Args:
        data: Input DataFrame
        include_correlations: Whether to include correlation analysis
        include_missing: Whether to include missing value analysis
        include_distributions: Whether to include distribution analysis

    Returns:
        Dictionary containing various descriptive statistics and analyses
    """
    description = {}

    # Basic statistics
    description['basic_stats'] = data.describe().to_dict()
    
    # Data types
    description['dtypes'] = data.dtypes.to_dict()
    
    # Shape
    description['shape'] = {
        'rows': data.shape[0],
        'columns': data.shape[1]
    }

    # Missing values analysis
    if include_missing:
        missing = data.isnull().sum()
        description['missing'] = {
            'total': missing.to_dict(),
            'percentage': (missing / len(data) * 100).to_dict()
        }

    # Correlation analysis
    if include_correlations:
        numeric_data = data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            description['correlations'] = numeric_data.corr().to_dict()

    # Distribution analysis
    if include_distributions:
        distributions = {}
        for column in data.select_dtypes(include=[np.number]).columns:
            distributions[column] = {
                'skewness': float(stats.skew(data[column].dropna())),
                'kurtosis': float(stats.kurtosis(data[column].dropna())),
                'normality_test': stats.normaltest(data[column].dropna())[1]
            }
        description['distributions'] = distributions

    return description 
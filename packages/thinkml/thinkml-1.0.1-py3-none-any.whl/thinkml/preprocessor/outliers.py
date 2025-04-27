"""
Outlier detection module for ThinkML.
"""

import numpy as np
import pandas as pd
from typing import Union, Dict, Any, List, Optional
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging
from sklearn.neighbors import LocalOutlierFactor

# Set up logging
logger = logging.getLogger(__name__)

def detect_outliers(
    data: pd.DataFrame,
    method: str = 'zscore',
    threshold: float = 3.0,
    columns: Optional[List[str]] = None
) -> Dict[str, List[int]]:
    """
    Detect outliers in the dataset using various methods.

    Args:
        data (pd.DataFrame): Input DataFrame.
        method (str): Method to detect outliers.
            Options: 'zscore', 'iqr', 'isolation_forest', 'lof'.
        threshold (float): Threshold for outlier detection.
            For zscore: number of standard deviations.
            For iqr: multiplier for IQR.
        columns (Optional[List[str]]): List of columns to check for outliers.
            If None, all numeric columns are used.

    Returns:
        Dict[str, List[int]]: Dictionary mapping column names to lists of outlier indices.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if data.empty:
        raise ValueError("Empty dataset provided")

    # Select columns to check
    if columns is None:
        columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    else:
        # Validate columns exist in dataset
        invalid_cols = [col for col in columns if col not in data.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataset: {invalid_cols}")

    if not columns:
        logger.warning("No numeric columns found for outlier detection")
        return {}

    outliers = {}
    for column in columns:
        # Skip non-numeric columns
        if not pd.api.types.is_numeric_dtype(data[column]):
            logger.warning(f"Skipping non-numeric column: {column}")
            continue

        # Get column data
        values = data[column].values.reshape(-1, 1)

        if method == 'zscore':
            # Calculate z-scores
            z_scores = np.abs((values - np.mean(values)) / np.std(values))
            outlier_indices = np.where(z_scores > threshold)[0]

        elif method == 'iqr':
            # Calculate IQR
            q1 = np.percentile(values, 25)
            q3 = np.percentile(values, 75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            outlier_indices = np.where((values < lower_bound) | (values > upper_bound))[0]

        elif method == 'isolation_forest':
            # Use Isolation Forest
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            predictions = iso_forest.fit_predict(values)
            outlier_indices = np.where(predictions == -1)[0]

        elif method == 'lof':
            # Use Local Outlier Factor
            lof = LocalOutlierFactor(contamination=0.1)
            predictions = lof.fit_predict(values)
            outlier_indices = np.where(predictions == -1)[0]

        else:
            raise ValueError(f"Unknown method: {method}")

        if len(outlier_indices) > 0:
            outliers[column] = outlier_indices.tolist()
            logger.info(f"Found {len(outlier_indices)} outliers in column '{column}'")

    return outliers

def remove_outliers(
    data: pd.DataFrame,
    outliers: Dict[str, List[int]],
    method: str = 'drop'
) -> pd.DataFrame:
    """
    Remove outliers from the dataset.

    Args:
        data (pd.DataFrame): Input DataFrame.
        outliers (Dict[str, List[int]]): Dictionary mapping column names to lists of outlier indices.
        method (str): Method to handle outliers.
            Options: 'drop', 'clip', 'mean', 'median'.

    Returns:
        pd.DataFrame: DataFrame with outliers handled according to the specified method.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if data.empty:
        raise ValueError("Empty dataset provided")

    if not outliers:
        logger.info("No outliers to remove")
        return data

    result = data.copy()

    for column, indices in outliers.items():
        if column not in result.columns:
            continue

        if method == 'drop':
            # Drop rows with outliers
            result = result.drop(index=result.index[indices])
            logger.info(f"Dropped {len(indices)} rows with outliers in column '{column}'")

        elif method == 'clip':
            # Clip outliers to min/max values
            values = result[column].values
            q1 = np.percentile(values, 25)
            q3 = np.percentile(values, 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            result[column] = result[column].clip(lower_bound, upper_bound)
            logger.info(f"Clipped outliers in column '{column}' to [{lower_bound:.2f}, {upper_bound:.2f}]")

        elif method == 'mean':
            # Replace outliers with mean
            mean_value = result[column].mean()
            result.loc[indices, column] = mean_value
            logger.info(f"Replaced {len(indices)} outliers in column '{column}' with mean value {mean_value:.2f}")

        elif method == 'median':
            # Replace outliers with median
            median_value = result[column].median()
            result.loc[indices, column] = median_value
            logger.info(f"Replaced {len(indices)} outliers in column '{column}' with median value {median_value:.2f}")

        else:
            raise ValueError(f"Unknown method: {method}")

    return result 
"""
Data splitting functionality for ThinkML.

This module provides functions for standardizing and splitting datasets
into training and testing sets with various scaling options.
"""

from typing import Union, Tuple, Optional, Literal
import pandas as pd
import numpy as np
import dask.dataframe as dd
from dask_ml.preprocessing import StandardScaler as DaskStandardScaler
from dask_ml.preprocessing import MinMaxScaler as DaskMinMaxScaler
from dask_ml.preprocessing import RobustScaler as DaskRobustScaler


def train_test_split(
    X: Union[pd.DataFrame, np.ndarray],
    y: Optional[Union[pd.Series, np.ndarray]] = None,
    test_size: float = 0.2,
    random_state: Optional[int] = None
) -> Tuple[Union[pd.DataFrame, np.ndarray], Union[pd.DataFrame, np.ndarray], 
          Optional[Union[pd.Series, np.ndarray]], Optional[Union[pd.Series, np.ndarray]]]:
    """
    Split arrays into random train and test subsets.
    
    Args:
        X: Features dataset
        y: Target variable (optional)
        test_size: Proportion of the dataset to include in the test split
        random_state: Controls the shuffling applied to the data before splitting
        
    Returns:
        Tuple containing:
        - X_train: Training features
        - X_test: Test features
        - y_train: Training target (if y is provided)
        - y_test: Test target (if y is provided)
    """
    # Set random seed if provided
    if random_state is not None:
        np.random.seed(random_state)
    
    # Get the number of samples
    n_samples = len(X)
    
    # Calculate the number of test samples
    n_test = int(n_samples * test_size)
    
    # Generate random indices
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    
    # Split indices into train and test
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    # Split the data
    if isinstance(X, pd.DataFrame):
        X_train = X.iloc[train_indices]
        X_test = X.iloc[test_indices]
    else:
        X_train = X[train_indices]
        X_test = X[test_indices]
    
    # Split the target if provided
    if y is not None:
        if isinstance(y, pd.Series):
            y_train = y.iloc[train_indices]
            y_test = y.iloc[test_indices]
        else:
            y_train = y[train_indices]
            y_test = y[test_indices]
    else:
        y_train, y_test = None, None
    
    return X_train, X_test, y_train, y_test


def standardize_and_split(
    X: Union[pd.DataFrame, dd.DataFrame],
    y: Optional[Union[pd.Series, np.ndarray, dd.Series]] = None,
    scaler: Optional[Literal['standard', 'minmax', 'robust']] = 'standard',
    test_size: float = 0.2,
    random_state: Optional[int] = None
) -> Tuple[Union[pd.DataFrame, dd.DataFrame], Union[pd.DataFrame, dd.DataFrame], 
          Optional[Union[pd.Series, np.ndarray, dd.Series]], 
          Optional[Union[pd.Series, np.ndarray, dd.Series]]]:
    """
    Split and standardize a dataset into training and testing sets.

    Args:
        X: Features dataset
        y: Target variable (optional)
        scaler: Type of scaler to use. Options are:
            - 'standard': StandardScaler (zero mean, unit variance)
            - 'minmax': MinMaxScaler (scale to range [0,1])
            - 'robust': RobustScaler (robust to outliers)
            - None: No scaling
        test_size: Proportion of the dataset to include in the test split
        random_state: Controls the shuffling applied to the data before splitting

    Returns:
        Tuple containing:
        - X_train: Training features
        - X_test: Test features
        - y_train: Training target (if y is provided)
        - y_test: Test target (if y is provided)

    Raises:
        ValueError: If scaler is not one of the supported options
    """
    # Input validation
    if scaler not in [None, 'standard', 'minmax', 'robust']:
        raise ValueError("scaler must be one of: None, 'standard', 'minmax', 'robust'")

    # Determine if we're working with Dask DataFrames
    is_dask = isinstance(X, dd.DataFrame)

    # Split the data
    if is_dask:
        X_train, X_test = X.random_split([1 - test_size, test_size], random_state=random_state)
        if y is not None:
            y_train, y_test = y.random_split([1 - test_size, test_size], random_state=random_state)
        else:
            y_train, y_test = None, None
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

    # Apply scaling if requested
    if scaler is not None:
        if is_dask:
            if scaler == 'standard':
                scaler_obj = DaskStandardScaler()
            elif scaler == 'minmax':
                scaler_obj = DaskMinMaxScaler()
            else:  # robust
                scaler_obj = DaskRobustScaler()
            
            # Fit on training data only
            scaler_obj.fit(X_train)
            
            # Transform both training and test data
            X_train = scaler_obj.transform(X_train)
            X_test = scaler_obj.transform(X_test)
        else:
            # Use our own scaler implementation
            from thinkml.preprocessor.scaler import scale_features
            
            # Scale training data
            X_train = scale_features(X_train, method=scaler)
            
            # Scale test data using the same parameters as training
            X_test = scale_features(X_test, method=scaler)
    
    return X_train, X_test, y_train, y_test 
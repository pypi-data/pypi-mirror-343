"""
Data Utilities Module for ThinkML.

This module provides functions for data preprocessing and manipulation.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from typing import Optional, Union, Dict, Any, Tuple, List

def preprocess_data(
    X: Union[np.ndarray, pd.DataFrame],
    y: Optional[Union[np.ndarray, pd.Series]] = None,
    categorical_features: Optional[List[Union[str, int]]] = None,
    numerical_features: Optional[List[Union[str, int]]] = None,
    scaling: str = 'standard',
    encoding: str = 'onehot',
    handle_missing: str = 'mean',
    handle_outliers: bool = False,
    outlier_threshold: float = 3.0
) -> Union[Tuple[np.ndarray, np.ndarray], np.ndarray]:
    """
    Preprocess data by handling missing values, encoding categorical variables,
    scaling numerical variables, and optionally handling outliers.
    
    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The input data to preprocess.
    y : array-like of shape (n_samples,), optional
        Target values.
    categorical_features : list of str or int, optional
        List of categorical feature names or indices.
    numerical_features : list of str or int, optional
        List of numerical feature names or indices.
    scaling : str, default='standard'
        The scaling method to use for numerical features.
        Options: ['standard', 'minmax', 'robust', None]
    encoding : str, default='onehot'
        The encoding method to use for categorical features.
        Options: ['onehot', 'label', None]
    handle_missing : str, default='mean'
        The method to handle missing values.
        Options: ['mean', 'median', 'most_frequent', 'constant']
    handle_outliers : bool, default=False
        Whether to handle outliers in numerical features.
    outlier_threshold : float, default=3.0
        The threshold (in standard deviations) for outlier detection.
        
    Returns
    -------
    array-like or tuple of array-like
        The preprocessed features X and optionally the preprocessed target y.
    """
    # Convert input to DataFrame if numpy array
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)
        
    # Make a copy to avoid modifying the original data
    X = X.copy()
    if y is not None:
        y = y.copy()
    
    # Identify features if not provided
    if categorical_features is None and numerical_features is None:
        categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
        numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    elif categorical_features is None:
        categorical_features = [col for col in X.columns if col not in numerical_features]
    elif numerical_features is None:
        numerical_features = [col for col in X.columns if col not in categorical_features]
    
    # Handle missing values
    if handle_missing is not None:
        # For numerical features
        if numerical_features:
            imputer = SimpleImputer(strategy=handle_missing)
            X[numerical_features] = imputer.fit_transform(X[numerical_features])
            
        # For categorical features
        if categorical_features:
            imputer = SimpleImputer(strategy='most_frequent')
            X[categorical_features] = imputer.fit_transform(X[categorical_features])
    
    # Handle outliers in numerical features
    if handle_outliers and numerical_features:
        for feature in numerical_features:
            values = X[feature].values
            z_scores = np.abs((values - np.mean(values)) / np.std(values))
            outliers = z_scores > outlier_threshold
            X.loc[outliers, feature] = np.mean(values[~outliers])
    
    # Scale numerical features
    if scaling is not None and numerical_features:
        if scaling == 'standard':
            scaler = StandardScaler()
        elif scaling == 'minmax':
            scaler = MinMaxScaler()
        elif scaling == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaling method: {scaling}")
            
        X[numerical_features] = scaler.fit_transform(X[numerical_features])
    
    # Encode categorical features
    if encoding is not None and categorical_features:
        if encoding == 'onehot':
            encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
            encoded_features = encoder.fit_transform(X[categorical_features])
            feature_names = encoder.get_feature_names_out(categorical_features)
            
            # Replace original categorical columns with encoded ones
            X = X.drop(columns=categorical_features)
            X = pd.concat([
                X,
                pd.DataFrame(
                    encoded_features,
                    columns=feature_names,
                    index=X.index
                )
            ], axis=1)
            
        elif encoding == 'label':
            for feature in categorical_features:
                encoder = LabelEncoder()
                X[feature] = encoder.fit_transform(X[feature])
        else:
            raise ValueError(f"Unknown encoding method: {encoding}")
    
    # Convert target if provided
    if y is not None:
        if isinstance(y, pd.Series):
            y = y.values
        if encoding == 'label' and y.dtype == object:
            encoder = LabelEncoder()
            y = encoder.fit_transform(y)
    
    # Convert to numpy array
    X = X.values
    
    return (X, y) if y is not None else X 
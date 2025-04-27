"""
Feature Creation Module for ThinkML.

This module provides functionality for creating and transforming features in machine learning pipelines.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PolynomialFeatures
from typing import List, Union, Dict, Any, Optional

def create_features(X: Union[pd.DataFrame, np.ndarray], 
                   feature_types: List[str] = ['polynomial', 'interaction'],
                   polynomial_degree: int = 2,
                   interaction_only: bool = False,
                   include_bias: bool = False) -> pd.DataFrame:
    """Create new features based on specified feature types.
    
    Args:
        X: Input features
        feature_types: List of feature types to create. Options:
            - 'polynomial': Polynomial features up to degree
            - 'interaction': Interaction terms between features
            - 'ratio': Ratios between numeric features
            - 'log': Log transformation of numeric features
            - 'sqrt': Square root of numeric features
            - 'exp': Exponential of numeric features
        polynomial_degree: Degree for polynomial features
        interaction_only: If True, only interaction features are produced
        include_bias: Whether to include a bias column
        
    Returns:
        DataFrame with original and new features
    """
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)
    
    result = X.copy()
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    
    for feature_type in feature_types:
        if feature_type == 'polynomial':
            poly = PolynomialFeatures(degree=polynomial_degree, 
                                    interaction_only=interaction_only,
                                    include_bias=include_bias)
            poly_features = poly.fit_transform(X[numeric_cols])
            feature_names = [f'poly_{i}' for i in range(poly_features.shape[1])]
            poly_df = pd.DataFrame(poly_features, columns=feature_names, index=X.index)
            result = pd.concat([result, poly_df], axis=1)
            
        elif feature_type == 'interaction':
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    result[f'interaction_{col1}_{col2}'] = X[col1] * X[col2]
                    
        elif feature_type == 'ratio':
            for i in range(len(numeric_cols)):
                for j in range(len(numeric_cols)):
                    if i != j:
                        col1, col2 = numeric_cols[i], numeric_cols[j]
                        result[f'ratio_{col1}_{col2}'] = X[col1] / (X[col2] + 1e-8)
                        
        elif feature_type == 'log':
            for col in numeric_cols:
                result[f'log_{col}'] = np.log1p(np.abs(X[col]))
                
        elif feature_type == 'sqrt':
            for col in numeric_cols:
                result[f'sqrt_{col}'] = np.sqrt(np.abs(X[col]))
                
        elif feature_type == 'exp':
            for col in numeric_cols:
                result[f'exp_{col}'] = np.exp(X[col])
                
    return result

def create_features_old(
    X: Union[np.ndarray, pd.DataFrame],
    feature_types: Optional[List[str]] = None,
    polynomial_degree: int = 2,
    interaction_only: bool = False,
    include_bias: bool = True
) -> Union[np.ndarray, pd.DataFrame]:
    """
    Create new features from existing data.
    
    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Training data
    feature_types : list of str, optional
        Types of features to create. Options include:
        - 'polynomial': Polynomial features
        - 'interaction': Interaction features
        - 'ratio': Ratio features
        - 'log': Log features
        - 'sqrt': Square root features
        - 'exp': Exponential features
    polynomial_degree : int, default=2
        Degree of polynomial features
    interaction_only : bool, default=False
        If True, only interaction features are produced
    include_bias : bool, default=True
        If True, include a bias column
        
    Returns
    -------
    array-like of shape (n_samples, n_new_features)
        Transformed data with new features
    """
    # Convert to DataFrame if numpy array
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    
    # Default feature types if none provided
    if feature_types is None:
        feature_types = ['polynomial']
    
    # Create a copy to avoid modifying the original data
    X_new = X.copy()
    
    # Get numeric columns
    numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
    
    # Create polynomial features
    if 'polynomial' in feature_types and len(numeric_cols) > 0:
        poly = PolynomialFeatures(
            degree=polynomial_degree,
            interaction_only=interaction_only,
            include_bias=include_bias
        )
        poly_features = poly.fit_transform(X[numeric_cols])
        
        # Create feature names
        feature_names = []
        if include_bias:
            feature_names.append('bias')
        
        for i in range(len(numeric_cols)):
            feature_names.append(numeric_cols[i])
            
            if polynomial_degree > 1:
                for d in range(2, polynomial_degree + 1):
                    feature_names.append(f"{numeric_cols[i]}^{d}")
        
        if not interaction_only:
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    feature_names.append(f"{numeric_cols[i]} * {numeric_cols[j]}")
        
        # Add polynomial features to DataFrame
        poly_df = pd.DataFrame(
            poly_features,
            columns=feature_names,
            index=X.index
        )
        X_new = pd.concat([X_new, poly_df], axis=1)
    
    # Create interaction features
    if 'interaction' in feature_types and len(numeric_cols) > 1:
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                col_name = f"{numeric_cols[i]}_{numeric_cols[j]}_interaction"
                X_new[col_name] = X[numeric_cols[i]] * X[numeric_cols[j]]
    
    # Create ratio features
    if 'ratio' in feature_types and len(numeric_cols) > 1:
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                if i != j:
                    col_name = f"{numeric_cols[i]}_{numeric_cols[j]}_ratio"
                    # Avoid division by zero
                    denominator = X[numeric_cols[j]].replace(0, np.nan)
                    X_new[col_name] = X[numeric_cols[i]] / denominator
    
    # Create log features
    if 'log' in feature_types and len(numeric_cols) > 0:
        for col in numeric_cols:
            # Only apply log to positive values
            positive_mask = X[col] > 0
            if positive_mask.any():
                col_name = f"{col}_log"
                X_new[col_name] = np.nan
                X_new.loc[positive_mask, col_name] = np.log(X.loc[positive_mask, col])
    
    # Create square root features
    if 'sqrt' in feature_types and len(numeric_cols) > 0:
        for col in numeric_cols:
            # Only apply sqrt to non-negative values
            non_neg_mask = X[col] >= 0
            if non_neg_mask.any():
                col_name = f"{col}_sqrt"
                X_new[col_name] = np.nan
                X_new.loc[non_neg_mask, col_name] = np.sqrt(X.loc[non_neg_mask, col])
    
    # Create exponential features
    if 'exp' in feature_types and len(numeric_cols) > 0:
        for col in numeric_cols:
            col_name = f"{col}_exp"
            X_new[col_name] = np.exp(X[col])
    
    # Handle categorical features
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    if categorical_cols:
        # One-hot encoding for categorical features
        X_new = pd.get_dummies(X_new, columns=categorical_cols, prefix=categorical_cols)
    
    return X_new 
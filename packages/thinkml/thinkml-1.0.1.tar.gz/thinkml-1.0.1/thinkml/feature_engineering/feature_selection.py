"""
Feature Selection Module for ThinkML.

This module provides functionality for selecting the most important features in machine learning pipelines.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectKBest, mutual_info_regression, mutual_info_classif
from sklearn.feature_selection import f_regression, f_classif, chi2
from sklearn.feature_selection import RFE, RFECV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Lasso, LassoCV
from sklearn.decomposition import PCA
from typing import List, Union, Dict, Any, Optional, Tuple

def select_features(
    X: Union[np.ndarray, pd.DataFrame],
    y: Union[np.ndarray, pd.Series],
    method: str = 'mutual_info',
    n_features: int = 10,
    task: str = 'regression',
    estimator: Optional[BaseEstimator] = None,
    cv: int = 5,
    scoring: str = 'r2',
    step: int = 1,
    min_features_to_select: int = 1
) -> Tuple[Union[np.ndarray, pd.DataFrame], List[int]]:
    """
    Select the most important features.
    
    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Training data
    y : array-like of shape (n_samples,)
        Target values
    method : str, default='mutual_info'
        Feature selection method. Options include:
        - 'mutual_info': Mutual information
        - 'f_regression': F-regression
        - 'f_classif': F-classification
        - 'chi2': Chi-squared
        - 'lasso': Lasso regularization
        - 'random_forest': Random Forest importance
        - 'rfe': Recursive Feature Elimination
        - 'rfecv': Recursive Feature Elimination with Cross-validation
        - 'pca': Principal Component Analysis
    n_features : int, default=10
        Number of features to select
    task : str, default='regression'
        Task type ('regression' or 'classification')
    estimator : estimator object, optional
        Base estimator for RFE, RFECV, or Random Forest methods
    cv : int, default=5
        Number of cross-validation folds for RFECV
    scoring : str, default='r2'
        Scoring metric for RFECV
    step : int, default=1
        Number of features to remove at each iteration for RFE and RFECV
    min_features_to_select : int, default=1
        Minimum number of features to select for RFECV
        
    Returns
    -------
    tuple
        Selected features array and indices of selected features
    """
    # Convert to DataFrame if numpy array
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    
    # Get feature names
    feature_names = X.columns.tolist()
    
    # Select features based on method
    if method == 'mutual_info':
        if task == 'regression':
            selector = SelectKBest(score_func=mutual_info_regression, k=n_features)
        else:
            selector = SelectKBest(score_func=mutual_info_classif, k=n_features)
        X_selected = selector.fit_transform(X, y)
        selected_indices = selector.get_support(indices=True)
        
    elif method == 'f_regression':
        if task == 'regression':
            selector = SelectKBest(score_func=f_regression, k=n_features)
        else:
            selector = SelectKBest(score_func=f_classif, k=n_features)
        X_selected = selector.fit_transform(X, y)
        selected_indices = selector.get_support(indices=True)
        
    elif method == 'chi2':
        if task == 'classification':
            selector = SelectKBest(score_func=chi2, k=n_features)
            X_selected = selector.fit_transform(X, y)
            selected_indices = selector.get_support(indices=True)
        else:
            raise ValueError("Chi-squared feature selection is only for classification tasks")
            
    elif method == 'lasso':
        if task == 'regression':
            lasso = LassoCV(cv=cv)
        else:
            lasso = LassoCV(cv=cv, class_weight='balanced')
        lasso.fit(X, y)
        selected_indices = np.where(np.abs(lasso.coef_) > 0)[0]
        X_selected = X.iloc[:, selected_indices]
        
    elif method == 'random_forest':
        if estimator is None:
            if task == 'regression':
                estimator = RandomForestRegressor(n_estimators=100, random_state=42)
            else:
                estimator = RandomForestClassifier(n_estimators=100, random_state=42)
        
        estimator.fit(X, y)
        importances = estimator.feature_importances_
        selected_indices = np.argsort(importances)[-n_features:]
        X_selected = X.iloc[:, selected_indices]
        
    elif method == 'rfe':
        if estimator is None:
            if task == 'regression':
                estimator = RandomForestRegressor(n_estimators=100, random_state=42)
            else:
                estimator = RandomForestClassifier(n_estimators=100, random_state=42)
        
        rfe = RFE(
            estimator=estimator,
            n_features_to_select=n_features,
            step=step
        )
        X_selected = rfe.fit_transform(X, y)
        selected_indices = np.where(rfe.support_)[0]
        
    elif method == 'rfecv':
        if estimator is None:
            if task == 'regression':
                estimator = RandomForestRegressor(n_estimators=100, random_state=42)
            else:
                estimator = RandomForestClassifier(n_estimators=100, random_state=42)
        
        rfecv = RFECV(
            estimator=estimator,
            min_features_to_select=min_features_to_select,
            step=step,
            cv=cv,
            scoring=scoring
        )
        X_selected = rfecv.fit_transform(X, y)
        selected_indices = np.where(rfecv.support_)[0]
        
    elif method == 'pca':
        pca = PCA(n_components=n_features)
        X_selected = pca.fit_transform(X)
        # For PCA, we don't have direct feature indices
        # Return the transformed data and empty indices list
        return X_selected, []
        
    else:
        raise ValueError(f"Unknown feature selection method: {method}")
    
    # Convert back to DataFrame with original feature names
    if isinstance(X_selected, np.ndarray):
        selected_feature_names = [feature_names[i] for i in selected_indices]
        X_selected = pd.DataFrame(X_selected, columns=selected_feature_names, index=X.index)
    
    return X_selected, selected_indices 
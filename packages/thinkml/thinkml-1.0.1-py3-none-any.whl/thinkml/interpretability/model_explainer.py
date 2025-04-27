"""
Model Explainer Module for ThinkML.

This module provides functionality for explaining machine learning models.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.base import BaseEstimator
from sklearn.inspection import permutation_importance
from typing import List, Union, Dict, Any, Optional, Tuple
import shap
import lime
import lime.lime_tabular

def explain_model(
    model: BaseEstimator,
    X: Union[np.ndarray, pd.DataFrame],
    method: str = 'shap',
    n_samples: int = 100,
    feature_names: Optional[List[str]] = None,
    class_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Explain model predictions using various interpretability techniques.
    
    Parameters
    ----------
    model : estimator object
        The trained model to explain
    X : array-like of shape (n_samples, n_features)
        Training data
    method : str, default='shap'
        Explanation method. Options include:
        - 'shap': SHAP values
        - 'lime': LIME explanations
        - 'permutation': Permutation importance
    n_samples : int, default=100
        Number of samples to use for explanation
    feature_names : list of str, optional
        Names of features
    class_names : list of str, optional
        Names of classes for classification tasks
        
    Returns
    -------
    dict
        Dictionary containing explanation results
    """
    # Convert to DataFrame if numpy array
    if isinstance(X, np.ndarray):
        if feature_names is None:
            feature_names = [f'feature_{i}' for i in range(X.shape[1])]
        X = pd.DataFrame(X, columns=feature_names)
    
    # Limit samples if needed
    if n_samples < len(X):
        X_sample = X.sample(n_samples, random_state=42)
    else:
        X_sample = X
    
    # Get feature names
    if feature_names is None:
        feature_names = X.columns.tolist()
    
    # Explain model based on method
    if method == 'shap':
        return _explain_with_shap(model, X_sample, feature_names, class_names)
    elif method == 'lime':
        return _explain_with_lime(model, X_sample, feature_names, class_names)
    elif method == 'permutation':
        return _explain_with_permutation(model, X_sample, feature_names)
    else:
        raise ValueError(f"Unknown explanation method: {method}")

def _explain_with_shap(
    model: BaseEstimator,
    X: pd.DataFrame,
    feature_names: List[str],
    class_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Explain model using SHAP values.
    
    Parameters
    ----------
    model : estimator object
        The trained model
    X : DataFrame of shape (n_samples, n_features)
        Training data
    feature_names : list of str
        Names of features
    class_names : list of str, optional
        Names of classes for classification tasks
        
    Returns
    -------
    dict
        Dictionary containing SHAP values and explanations
    """
    # Create SHAP explainer
    if hasattr(model, 'predict_proba'):
        # For models with predict_proba method (classification)
        explainer = shap.KernelExplainer(model.predict_proba, X)
        shap_values = explainer.shap_values(X)
        
        # For multi-class models, shap_values is a list
        if isinstance(shap_values, list):
            shap_values_dict = {f'class_{i}': values for i, values in enumerate(shap_values)}
        else:
            shap_values_dict = {'class_0': shap_values}
    else:
        # For models without predict_proba method (regression)
        explainer = shap.KernelExplainer(model.predict, X)
        shap_values = explainer.shap_values(X)
        shap_values_dict = {'regression': shap_values}
    
    # Create summary plot
    plt.figure(figsize=(10, 6))
    if isinstance(shap_values, list):
        shap.summary_plot(shap_values, X, feature_names=feature_names, class_names=class_names)
    else:
        shap.summary_plot(shap_values, X, feature_names=feature_names)
    plt.tight_layout()
    
    # Create dependence plots for top features
    if not isinstance(shap_values, list):
        # Get feature importance
        feature_importance = np.abs(shap_values).mean(0)
        top_features = np.argsort(feature_importance)[-3:]  # Top 3 features
        
        dependence_plots = {}
        for i in top_features:
            plt.figure(figsize=(8, 6))
            shap.dependence_plot(i, shap_values, X, feature_names=feature_names)
            plt.tight_layout()
            dependence_plots[feature_names[i]] = plt.gcf()
    else:
        dependence_plots = {}
    
    return {
        'shap_values': shap_values_dict,
        'explainer': explainer,
        'summary_plot': plt.gcf(),
        'dependence_plots': dependence_plots
    }

def _explain_with_lime(
    model: BaseEstimator,
    X: pd.DataFrame,
    feature_names: List[str],
    class_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Explain model using LIME.
    
    Parameters
    ----------
    model : estimator object
        The trained model
    X : DataFrame of shape (n_samples, n_features)
        Training data
    feature_names : list of str
        Names of features
    class_names : list of str, optional
        Names of classes for classification tasks
        
    Returns
    -------
    dict
        Dictionary containing LIME explanations
    """
    # Determine if classification or regression
    is_classification = hasattr(model, 'predict_proba')
    
    # Create LIME explainer
    explainer = lime.lime_tabular.LimeTabularExplainer(
        X.values,
        feature_names=feature_names,
        class_names=class_names if is_classification else None,
        mode='classification' if is_classification else 'regression'
    )
    
    # Explain a few instances
    explanations = {}
    for i in range(min(3, len(X))):
        exp = explainer.explain_instance(
            X.iloc[i].values,
            model.predict_proba if is_classification else model.predict,
            num_features=len(feature_names)
        )
        explanations[i] = exp
    
    return {
        'explainer': explainer,
        'explanations': explanations
    }

def _explain_with_permutation(
    model: BaseEstimator,
    X: pd.DataFrame,
    feature_names: List[str]
) -> Dict[str, Any]:
    """
    Explain model using permutation importance.
    
    Parameters
    ----------
    model : estimator object
        The trained model
    X : DataFrame of shape (n_samples, n_features)
        Training data
    feature_names : list of str
        Names of features
        
    Returns
    -------
    dict
        Dictionary containing permutation importance results
    """
    # Calculate permutation importance
    result = permutation_importance(
        model, X, model.predict(X),
        n_repeats=10, random_state=42
    )
    
    # Create feature importance plot
    plt.figure(figsize=(10, 6))
    importances = result.importances_mean
    indices = np.argsort(importances)[::-1]
    
    plt.title("Feature Permutation Importance")
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
    plt.tight_layout()
    
    return {
        'importances': importances,
        'importances_std': result.importances_std,
        'importances_permutations': result.importances_permutations,
        'plot': plt.gcf()
    }

def get_feature_importance(
    model: BaseEstimator,
    X: Union[np.ndarray, pd.DataFrame],
    method: str = 'builtin',
    feature_names: Optional[List[str]] = None,
    n_repeats: int = 10,
    random_state: int = 42
) -> Tuple[np.ndarray, List[str]]:
    """
    Get feature importance from a trained model.
    
    Parameters
    ----------
    model : estimator object
        The trained model
    X : array-like of shape (n_samples, n_features)
        Training data
    method : str, default='builtin'
        Method to use for feature importance. Options include:
        - 'builtin': Use model's built-in feature_importances_ attribute
        - 'permutation': Use permutation importance
        - 'shap': Use SHAP values
    feature_names : list of str, optional
        Names of features
    n_repeats : int, default=10
        Number of times to permute each feature for permutation importance
    random_state : int, default=42
        Random state for reproducibility
        
    Returns
    -------
    tuple
        Feature importance values and feature names
    """
    # Convert to DataFrame if numpy array
    if isinstance(X, np.ndarray):
        if feature_names is None:
            feature_names = [f'feature_{i}' for i in range(X.shape[1])]
        X = pd.DataFrame(X, columns=feature_names)
    
    # Get feature names
    if feature_names is None:
        feature_names = X.columns.tolist()
    
    # Get feature importance based on method
    if method == 'builtin':
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_).flatten()
        else:
            raise ValueError("Model does not have feature_importances_ or coef_ attribute")
            
    elif method == 'permutation':
        result = permutation_importance(
            model, X, model.predict(X),
            n_repeats=n_repeats, random_state=random_state
        )
        importances = result.importances_mean
        
    elif method == 'shap':
        # Create SHAP explainer
        if hasattr(model, 'predict_proba'):
            explainer = shap.KernelExplainer(model.predict_proba, X)
            shap_values = explainer.shap_values(X)
            
            # For multi-class models, shap_values is a list
            if isinstance(shap_values, list):
                # Use mean absolute SHAP values across all classes
                importances = np.mean([np.abs(values).mean(0) for values in shap_values], axis=0)
            else:
                importances = np.abs(shap_values).mean(0)
        else:
            explainer = shap.KernelExplainer(model.predict, X)
            shap_values = explainer.shap_values(X)
            importances = np.abs(shap_values).mean(0)
            
    else:
        raise ValueError(f"Unknown feature importance method: {method}")
    
    return importances, feature_names 
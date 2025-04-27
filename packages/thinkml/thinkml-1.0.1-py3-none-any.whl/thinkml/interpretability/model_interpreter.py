"""
Model Interpreter Module for ThinkML.

This module provides functionality for interpreting machine learning models.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Union, Dict, Any, Optional
from sklearn.base import BaseEstimator
import shap
from lime import lime_tabular

class ModelInterpreter:
    """
    A class for interpreting machine learning models.
    
    This class provides methods for:
    - SHAP value analysis
    - LIME explanations
    - Feature importance visualization
    - Model decision path analysis
    """
    
    def __init__(self):
        """Initialize the ModelInterpreter."""
        self.shap_values = None
        self.feature_importance = None
        self.explainer = None
        
    def explain_model(self, 
                     model: BaseEstimator,
                     X: Union[np.ndarray, pd.DataFrame],
                     method: str = 'shap') -> Dict[str, Any]:
        """
        Explain the model's predictions.
        
        Parameters
        ----------
        model : BaseEstimator
            The trained model
        X : array-like of shape (n_samples, n_features)
            Training data
        method : str, default='shap'
            Explanation method ('shap' or 'lime')
            
        Returns
        -------
        dict
            Dictionary containing explanation results
        """
        if method == 'shap':
            return self._explain_with_shap(model, X)
        elif method == 'lime':
            return self._explain_with_lime(model, X)
        else:
            raise ValueError(f"Unknown explanation method: {method}")
    
    def _explain_with_shap(self, 
                          model: BaseEstimator,
                          X: Union[np.ndarray, pd.DataFrame]) -> Dict[str, Any]:
        """
        Explain model using SHAP values.
        
        Parameters
        ----------
        model : BaseEstimator
            The trained model
        X : array-like of shape (n_samples, n_features)
            Training data
            
        Returns
        -------
        dict
            Dictionary containing SHAP values and explanations
        """
        # Create SHAP explainer
        if isinstance(X, pd.DataFrame):
            feature_names = X.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
            
        self.explainer = shap.KernelExplainer(model.predict, X)
        self.shap_values = self.explainer.shap_values(X)
        
        return {
            'shap_values': self.shap_values,
            'feature_names': feature_names,
            'explainer': self.explainer
        }
    
    def _explain_with_lime(self, 
                          model: BaseEstimator,
                          X: Union[np.ndarray, pd.DataFrame]) -> Dict[str, Any]:
        """
        Explain model using LIME.
        
        Parameters
        ----------
        model : BaseEstimator
            The trained model
        X : array-like of shape (n_samples, n_features)
            Training data
            
        Returns
        -------
        dict
            Dictionary containing LIME explanations
        """
        if isinstance(X, pd.DataFrame):
            feature_names = X.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
            
        explainer = lime_tabular.LimeTabularExplainer(
            X,
            feature_names=feature_names,
            class_names=['class_0', 'class_1'] if hasattr(model, 'classes_') else None,
            mode='classification' if hasattr(model, 'classes_') else 'regression'
        )
        
        return {
            'explainer': explainer,
            'feature_names': feature_names
        }
    
    def plot_feature_importance(self, 
                              model: BaseEstimator,
                              X: Union[np.ndarray, pd.DataFrame],
                              top_n: int = 10) -> None:
        """
        Plot feature importance.
        
        Parameters
        ----------
        model : BaseEstimator
            The trained model
        X : array-like of shape (n_samples, n_features)
            Training data
        top_n : int, default=10
            Number of top features to plot
        """
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_)
        else:
            raise ValueError("Model does not support feature importance")
            
        if isinstance(X, pd.DataFrame):
            feature_names = X.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
            
        # Sort features by importance
        indices = np.argsort(importance)[::-1][:top_n]
        plt.figure(figsize=(10, 6))
        plt.title("Feature Importance")
        plt.bar(range(top_n), importance[indices])
        plt.xticks(range(top_n), [feature_names[i] for i in indices], rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_shap_summary(self, 
                         model: BaseEstimator,
                         X: Union[np.ndarray, pd.DataFrame],
                         top_n: int = 10) -> None:
        """
        Plot SHAP summary.
        
        Parameters
        ----------
        model : BaseEstimator
            The trained model
        X : array-like of shape (n_samples, n_features)
            Training data
        top_n : int, default=10
            Number of top features to plot
        """
        if self.shap_values is None:
            self._explain_with_shap(model, X)
            
        shap.summary_plot(
            self.shap_values,
            X,
            feature_names=X.columns.tolist() if isinstance(X, pd.DataFrame) else None,
            max_display=top_n
        )
        plt.tight_layout()
        plt.show()
    
    def plot_lime_explanation(self, 
                            model: BaseEstimator,
                            X: Union[np.ndarray, pd.DataFrame],
                            instance_idx: int = 0,
                            num_features: int = 10) -> None:
        """
        Plot LIME explanation for a specific instance.
        
        Parameters
        ----------
        model : BaseEstimator
            The trained model
        X : array-like of shape (n_samples, n_features)
            Training data
        instance_idx : int, default=0
            Index of the instance to explain
        num_features : int, default=10
            Number of features to show in the explanation
        """
        if isinstance(X, pd.DataFrame):
            feature_names = X.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
            
        explainer = lime_tabular.LimeTabularExplainer(
            X,
            feature_names=feature_names,
            class_names=['class_0', 'class_1'] if hasattr(model, 'classes_') else None,
            mode='classification' if hasattr(model, 'classes_') else 'regression'
        )
        
        exp = explainer.explain_instance(
            X[instance_idx],
            model.predict,
            num_features=num_features
        )
        
        exp.show_in_notebook() 
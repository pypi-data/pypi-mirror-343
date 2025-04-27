"""
Advanced Regression Module for ThinkML.

This module provides advanced regression functionality including:
- Linear regression with regularization
- Polynomial regression
- Support vector regression
- Neural network regression
- Ensemble regression methods
- Quantile regression
"""

import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any, Optional
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, HuberRegressor, QuantileRegressor as SkQuantileRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import torch
import torch.nn as nn
from scipy.optimize import minimize
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

class QuantileRegressor(BaseEstimator, RegressorMixin):
    """
    Quantile Regression estimator.
    
    This class implements quantile regression, which estimates the conditional quantiles
    of the target variable. It's useful when you want to predict a specific quantile
    of the target distribution rather than just the mean.
    
    Parameters
    ----------
    quantile : float, default=0.5
        The quantile to estimate, must be between 0 and 1.
    solver : str, default='highs'
        The solver to use in the optimization, options: ['highs', 'highs-ds', 'highs-ipm'].
    alpha : float, default=0.0
        L1 regularization parameter.
    fit_intercept : bool, default=True
        Whether to calculate the intercept for this model.
    """
    
    def __init__(
        self,
        quantile: float = 0.5,
        solver: str = 'highs',
        alpha: float = 0.0,
        fit_intercept: bool = True
    ):
        self.quantile = quantile
        self.solver = solver
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'QuantileRegressor':
        """
        Fit the quantile regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
            
        Returns
        -------
        self : object
            Returns self.
        """
        # Input validation
        X, y = check_X_y(X, y)
        
        # Initialize and fit the underlying sklearn quantile regressor
        self.model_ = SkQuantileRegressor(
            quantile=self.quantile,
            solver=self.solver,
            alpha=self.alpha,
            fit_intercept=self.fit_intercept
        )
        
        self.model_.fit(X, y)
        
        # Store training data characteristics
        self.n_features_in_ = X.shape[1]
        
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict using the quantile regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        y : array-like of shape (n_samples,)
            Returns predicted values.
        """
        check_is_fitted(self)
        X = check_array(X)
        
        return self.model_.predict(X)
        
    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """Get parameters for this estimator."""
        return {
            'quantile': self.quantile,
            'solver': self.solver,
            'alpha': self.alpha,
            'fit_intercept': self.fit_intercept
        }
        
    def set_params(self, **parameters: Any) -> 'QuantileRegressor':
        """Set the parameters of this estimator."""
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

class RobustRegressor(BaseEstimator, RegressorMixin):
    """
    Robust Regression estimator.
    
    This class implements robust regression using Huber loss, which combines the best
    properties of squared-error loss and absolute-error loss. It's less sensitive to
    outliers than ordinary least squares regression.
    
    Parameters
    ----------
    epsilon : float, default=1.35
        The parameter epsilon controls the number of samples that should be classified
        as outliers. The default value is 1.35 which ensures 95% statistical efficiency
        for normally distributed data.
    max_iter : int, default=100
        Maximum number of iterations that solver should run.
    alpha : float, default=0.0001
        Regularization parameter.
    warm_start : bool, default=False
        This is useful if the stored attributes of a previously used model
        has to be reused.
    fit_intercept : bool, default=True
        Whether to calculate the intercept for this model.
    """
    
    def __init__(
        self,
        epsilon: float = 1.35,
        max_iter: int = 100,
        alpha: float = 0.0001,
        warm_start: bool = False,
        fit_intercept: bool = True
    ):
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.alpha = alpha
        self.warm_start = warm_start
        self.fit_intercept = fit_intercept
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RobustRegressor':
        """
        Fit the robust regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
            
        Returns
        -------
        self : object
            Returns self.
        """
        # Input validation
        X, y = check_X_y(X, y)
        
        # Initialize and fit the underlying sklearn Huber regressor
        self.model_ = HuberRegressor(
            epsilon=self.epsilon,
            max_iter=self.max_iter,
            alpha=self.alpha,
            warm_start=self.warm_start,
            fit_intercept=self.fit_intercept
        )
        
        self.model_.fit(X, y)
        
        # Store training data characteristics
        self.n_features_in_ = X.shape[1]
        
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict using the robust regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        y : array-like of shape (n_samples,)
            Returns predicted values.
        """
        check_is_fitted(self)
        X = check_array(X)
        
        return self.model_.predict(X)
        
    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """Get parameters for this estimator."""
        return {
            'epsilon': self.epsilon,
            'max_iter': self.max_iter,
            'alpha': self.alpha,
            'warm_start': self.warm_start,
            'fit_intercept': self.fit_intercept
        }
        
    def set_params(self, **parameters: Any) -> 'RobustRegressor':
        """Set the parameters of this estimator."""
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

class CensoredRegressor(BaseEstimator, RegressorMixin):
    """Censored regression model for handling censored data."""
    
    def __init__(self, censoring_type='right', base_estimator=None):
        """
        Initialize censored regression model.
        
        Parameters:
        -----------
        censoring_type : str, default='right'
            Type of censoring: 'right', 'left', or 'interval'
        base_estimator : estimator object, default=None
            Base estimator to use for prediction
        """
        self.censoring_type = censoring_type
        self.base_estimator = base_estimator if base_estimator is not None else LinearRegression()
        self.censoring_threshold = None
        
    def fit(self, X, y, censoring_mask=None):
        """
        Fit the censored regression model.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        censoring_mask : array-like of shape (n_samples,), default=None
            Boolean mask indicating censored samples
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        if censoring_mask is None:
            # If no mask provided, assume right censoring at max value
            self.censoring_threshold = np.max(y)
            censoring_mask = y >= self.censoring_threshold
        
        # Fit base estimator on non-censored data
        self.base_estimator.fit(X[~censoring_mask], y[~censoring_mask])
        
        return self
        
    def predict(self, X):
        """
        Predict using the censored regression model.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Samples
        """
        X = np.asarray(X)
        predictions = self.base_estimator.predict(X)
        
        if self.censoring_type == 'right':
            predictions = np.minimum(predictions, self.censoring_threshold)
        elif self.censoring_type == 'left':
            predictions = np.maximum(predictions, self.censoring_threshold)
            
        return predictions

class AdvancedRegression:
    """
    A class for advanced regression techniques.
    
    This class provides methods for:
    - Linear regression with various regularization techniques
    - Polynomial regression
    - Support vector regression
    - Neural network regression
    - Ensemble regression methods
    """
    
    def __init__(self):
        """Initialize the AdvancedRegression class."""
        self.models = {}
        self.best_model = None
        self.best_score = float('-inf')
        
    def create_linear_model(self, 
                          regularization: str = 'none',
                          alpha: float = 1.0,
                          l1_ratio: float = 0.5) -> BaseEstimator:
        """
        Create a linear regression model with optional regularization.
        
        Parameters
        ----------
        regularization : str, default='none'
            Type of regularization ('none', 'ridge', 'lasso', 'elasticnet')
        alpha : float, default=1.0
            Regularization strength
        l1_ratio : float, default=0.5
            ElasticNet mixing parameter (0 <= l1_ratio <= 1)
            
        Returns
        -------
        BaseEstimator
            The configured linear regression model
        """
        if regularization == 'none':
            return LinearRegression()
        elif regularization == 'ridge':
            return Ridge(alpha=alpha)
        elif regularization == 'lasso':
            return Lasso(alpha=alpha)
        elif regularization == 'elasticnet':
            return ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        else:
            raise ValueError(f"Unknown regularization type: {regularization}")
    
    def create_polynomial_model(self, 
                              degree: int = 2,
                              regularization: str = 'none',
                              alpha: float = 1.0) -> Pipeline:
        """
        Create a polynomial regression model.
        
        Parameters
        ----------
        degree : int, default=2
            Polynomial degree
        regularization : str, default='none'
            Type of regularization
        alpha : float, default=1.0
            Regularization strength
            
        Returns
        -------
        Pipeline
            The configured polynomial regression pipeline
        """
        poly = PolynomialFeatures(degree=degree)
        model = self.create_linear_model(regularization=regularization, alpha=alpha)
        return Pipeline([('poly', poly), ('model', model)])
    
    def create_svr_model(self, 
                        kernel: str = 'rbf',
                        C: float = 1.0,
                        epsilon: float = 0.1) -> SVR:
        """
        Create a support vector regression model.
        
        Parameters
        ----------
        kernel : str, default='rbf'
            Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
        C : float, default=1.0
            Regularization parameter
        epsilon : float, default=0.1
            Epsilon in the epsilon-SVR model
            
        Returns
        -------
        SVR
            The configured SVR model
        """
        return SVR(kernel=kernel, C=C, epsilon=epsilon)
    
    def create_neural_network(self, 
                            input_size: int,
                            hidden_sizes: List[int] = [64, 32],
                            output_size: int = 1) -> nn.Module:
        """
        Create a neural network for regression.
        
        Parameters
        ----------
        input_size : int
            Number of input features
        hidden_sizes : List[int], default=[64, 32]
            List of hidden layer sizes
        output_size : int, default=1
            Number of output units
            
        Returns
        -------
        nn.Module
            The configured neural network
        """
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_size),
                nn.Dropout(0.2)
            ])
            prev_size = hidden_size
            
        layers.append(nn.Linear(prev_size, output_size))
        
        return nn.Sequential(*layers)
    
    def create_ensemble_model(self, 
                            method: str = 'random_forest',
                            n_estimators: int = 100,
                            **kwargs) -> BaseEstimator:
        """
        Create an ensemble regression model.
        
        Parameters
        ----------
        method : str, default='random_forest'
            Ensemble method ('random_forest' or 'gradient_boosting')
        n_estimators : int, default=100
            Number of estimators
        **kwargs : dict
            Additional parameters for the ensemble model
            
        Returns
        -------
        BaseEstimator
            The configured ensemble model
        """
        if method == 'random_forest':
            return RandomForestRegressor(n_estimators=n_estimators, **kwargs)
        elif method == 'gradient_boosting':
            return GradientBoostingRegressor(n_estimators=n_estimators, **kwargs)
        else:
            raise ValueError(f"Unknown ensemble method: {method}")
    
    def evaluate_model(self, 
                      model: BaseEstimator,
                      X: Union[np.ndarray, pd.DataFrame],
                      y: Union[np.ndarray, pd.Series],
                      cv: int = 5) -> Dict[str, float]:
        """
        Evaluate a regression model using cross-validation.
        
        Parameters
        ----------
        model : BaseEstimator
            The model to evaluate
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        cv : int, default=5
            Number of cross-validation folds
            
        Returns
        -------
        dict
            Dictionary containing evaluation metrics
        """
        scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_squared_error')
        mse = -scores.mean()
        rmse = np.sqrt(mse)
        
        return {
            'mse': mse,
            'rmse': rmse,
            'cv_scores': scores
        }
    
    def find_best_model(self, 
                       X: Union[np.ndarray, pd.DataFrame],
                       y: Union[np.ndarray, pd.Series],
                       models: Dict[str, BaseEstimator]) -> Dict[str, Any]:
        """
        Find the best performing model from a set of models.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        models : dict
            Dictionary of models to evaluate
            
        Returns
        -------
        dict
            Dictionary containing the best model and its performance
        """
        best_model_name = None
        best_score = float('-inf')
        results = {}
        
        for name, model in models.items():
            scores = self.evaluate_model(model, X, y)
            results[name] = scores
            
            if -scores['mse'] > best_score:
                best_score = -scores['mse']
                best_model_name = name
                self.best_model = model
                self.best_score = best_score
        
        return {
            'best_model_name': best_model_name,
            'best_model': self.best_model,
            'best_score': self.best_score,
            'all_results': results
        } 
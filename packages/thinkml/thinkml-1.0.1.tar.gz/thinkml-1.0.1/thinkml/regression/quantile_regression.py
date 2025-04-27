"""
Quantile regression models for estimating conditional quantiles.
"""

from typing import Optional, Union, Dict, Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array

class QuantileRegressor(BaseEstimator, RegressorMixin):
    """
    A regressor for estimating conditional quantiles.
    
    This regressor implements quantile regression, which estimates the conditional
    quantile of the target variable given the input features.
    
    Parameters
    ----------
    quantile : float, default=0.5
        The quantile to estimate. Must be between 0 and 1.
    alpha : float, default=0.0
        The regularization strength. Larger values specify stronger regularization.
    solver : {'interior-point', 'highs-ds', 'highs-ipm', 'highs'}, default='interior-point'
        The solver to use in the optimization.
    fit_intercept : bool, default=True
        Whether to calculate the intercept for this model.
    """
    
    def __init__(
        self,
        quantile: float = 0.5,
        alpha: float = 0.0,
        solver: str = 'interior-point',
        fit_intercept: bool = True
    ):
        if not 0 < quantile < 1:
            raise ValueError("quantile must be between 0 and 1")
        if alpha < 0:
            raise ValueError("alpha must be non-negative")
            
        self.quantile = quantile
        self.alpha = alpha
        self.solver = solver
        self.fit_intercept = fit_intercept
    
    def _quantile_loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate the quantile loss."""
        diff = y_true - y_pred
        return np.mean(np.maximum(self.quantile * diff, (self.quantile - 1) * diff))
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> 'QuantileRegressor':
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
        X, y = check_X_y(X, y)
        
        if self.fit_intercept:
            X = np.column_stack([np.ones(X.shape[0]), X])
        
        from scipy.optimize import linprog
        
        n_samples, n_features = X.shape
        c = np.concatenate([np.zeros(n_features), np.ones(n_samples), np.ones(n_samples)])
        
        # Constraints for quantile regression
        A_ub = np.vstack([
            np.hstack([X, -np.eye(n_samples), np.zeros((n_samples, n_samples))]),
            np.hstack([-X, np.zeros((n_samples, n_samples)), -np.eye(n_samples)])
        ])
        b_ub = np.concatenate([y, -y])
        
        # Add L1 regularization if alpha > 0
        if self.alpha > 0:
            c[:n_features] = self.alpha
        
        # Solve the linear programming problem
        result = linprog(
            c=c,
            A_ub=A_ub,
            b_ub=b_ub,
            method=self.solver
        )
        
        if not result.success:
            raise RuntimeError(f"Optimization failed: {result.message}")
        
        self.coef_ = result.x[:n_features]
        if self.fit_intercept:
            self.intercept_ = self.coef_[0]
            self.coef_ = self.coef_[1:]
        else:
            self.intercept_ = 0.0
        
        return self
    
    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Predict using the quantile regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        y : array-like of shape (n_samples,)
            Predicted conditional quantile values.
        """
        X = check_array(X)
        return X @ self.coef_ + self.intercept_
    
    def score(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> float:
        """
        Return the quantile loss score.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.
        y : array-like of shape (n_samples,)
            True values for X.
            
        Returns
        -------
        score : float
            Quantile loss score.
        """
        y_pred = self.predict(X)
        return -self._quantile_loss(y, y_pred)  # Negative because higher score is better 
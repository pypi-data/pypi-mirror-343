"""
Censored regression models for handling censored data.
"""

from typing import Optional, Union, Dict, Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression
from sklearn.utils.validation import check_X_y, check_array

class CensoredRegressor(BaseEstimator, RegressorMixin):
    """
    A regressor for handling censored data.
    
    This regressor is designed to handle data where some observations are censored
    (i.e., we only know that they are above or below a certain threshold).
    
    Parameters
    ----------
    base_estimator : estimator object, default=None
        The base estimator to use for regression. If None, LinearRegression is used.
    censoring : {'left', 'right', 'interval'}, default='right'
        The type of censoring to handle.
    threshold : float, default=None
        The censoring threshold. Required for 'left' and 'right' censoring.
    lower_bound : float, default=None
        The lower bound for interval censoring.
    upper_bound : float, default=None
        The upper bound for interval censoring.
    """
    
    def __init__(
        self,
        base_estimator: Optional[BaseEstimator] = None,
        censoring: str = 'right',
        threshold: Optional[float] = None,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None
    ):
        self.base_estimator = base_estimator or LinearRegression()
        self.censoring = censoring
        self.threshold = threshold
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        if censoring in ['left', 'right'] and threshold is None:
            raise ValueError("threshold must be specified for left or right censoring")
        if censoring == 'interval' and (lower_bound is None or upper_bound is None):
            raise ValueError("lower_bound and upper_bound must be specified for interval censoring")
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> 'CensoredRegressor':
        """
        Fit the censored regression model.
        
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
        
        if self.censoring == 'right':
            mask = y > self.threshold
            y[mask] = self.threshold
        elif self.censoring == 'left':
            mask = y < self.threshold
            y[mask] = self.threshold
        elif self.censoring == 'interval':
            mask = (y < self.lower_bound) | (y > self.upper_bound)
            y[y < self.lower_bound] = self.lower_bound
            y[y > self.upper_bound] = self.upper_bound
        
        self.base_estimator.fit(X, y)
        return self
    
    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Predict using the censored regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        y : array-like of shape (n_samples,)
            Predicted values.
        """
        X = check_array(X)
        return self.base_estimator.predict(X)
    
    def score(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> float:
        """
        Return the coefficient of determination R^2 of the prediction.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.
        y : array-like of shape (n_samples,)
            True values for X.
            
        Returns
        -------
        score : float
            R^2 of self.predict(X) wrt. y.
        """
        return self.base_estimator.score(X, y) 
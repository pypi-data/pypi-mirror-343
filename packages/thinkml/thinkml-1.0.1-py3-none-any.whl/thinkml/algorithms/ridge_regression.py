"""
Ridge Regression implementation for ThinkML.

This module provides a Ridge Regression model implemented from scratch
using gradient descent optimization with L2 regularization.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel

class RidgeRegression(BaseModel):
    """
    Ridge Regression model implemented from scratch.
    
    This model uses gradient descent with L2 regularization to optimize
    the parameters and supports both small and large datasets.
    """
    
    def __init__(
        self,
        alpha: float = 1.0,
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        chunk_size: int = 10000,
        tol: float = 1e-5,
        verbose: bool = False
    ):
        """
        Initialize the Ridge Regression model.
        
        Parameters
        ----------
        alpha : float, default=1.0
            Regularization strength
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        n_iterations : int, default=1000
            Maximum number of iterations for gradient descent
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        tol : float, default=1e-5
            Tolerance for convergence
        verbose : bool, default=False
            Whether to print progress during training
        """
        super().__init__(chunk_size=chunk_size)
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.tol = tol
        self.verbose = verbose
        self.weights = None
        self.bias = None
        self.loss_history = []
    
    def fit(self, X, y):
        """
        Fit the Ridge Regression model to the data.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Training features
        y : Union[pd.Series, np.ndarray, dd.Series]
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        # Preprocess data
        X, y = self._preprocess_data(X, y)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame) or isinstance(y, dd.Series)
        
        if is_dask:
            # For Dask DataFrames, convert to Dask arrays
            if isinstance(X, dd.DataFrame):
                X = X.to_dask_array()
            if isinstance(y, dd.Series):
                y = y.to_dask_array()
            
            # Initialize parameters
            n_features = X.shape[1]
            self.weights = da.zeros(n_features)
            self.bias = da.zeros(1)
            
            # Gradient descent with Dask
            for i in range(self.n_iterations):
                # Compute predictions
                y_pred = da.dot(X, self.weights) + self.bias
                
                # Compute gradients with L2 regularization
                dw = da.mean(da.multiply(X, (y_pred - y)[:, np.newaxis]), axis=0) + self.alpha * self.weights
                db = da.mean(y_pred - y)
                
                # Update parameters
                self.weights -= self.learning_rate * dw
                self.bias -= self.learning_rate * db
                
                # Compute loss with L2 regularization
                mse = da.mean((y_pred - y) ** 2)
                l2_reg = 0.5 * self.alpha * da.sum(self.weights ** 2)
                loss = mse + l2_reg
                self.loss_history.append(float(loss.compute()))
                
                # Check for convergence
                if i > 0 and abs(self.loss_history[-1] - self.loss_history[-2]) < self.tol:
                    if self.verbose:
                        print(f"Converged at iteration {i+1}")
                    break
                
                if self.verbose and (i+1) % 100 == 0:
                    print(f"Iteration {i+1}, Loss: {self.loss_history[-1]}")
        else:
            # For numpy arrays or pandas DataFrames
            # Initialize parameters
            n_samples, n_features = X.shape
            self.weights = np.zeros(n_features)
            self.bias = 0
            
            # Gradient descent
            for i in range(self.n_iterations):
                # Compute predictions
                y_pred = np.dot(X, self.weights) + self.bias
                
                # Compute gradients with L2 regularization
                dw = np.mean(X * (y_pred - y)[:, np.newaxis], axis=0) + self.alpha * self.weights
                db = np.mean(y_pred - y)
                
                # Update parameters
                self.weights -= self.learning_rate * dw
                self.bias -= self.learning_rate * db
                
                # Compute loss with L2 regularization
                mse = np.mean((y_pred - y) ** 2)
                l2_reg = 0.5 * self.alpha * np.sum(self.weights ** 2)
                loss = mse + l2_reg
                self.loss_history.append(loss)
                
                # Check for convergence
                if i > 0 and abs(self.loss_history[-1] - self.loss_history[-2]) < self.tol:
                    if self.verbose:
                        print(f"Converged at iteration {i+1}")
                    break
                
                if self.verbose and (i+1) % 100 == 0:
                    print(f"Iteration {i+1}, Loss: {self.loss_history[-1]}")
        
        self.is_fitted = True
        return self
    
    def predict(self, X):
        """
        Make predictions for X.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Samples
            
        Returns
        -------
        Union[np.ndarray, pd.Series, dd.Series]
            Predicted values
        """
        self._check_is_fitted()
        
        # Preprocess data
        X = self._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # For Dask DataFrames, convert to Dask arrays
            if isinstance(X, dd.DataFrame):
                X = X.to_dask_array()
            
            # Make predictions
            y_pred = da.dot(X, self.weights) + self.bias
            
            # Convert back to Dask Series if input was a DataFrame
            if isinstance(X, dd.DataFrame):
                y_pred = dd.from_dask_array(y_pred)
        else:
            # For numpy arrays or pandas DataFrames
            # Make predictions
            y_pred = np.dot(X, self.weights) + self.bias
        
        return y_pred
    
    def score(self, X, y):
        """
        Return the R² score of the model on the given test data and labels.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Test samples
        y : Union[pd.Series, np.ndarray, dd.Series]
            True labels for X
            
        Returns
        -------
        float
            R² score of the model
        """
        self._check_is_fitted()
        
        # Preprocess data
        X, y = self._preprocess_data(X, y)
        
        # Make predictions
        y_pred = self.predict(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(y, dd.Series) or isinstance(y_pred, dd.Series)
        
        if is_dask:
            # For Dask DataFrames, compute R² score
            y_mean = da.mean(y)
            ss_tot = da.sum((y - y_mean) ** 2)
            ss_res = da.sum((y - y_pred) ** 2)
            r2 = 1 - (ss_res / ss_tot)
            return float(r2.compute())
        else:
            # For numpy arrays or pandas DataFrames
            # Compute R² score
            y_mean = np.mean(y)
            ss_tot = np.sum((y - y_mean) ** 2)
            ss_res = np.sum((y - y_pred) ** 2)
            r2 = 1 - (ss_res / ss_tot)
            return r2 
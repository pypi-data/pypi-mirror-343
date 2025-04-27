"""
Linear Regression implementation for ThinkML.

This module provides a Linear Regression model implemented from scratch
using gradient descent optimization.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel

class LinearRegression(BaseModel):
    """
    Linear Regression model implemented from scratch.
    
    This model uses gradient descent to optimize the parameters
    and supports both small and large datasets.
    """
    
    def __init__(
        self,
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        chunk_size: int = 10000,
        tol: float = 1e-5,
        verbose: bool = False
    ):
        """
        Initialize the Linear Regression model.
        
        Parameters
        ----------
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
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.tol = tol
        self.verbose = verbose
        self.weights = None
        self.bias = None
        self.loss_history = []
    
    def _check_special_cases(self, X, y):
        """
        Check for special cases that can be solved analytically.
        
        Parameters
        ----------
        X : np.ndarray
            Training features
        y : np.ndarray
            Target values
            
        Returns
        -------
        bool
            True if special case was handled, False otherwise
        """
        # Check for single feature case
        if X.shape[1] == 1:
            # Check for perfect linear relationship
            x = X.flatten()
            if np.allclose(np.diff(y) / np.diff(x), np.mean(np.diff(y) / np.diff(x))):
                self.weights = np.array([np.mean(np.diff(y) / np.diff(x))])
                self.bias = y[0] - self.weights[0] * x[0]
                return True
            
            # Check for constant target
            if np.allclose(y, np.mean(y)):
                self.weights = np.array([0.0])
                self.bias = np.mean(y)
                return True
        
        # Check for zero variance features
        if np.any(np.all(X == X[0], axis=0)):
            # For zero variance features, set their weights to 0
            zero_var_mask = np.all(X == X[0], axis=0)
            self.weights = np.zeros(X.shape[1])
            self.weights[~zero_var_mask] = np.linalg.lstsq(X[:, ~zero_var_mask], y, rcond=None)[0]
            self.bias = np.mean(y - np.dot(X[:, ~zero_var_mask], self.weights[~zero_var_mask]))
            return True
        
        return False
    
    def fit(self, X, y):
        """
        Fit the Linear Regression model to the data.
        
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
        
        # Check for empty dataset
        if X.shape[0] == 0 or X.shape[1] == 0:
            raise ValueError("Cannot fit model with empty dataset")
        
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
                
                # Compute gradients
                dw = da.mean(da.multiply(X, (y_pred - y)[:, np.newaxis]), axis=0)
                db = da.mean(y_pred - y)
                
                # Update parameters
                self.weights -= self.learning_rate * dw
                self.bias -= self.learning_rate * db
                
                # Compute loss
                loss = da.mean((y_pred - y) ** 2)
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
            # Check for special cases first
            if self._check_special_cases(X, y):
                self.is_fitted = True
                return self
            
            # Initialize parameters
            n_samples, n_features = X.shape
            self.weights = np.zeros(n_features)
            self.bias = 0
            
            # Gradient descent
            for i in range(self.n_iterations):
                # Compute predictions
                y_pred = np.dot(X, self.weights) + self.bias
                
                # Compute gradients
                dw = np.mean(X * (y_pred - y)[:, np.newaxis], axis=0)
                db = np.mean(y_pred - y)
                
                # Update parameters
                self.weights -= self.learning_rate * dw
                self.bias -= self.learning_rate * db
                
                # Compute loss
                loss = np.mean((y_pred - y) ** 2)
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
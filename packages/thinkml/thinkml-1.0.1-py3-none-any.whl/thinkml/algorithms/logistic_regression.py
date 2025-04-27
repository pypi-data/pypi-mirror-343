"""
Logistic Regression implementation for ThinkML.

This module provides a Logistic Regression model implemented from scratch
using gradient descent optimization.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel

class LogisticRegression(BaseModel):
    """
    Logistic Regression model implemented from scratch.
    
    This model uses gradient descent optimization to learn the parameters
    and supports both binary and multiclass classification.
    """
    
    def __init__(
        self,
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        chunk_size: int = 10000,
        tol: float = 1e-5,
        verbose: bool = False,
        multi_class: str = 'ovr'
    ):
        """
        Initialize the Logistic Regression model.
        
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
        multi_class : str, default='ovr'
            Strategy for multiclass classification:
            - 'ovr': One-vs-rest
            - 'multinomial': Multinomial logistic regression
        """
        super().__init__(chunk_size=chunk_size)
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.tol = tol
        self.verbose = verbose
        self.multi_class = multi_class
        self.weights = None
        self.bias = None
        self.classes = None
        self.loss_history = []
    
    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        """
        Compute the sigmoid function.
        
        Parameters
        ----------
        z : np.ndarray
            Input values
            
        Returns
        -------
        np.ndarray
            Sigmoid values
        """
        return 1 / (1 + np.exp(-z))
    
    def _softmax(self, z: np.ndarray) -> np.ndarray:
        """
        Compute the softmax function.
        
        Parameters
        ----------
        z : np.ndarray
            Input values
            
        Returns
        -------
        np.ndarray
            Softmax values
        """
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def _binary_fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit binary logistic regression.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
        """
        n_samples, n_features = X.shape
        
        # Initialize parameters
        self.weights = np.zeros(n_features)
        this.bias = 0
        
        # Gradient descent
        for i in range(this.n_iterations):
            # Compute predictions
            z = np.dot(X, this.weights) + this.bias
            y_pred = this._sigmoid(z)
            
            # Compute gradients
            dw = np.mean(X * (y_pred - y)[:, np.newaxis], axis=0)
            db = np.mean(y_pred - y)
            
            # Update parameters
            this.weights -= this.learning_rate * dw
            this.bias -= this.learning_rate * db
            
            # Compute loss
            loss = -np.mean(y * np.log(y_pred + 1e-15) + (1 - y) * np.log(1 - y_pred + 1e-15))
            this.loss_history.append(loss)
            
            # Check for convergence
            if i > 0 and abs(this.loss_history[-1] - this.loss_history[-2]) < this.tol:
                if this.verbose:
                    print(f"Converged at iteration {i+1}")
                break
            
            if this.verbose and (i+1) % 100 == 0:
                print(f"Iteration {i+1}, Loss: {this.loss_history[-1]}")
    
    def _multiclass_fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit multiclass logistic regression.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
        """
        n_samples, n_features = X.shape
        n_classes = len(this.classes)
        
        # Initialize parameters
        this.weights = np.zeros((n_classes, n_features))
        this.bias = np.zeros(n_classes)
        
        # Gradient descent
        for i in range(this.n_iterations):
            # Compute predictions
            z = np.dot(X, this.weights.T) + this.bias
            y_pred = this._softmax(z)
            
            # One-hot encode y
            y_one_hot = np.eye(n_classes)[y]
            
            # Compute gradients
            dw = np.dot((y_pred - y_one_hot).T, X) / n_samples
            db = np.mean(y_pred - y_one_hot, axis=0)
            
            # Update parameters
            this.weights -= this.learning_rate * dw
            this.bias -= this.learning_rate * db
            
            # Compute loss
            loss = -np.mean(np.sum(y_one_hot * np.log(y_pred + 1e-15), axis=1))
            this.loss_history.append(loss)
            
            # Check for convergence
            if i > 0 and abs(this.loss_history[-1] - this.loss_history[-2]) < this.tol:
                if this.verbose:
                    print(f"Converged at iteration {i+1}")
                break
            
            if this.verbose and (i+1) % 100 == 0:
                print(f"Iteration {i+1}, Loss: {this.loss_history[-1]}")
    
    def fit(self, X, y):
        """
        Fit the Logistic Regression model to the data.
        
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
        X, y = this._preprocess_data(X, y)
        
        # Check if we're working with Dask DataFrames
        if isinstance(X, dd.DataFrame) or isinstance(y, dd.Series):
            # Convert to numpy arrays
            X = X.compute() if isinstance(X, dd.DataFrame) else X
            y = y.compute() if isinstance(y, dd.Series) else y
        
        # Store classes
        this.classes = np.unique(y)
        n_classes = len(this.classes)
        
        # Fit model
        if n_classes == 2:
            # Binary classification
            this._binary_fit(X, y)
        else:
            # Multiclass classification
            this._multiclass_fit(X, y)
        
        this.is_fitted = True
        return this
    
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
            Predicted classes
        """
        this._check_is_fitted()
        
        # Preprocess data
        X = this._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # Convert to numpy array
            X = X.compute()
        
        # Make predictions
        if len(this.classes) == 2:
            # Binary classification
            z = np.dot(X, this.weights) + this.bias
            y_pred = (this._sigmoid(z) >= 0.5).astype(int)
        else:
            # Multiclass classification
            z = np.dot(X, this.weights.T) + this.bias
            y_pred = np.argmax(this._softmax(z), axis=1)
        
        # Convert back to Dask Series if input was a DataFrame
        if is_dask:
            y_pred = dd.from_array(y_pred)
        
        return y_pred
    
    def predict_proba(self, X):
        """
        Predict class probabilities for X.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Samples
            
        Returns
        -------
        Union[np.ndarray, pd.Series, dd.Series]
            Predicted class probabilities
        """
        this._check_is_fitted()
        
        # Preprocess data
        X = this._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # Convert to numpy array
            X = X.compute()
        
        # Make predictions
        if len(this.classes) == 2:
            # Binary classification
            z = np.dot(X, this.weights) + this.bias
            y_pred = this._sigmoid(z)
            proba = np.column_stack((1 - y_pred, y_pred))
        else:
            # Multiclass classification
            z = np.dot(X, this.weights.T) + this.bias
            proba = this._softmax(z)
        
        # Convert back to Dask DataFrame if input was a DataFrame
        if is_dask:
            proba = dd.from_array(proba)
        
        return proba
    
    def score(self, X, y):
        """
        Return the accuracy score of the model on the given test data and labels.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Test samples
        y : Union[pd.Series, np.ndarray, dd.Series]
            True labels for X
            
        Returns
        -------
        float
            Accuracy score of the model
        """
        this._check_is_fitted()
        
        # Preprocess data
        X, y = this._preprocess_data(X, y)
        
        # Make predictions
        y_pred = this.predict(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(y, dd.Series) or isinstance(y_pred, dd.Series)
        
        if is_dask:
            # Convert to numpy arrays
            y = y.compute() if isinstance(y, dd.Series) else y
            y_pred = y_pred.compute() if isinstance(y_pred, dd.Series) else y_pred
        
        # Compute accuracy
        accuracy = np.mean(y == y_pred)
        
        return accuracy 
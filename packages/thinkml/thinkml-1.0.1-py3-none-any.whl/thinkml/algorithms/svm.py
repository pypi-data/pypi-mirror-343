"""
Support Vector Machine (SVM) implementation for ThinkML.

This module provides SVM models for both regression and classification tasks,
implemented from scratch using gradient descent optimization.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel

class SVR(BaseModel):
    """
    Support Vector Regression implemented from scratch.
    
    This model uses gradient descent optimization to find the optimal hyperplane
    for regression tasks.
    """
    
    def __init__(
        self,
        kernel: str = 'linear',
        C: float = 1.0,
        epsilon: float = 0.1,
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        tol: float = 1e-4,
        chunk_size: int = 10000,
        verbose: bool = False
    ):
        """
        Initialize the Support Vector Regressor.
        
        Parameters
        ----------
        kernel : str, default='linear'
            Kernel type to be used in the algorithm
        C : float, default=1.0
            Regularization parameter
        epsilon : float, default=0.1
            Epsilon in the epsilon-SVR model
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        n_iterations : int, default=1000
            Maximum number of iterations for gradient descent
        tol : float, default=1e-4
            Tolerance for stopping criterion
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        verbose : bool, default=False
            Whether to print progress during training
        """
        super().__init__(chunk_size=chunk_size)
        this.kernel = kernel
        this.C = C
        this.epsilon = epsilon
        this.learning_rate = learning_rate
        this.n_iterations = n_iterations
        this.tol = tol
        this.verbose = verbose
        this.weights = None
        this.bias = None
        this.support_vectors = None
        this.support_vector_labels = None
    
    def _kernel_function(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """
        Compute the kernel matrix between two sets of samples.
        
        Parameters
        ----------
        X1 : np.ndarray
            First set of samples
        X2 : np.ndarray
            Second set of samples
            
        Returns
        -------
        np.ndarray
            Kernel matrix
        """
        if this.kernel == 'linear':
            return np.dot(X1, X2.T)
        elif this.kernel == 'rbf':
            # Implement RBF kernel
            diff = X1[:, np.newaxis] - X2
            return np.exp(-np.sum(diff ** 2, axis=2) / (2 * this.gamma ** 2))
        else:
            raise ValueError(f"Unsupported kernel: {this.kernel}")
    
    def _compute_gradients(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Compute gradients for the SVR loss function.
        
        Parameters
        ----------
        X : np.ndarray
            Training features
        y : np.ndarray
            Target values
            
        Returns
        -------
        Tuple[np.ndarray, float]
            Gradients for weights and bias
        """
        # Compute predictions
        y_pred = np.dot(X, this.weights) + this.bias
        
        # Compute errors
        errors = y_pred - y
        
        # Compute gradients
        mask = np.abs(errors) > this.epsilon
        grad_weights = np.zeros_like(this.weights)
        grad_bias = 0.0
        
        for i in range(len(X)):
            if mask[i]:
                sign = 1 if errors[i] > 0 else -1
                grad_weights += sign * X[i]
                grad_bias += sign
        
        # Add regularization term
        grad_weights = grad_weights / len(X) + this.C * this.weights
        grad_bias = grad_bias / len(X)
        
        return grad_weights, grad_bias
    
    def fit(self, X, y):
        """
        Fit the SVR model to the data.
        
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
        
        # Initialize weights and bias
        n_features = X.shape[1]
        this.weights = np.zeros(n_features)
        this.bias = 0.0
        
        # Gradient descent
        for i in range(this.n_iterations):
            # Compute gradients
            grad_weights, grad_bias = this._compute_gradients(X, y)
            
            # Update parameters
            this.weights -= this.learning_rate * grad_weights
            this.bias -= this.learning_rate * grad_bias
            
            # Check convergence
            if np.all(np.abs(grad_weights) < this.tol) and np.abs(grad_bias) < this.tol:
                if this.verbose:
                    print(f"Converged at iteration {i+1}")
                break
            
            if this.verbose and (i + 1) % 100 == 0:
                print(f"Iteration {i+1}/{this.n_iterations}")
        
        # Store support vectors
        y_pred = np.dot(X, this.weights) + this.bias
        errors = np.abs(y_pred - y)
        sv_mask = errors >= this.epsilon
        this.support_vectors = X[sv_mask]
        this.support_vector_labels = y[sv_mask]
        
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
            Predicted values
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
        y_pred = np.dot(X, this.weights) + this.bias
        
        # Convert back to Dask Series if input was a DataFrame
        if is_dask:
            y_pred = dd.from_array(y_pred)
        
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
        
        # Compute R² score
        y_mean = np.mean(y)
        ss_tot = np.sum((y - y_mean) ** 2)
        ss_res = np.sum((y - y_pred) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        return r2

class SVC(BaseModel):
    """
    Support Vector Classification implemented from scratch.
    
    This model uses gradient descent optimization to find the optimal hyperplane
    for classification tasks.
    """
    
    def __init__(
        self,
        kernel: str = 'linear',
        C: float = 1.0,
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        tol: float = 1e-4,
        chunk_size: int = 10000,
        verbose: bool = False
    ):
        """
        Initialize the Support Vector Classifier.
        
        Parameters
        ----------
        kernel : str, default='linear'
            Kernel type to be used in the algorithm
        C : float, default=1.0
            Regularization parameter
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        n_iterations : int, default=1000
            Maximum number of iterations for gradient descent
        tol : float, default=1e-4
            Tolerance for stopping criterion
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        verbose : bool, default=False
            Whether to print progress during training
        """
        super().__init__(chunk_size=chunk_size)
        this.kernel = kernel
        this.C = C
        this.learning_rate = learning_rate
        this.n_iterations = n_iterations
        this.tol = tol
        this.verbose = verbose
        this.weights = None
        this.bias = None
        this.support_vectors = None
        this.support_vector_labels = None
        this.classes = None
    
    def _kernel_function(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """
        Compute the kernel matrix between two sets of samples.
        
        Parameters
        ----------
        X1 : np.ndarray
            First set of samples
        X2 : np.ndarray
            Second set of samples
            
        Returns
        -------
        np.ndarray
            Kernel matrix
        """
        if this.kernel == 'linear':
            return np.dot(X1, X2.T)
        elif this.kernel == 'rbf':
            # Implement RBF kernel
            diff = X1[:, np.newaxis] - X2
            return np.exp(-np.sum(diff ** 2, axis=2) / (2 * this.gamma ** 2))
        else:
            raise ValueError(f"Unsupported kernel: {this.kernel}")
    
    def _compute_gradients(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Compute gradients for the SVM loss function.
        
        Parameters
        ----------
        X : np.ndarray
            Training features
        y : np.ndarray
            Target values
            
        Returns
        -------
        Tuple[np.ndarray, float]
            Gradients for weights and bias
        """
        # Compute predictions
        y_pred = np.dot(X, this.weights) + this.bias
        
        # Compute gradients
        grad_weights = np.zeros_like(this.weights)
        grad_bias = 0.0
        
        for i in range(len(X)):
            if y[i] * y_pred[i] < 1:  # Misclassified or within margin
                grad_weights -= y[i] * X[i]
                grad_bias -= y[i]
        
        # Add regularization term
        grad_weights = grad_weights / len(X) + this.C * this.weights
        grad_bias = grad_bias / len(X)
        
        return grad_weights, grad_bias
    
    def fit(self, X, y):
        """
        Fit the SVC model to the data.
        
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
        
        # Convert labels to binary
        y_binary = np.where(y == this.classes[0], -1, 1)
        
        # Initialize weights and bias
        n_features = X.shape[1]
        this.weights = np.zeros(n_features)
        this.bias = 0.0
        
        # Gradient descent
        for i in range(this.n_iterations):
            # Compute gradients
            grad_weights, grad_bias = this._compute_gradients(X, y_binary)
            
            # Update parameters
            this.weights -= this.learning_rate * grad_weights
            this.bias -= this.learning_rate * grad_bias
            
            # Check convergence
            if np.all(np.abs(grad_weights) < this.tol) and np.abs(grad_bias) < this.tol:
                if this.verbose:
                    print(f"Converged at iteration {i+1}")
                break
            
            if this.verbose and (i + 1) % 100 == 0:
                print(f"Iteration {i+1}/{this.n_iterations}")
        
        # Store support vectors
        y_pred = np.dot(X, this.weights) + this.bias
        sv_mask = np.abs(y_binary * y_pred) <= 1
        this.support_vectors = X[sv_mask]
        this.support_vector_labels = y[sv_mask]
        
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
        y_pred = np.dot(X, this.weights) + this.bias
        y_pred = np.where(y_pred >= 0, this.classes[1], this.classes[0])
        
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
        
        # Compute decision function
        y_pred = np.dot(X, this.weights) + this.bias
        
        # Convert to probabilities using sigmoid
        proba = 1 / (1 + np.exp(-y_pred))
        proba = np.column_stack((1 - proba, proba))
        
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
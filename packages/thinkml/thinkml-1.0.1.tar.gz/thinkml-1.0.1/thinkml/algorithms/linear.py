"""
Linear models for classification and regression.

This module provides implementations of linear models including:
- Logistic Regression for classification
- Linear Regression for regression
- Ridge Regression for regression with L2 regularization
"""

import numpy as np
from typing import Optional, Union, Tuple

class LogisticRegression:
    """Logistic Regression classifier.
    
    Implements binary classification using logistic regression with
    gradient descent optimization.
    
    Parameters
    ----------
    learning_rate : float, default=0.01
        Step size for gradient descent
    max_iter : int, default=1000
        Maximum number of iterations for gradient descent
    tol : float, default=1e-4
        Tolerance for stopping criterion
    random_state : Optional[int], default=None
        Random seed for reproducibility
    """
    
    def __init__(
        self,
        learning_rate: float = 0.01,
        max_iter: int = 1000,
        tol: float = 1e-4,
        random_state: Optional[int] = None
    ):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.weights = None
        self.bias = None
        
    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        """Compute sigmoid function."""
        return 1 / (1 + np.exp(-z))
    
    def _initialize_parameters(self, n_features: int) -> None:
        """Initialize model parameters."""
        if self.random_state is not None:
            np.random.seed(self.random_state)
        self.weights = np.zeros(n_features)
        self.bias = 0
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LogisticRegression':
        """Fit the model to the data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        n_samples, n_features = X.shape
        self._initialize_parameters(n_features)
        
        for _ in range(self.max_iter):
            # Forward pass
            z = np.dot(X, self.weights) + self.bias
            y_pred = self._sigmoid(z)
            
            # Compute gradients
            dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
            db = (1/n_samples) * np.sum(y_pred - y)
            
            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
            # Check convergence
            if np.all(np.abs(dw) < self.tol) and np.abs(db) < self.tol:
                break
                
        return self
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples
            
        Returns
        -------
        array of shape (n_samples,)
            Predicted probabilities
        """
        X = np.asarray(X)
        z = np.dot(X, self.weights) + self.bias
        return self._sigmoid(z)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples
            
        Returns
        -------
        array of shape (n_samples,)
            Predicted class labels
        """
        return (self.predict_proba(X) >= 0.5).astype(int)

class LinearRegression:
    """Linear Regression model.
    
    Implements linear regression using the normal equation or
    gradient descent optimization.
    
    Parameters
    ----------
    method : str, default='normal'
        Method to use for optimization ('normal' or 'gradient')
    learning_rate : float, default=0.01
        Step size for gradient descent (only used if method='gradient')
    max_iter : int, default=1000
        Maximum number of iterations for gradient descent
    tol : float, default=1e-4
        Tolerance for stopping criterion
    """
    
    def __init__(
        self,
        method: str = 'normal',
        learning_rate: float = 0.01,
        max_iter: int = 1000,
        tol: float = 1e-4
    ):
        self.method = method
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.weights = None
        self.bias = None
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LinearRegression':
        """Fit the model to the data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        if self.method == 'normal':
            # Add bias term
            X_b = np.c_[np.ones((X.shape[0], 1)), X]
            # Normal equation: θ = (X^T X)^(-1) X^T y
            theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
            self.bias = theta[0]
            self.weights = theta[1:]
        else:
            # Gradient descent
            n_samples, n_features = X.shape
            self.weights = np.zeros(n_features)
            self.bias = 0
            
            for _ in range(self.max_iter):
                # Forward pass
                y_pred = np.dot(X, self.weights) + self.bias
                
                # Compute gradients
                dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
                db = (1/n_samples) * np.sum(y_pred - y)
                
                # Update parameters
                self.weights -= self.learning_rate * dw
                self.bias -= self.learning_rate * db
                
                # Check convergence
                if np.all(np.abs(dw) < self.tol) and np.abs(db) < self.tol:
                    break
                    
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples
            
        Returns
        -------
        array of shape (n_samples,)
            Predicted target values
        """
        X = np.asarray(X)
        return np.dot(X, self.weights) + self.bias

class RidgeRegression:
    """Ridge Regression model.
    
    Implements linear regression with L2 regularization.
    
    Parameters
    ----------
    alpha : float, default=1.0
        Regularization strength
    method : str, default='normal'
        Method to use for optimization ('normal' or 'gradient')
    learning_rate : float, default=0.01
        Step size for gradient descent (only used if method='gradient')
    max_iter : int, default=1000
        Maximum number of iterations for gradient descent
    tol : float, default=1e-4
        Tolerance for stopping criterion
    """
    
    def __init__(
        self,
        alpha: float = 1.0,
        method: str = 'normal',
        learning_rate: float = 0.01,
        max_iter: int = 1000,
        tol: float = 1e-4
    ):
        self.alpha = alpha
        self.method = method
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.weights = None
        self.bias = None
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RidgeRegression':
        """Fit the model to the data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        if self.method == 'normal':
            # Add bias term
            X_b = np.c_[np.ones((X.shape[0], 1)), X]
            # Ridge equation: θ = (X^T X + αI)^(-1) X^T y
            n_features = X_b.shape[1]
            theta = np.linalg.inv(
                X_b.T.dot(X_b) + self.alpha * np.eye(n_features)
            ).dot(X_b.T).dot(y)
            self.bias = theta[0]
            self.weights = theta[1:]
        else:
            # Gradient descent
            n_samples, n_features = X.shape
            self.weights = np.zeros(n_features)
            self.bias = 0
            
            for _ in range(self.max_iter):
                # Forward pass
                y_pred = np.dot(X, self.weights) + self.bias
                
                # Compute gradients with L2 regularization
                dw = (1/n_samples) * (
                    np.dot(X.T, (y_pred - y)) + self.alpha * self.weights
                )
                db = (1/n_samples) * np.sum(y_pred - y)
                
                # Update parameters
                self.weights -= self.learning_rate * dw
                self.bias -= self.learning_rate * db
                
                # Check convergence
                if np.all(np.abs(dw) < self.tol) and np.abs(db) < self.tol:
                    break
                    
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples
            
        Returns
        -------
        array of shape (n_samples,)
            Predicted target values
        """
        X = np.asarray(X)
        return np.dot(X, self.weights) + self.bias 
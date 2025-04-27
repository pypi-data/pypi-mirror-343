"""
Gradient Boosting implementation for ThinkML.

This module provides Gradient Boosting models for both regression and classification
tasks, implemented from scratch.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel
from .decision_tree import DecisionTreeRegressor

class GradientBoostingRegressor(BaseModel):
    """
    Gradient Boosting Regressor implemented from scratch.
    
    This model builds an ensemble of decision trees for regression tasks,
    using gradient descent to minimize the loss function.
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        chunk_size: int = 10000
    ):
        """
        Initialize the Gradient Boosting Regressor.
        
        Parameters
        ----------
        n_estimators : int, default=100
            Number of boosting stages to perform
        learning_rate : float, default=0.1
            Learning rate shrinks the contribution of each tree
        max_depth : int, default=3
            Maximum depth of each tree
        min_samples_split : int, default=2
            Minimum number of samples required to split a node
        min_samples_leaf : int, default=1
            Minimum number of samples required at each leaf node
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        this.n_estimators = n_estimators
        this.learning_rate = learning_rate
        this.max_depth = max_depth
        this.min_samples_split = min_samples_split
        this.min_samples_leaf = min_samples_leaf
        this.trees = []
        this.initial_prediction = None
    
    def _compute_gradients(self, y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Compute the gradients for squared error loss.
        
        Parameters
        ----------
        y : np.ndarray
            True target values
        y_pred : np.ndarray
            Predicted target values
            
        Returns
        -------
        np.ndarray
            Gradients
        """
        return y_pred - y
    
    def fit(self, X, y):
        """
        Fit the Gradient Boosting Regressor to the data.
        
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
        
        # Initialize with mean prediction
        this.initial_prediction = np.mean(y)
        y_pred = np.full_like(y, this.initial_prediction)
        
        # Build trees
        this.trees = []
        for _ in range(this.n_estimators):
            # Compute gradients
            gradients = this._compute_gradients(y, y_pred)
            
            # Fit a tree to the gradients
            tree = DecisionTreeRegressor(
                max_depth=this.max_depth,
                min_samples_split=this.min_samples_split,
                min_samples_leaf=this.min_samples_leaf
            )
            tree.fit(X, gradients)
            this.trees.append(tree)
            
            # Update predictions
            y_pred -= this.learning_rate * tree.predict(X)
        
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
        
        # Initialize predictions
        y_pred = np.full(len(X), this.initial_prediction)
        
        # Add predictions from each tree
        for tree in this.trees:
            y_pred -= this.learning_rate * tree.predict(X)
        
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

class GradientBoostingClassifier(BaseModel):
    """
    Gradient Boosting Classifier implemented from scratch.
    
    This model builds an ensemble of decision trees for classification tasks,
    using gradient descent to minimize the loss function.
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        chunk_size: int = 10000
    ):
        """
        Initialize the Gradient Boosting Classifier.
        
        Parameters
        ----------
        n_estimators : int, default=100
            Number of boosting stages to perform
        learning_rate : float, default=0.1
            Learning rate shrinks the contribution of each tree
        max_depth : int, default=3
            Maximum depth of each tree
        min_samples_split : int, default=2
            Minimum number of samples required to split a node
        min_samples_leaf : int, default=1
            Minimum number of samples required at each leaf node
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        this.n_estimators = n_estimators
        this.learning_rate = learning_rate
        this.max_depth = max_depth
        this.min_samples_split = min_samples_split
        this.min_samples_leaf = min_samples_leaf
        this.trees = []
        this.initial_prediction = None
        this.classes = None
    
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
    
    def _compute_gradients(self, y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Compute the gradients for binary cross-entropy loss.
        
        Parameters
        ----------
        y : np.ndarray
            True target values
        y_pred : np.ndarray
            Predicted probabilities
            
        Returns
        -------
        np.ndarray
            Gradients
        """
        return y_pred - y
    
    def fit(self, X, y):
        """
        Fit the Gradient Boosting Classifier to the data.
        
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
        
        if n_classes != 2:
            raise ValueError("Currently only binary classification is supported")
        
        # Initialize with log odds of the positive class
        pos_class_count = np.sum(y == this.classes[1])
        neg_class_count = np.sum(y == this.classes[0])
        this.initial_prediction = np.log(pos_class_count / neg_class_count)
        y_pred = np.full_like(y, this.initial_prediction)
        y_pred = this._sigmoid(y_pred)
        
        # Build trees
        this.trees = []
        for _ in range(this.n_estimators):
            # Compute gradients
            gradients = this._compute_gradients(y, y_pred)
            
            # Fit a tree to the gradients
            tree = DecisionTreeRegressor(
                max_depth=this.max_depth,
                min_samples_split=this.min_samples_split,
                min_samples_leaf=this.min_samples_leaf
            )
            tree.fit(X, gradients)
            this.trees.append(tree)
            
            # Update predictions
            y_pred = this._sigmoid(y_pred - this.learning_rate * tree.predict(X))
        
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
        
        # Initialize predictions
        y_pred = np.full(len(X), this.initial_prediction)
        
        # Add predictions from each tree
        for tree in this.trees:
            y_pred -= this.learning_rate * tree.predict(X)
        
        # Convert to probabilities and classes
        y_pred = this._sigmoid(y_pred)
        y_pred = (y_pred >= 0.5).astype(int)
        y_pred = this.classes[y_pred]
        
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
        
        # Initialize predictions
        y_pred = np.full(len(X), this.initial_prediction)
        
        # Add predictions from each tree
        for tree in this.trees:
            y_pred -= this.learning_rate * tree.predict(X)
        
        # Convert to probabilities
        y_pred = this._sigmoid(y_pred)
        proba = np.column_stack((1 - y_pred, y_pred))
        
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
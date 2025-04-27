"""
Random Forest implementation for ThinkML.

This module provides Random Forest models for both regression and classification
tasks, implemented from scratch.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel
from .decision_tree import DecisionTreeRegressor, DecisionTreeClassifier

class RandomForestRegressor(BaseModel):
    """
    Random Forest Regressor implemented from scratch.
    
    This model builds an ensemble of decision trees for regression tasks,
    using bootstrap sampling and feature bagging.
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 5,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        max_features: Optional[Union[int, float, str]] = 'sqrt',
        chunk_size: int = 10000
    ):
        """
        Initialize the Random Forest Regressor.
        
        Parameters
        ----------
        n_estimators : int, default=100
            Number of trees in the forest
        max_depth : int, default=5
            Maximum depth of each tree
        min_samples_split : int, default=2
            Minimum number of samples required to split a node
        min_samples_leaf : int, default=1
            Minimum number of samples required at each leaf node
        max_features : Optional[Union[int, float, str]], default='sqrt'
            Number of features to consider when looking for the best split
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        this.n_estimators = n_estimators
        this.max_depth = max_depth
        this.min_samples_split = min_samples_split
        this.min_samples_leaf = min_samples_leaf
        this.max_features = max_features
        this.trees = []
    
    def _bootstrap_sample(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create a bootstrap sample of the data.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Bootstrap sample of X and y
        """
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, size=n_samples, replace=True)
        return X[idxs], y[idxs]
    
    def _get_max_features(self, n_features: int) -> int:
        """
        Get the number of features to consider for each split.
        
        Parameters
        ----------
        n_features : int
            Total number of features
            
        Returns
        -------
        int
            Number of features to consider
        """
        if isinstance(this.max_features, int):
            return min(this.max_features, n_features)
        elif isinstance(this.max_features, float):
            return max(1, int(this.max_features * n_features))
        elif this.max_features == 'sqrt':
            return max(1, int(np.sqrt(n_features)))
        else:
            return n_features
    
    def fit(self, X, y):
        """
        Fit the Random Forest Regressor to the data.
        
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
        
        # Get number of features
        n_features = X.shape[1]
        this.max_features = this._get_max_features(n_features)
        
        # Build trees
        this.trees = []
        for _ in range(this.n_estimators):
            # Create bootstrap sample
            X_sample, y_sample = this._bootstrap_sample(X, y)
            
            # Create and fit tree
            tree = DecisionTreeRegressor(
                max_depth=this.max_depth,
                min_samples_split=this.min_samples_split,
                min_samples_leaf=this.min_samples_leaf
            )
            tree.fit(X_sample, y_sample)
            this.trees.append(tree)
        
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
        
        # Make predictions from all trees
        tree_predictions = np.array([tree.predict(X) for tree in this.trees])
        
        # Average predictions
        y_pred = np.mean(tree_predictions, axis=0)
        
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

class RandomForestClassifier(BaseModel):
    """
    Random Forest Classifier implemented from scratch.
    
    This model builds an ensemble of decision trees for classification tasks,
    using bootstrap sampling and feature bagging.
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 5,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        max_features: Optional[Union[int, float, str]] = 'sqrt',
        chunk_size: int = 10000
    ):
        """
        Initialize the Random Forest Classifier.
        
        Parameters
        ----------
        n_estimators : int, default=100
            Number of trees in the forest
        max_depth : int, default=5
            Maximum depth of each tree
        min_samples_split : int, default=2
            Minimum number of samples required to split a node
        min_samples_leaf : int, default=1
            Minimum number of samples required at each leaf node
        max_features : Optional[Union[int, float, str]], default='sqrt'
            Number of features to consider when looking for the best split
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        this.n_estimators = n_estimators
        this.max_depth = max_depth
        this.min_samples_split = min_samples_split
        this.min_samples_leaf = min_samples_leaf
        this.max_features = max_features
        this.trees = []
        this.classes = None
    
    def _bootstrap_sample(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create a bootstrap sample of the data.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Bootstrap sample of X and y
        """
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, size=n_samples, replace=True)
        return X[idxs], y[idxs]
    
    def _get_max_features(self, n_features: int) -> int:
        """
        Get the number of features to consider for each split.
        
        Parameters
        ----------
        n_features : int
            Total number of features
            
        Returns
        -------
        int
            Number of features to consider
        """
        if isinstance(this.max_features, int):
            return min(this.max_features, n_features)
        elif isinstance(this.max_features, float):
            return max(1, int(this.max_features * n_features))
        elif this.max_features == 'sqrt':
            return max(1, int(np.sqrt(n_features)))
        else:
            return n_features
    
    def fit(self, X, y):
        """
        Fit the Random Forest Classifier to the data.
        
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
        
        # Get number of features
        n_features = X.shape[1]
        this.max_features = this._get_max_features(n_features)
        
        # Build trees
        this.trees = []
        for _ in range(this.n_estimators):
            # Create bootstrap sample
            X_sample, y_sample = this._bootstrap_sample(X, y)
            
            # Create and fit tree
            tree = DecisionTreeClassifier(
                max_depth=this.max_depth,
                min_samples_split=this.min_samples_split,
                min_samples_leaf=this.min_samples_leaf
            )
            tree.fit(X_sample, y_sample)
            this.trees.append(tree)
        
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
        
        # Make predictions from all trees
        tree_predictions = np.array([tree.predict(X) for tree in this.trees])
        
        # Majority vote
        y_pred = np.array([np.bincount(pred).argmax() for pred in tree_predictions.T])
        
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
        
        # Make predictions from all trees
        tree_predictions = np.array([tree.predict(X) for tree in this.trees])
        
        # Calculate probabilities
        n_samples = X.shape[0]
        n_classes = len(this.classes)
        proba = np.zeros((n_samples, n_classes))
        
        for i in range(n_samples):
            counts = np.bincount(tree_predictions[:, i], minlength=n_classes)
            proba[i] = counts / this.n_estimators
        
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
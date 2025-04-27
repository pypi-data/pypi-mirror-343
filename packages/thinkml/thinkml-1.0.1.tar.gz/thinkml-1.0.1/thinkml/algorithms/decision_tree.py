"""
Decision Tree implementation for ThinkML.

This module provides Decision Tree models for both regression and classification
tasks, implemented from scratch.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel

class Node:
    """Node class for Decision Tree."""
    
    def __init__(
        self,
        feature_idx: Optional[int] = None,
        threshold: Optional[float] = None,
        left: Optional['Node'] = None,
        right: Optional['Node'] = None,
        value: Optional[float] = None
    ):
        """
        Initialize a node in the decision tree.
        
        Parameters
        ----------
        feature_idx : Optional[int], default=None
            Index of the feature to split on
        threshold : Optional[float], default=None
            Threshold value for the split
        left : Optional[Node], default=None
            Left child node
        right : Optional[Node], default=None
            Right child node
        value : Optional[float], default=None
            Predicted value (for leaf nodes)
        """
        self.feature_idx = feature_idx
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class DecisionTreeRegressor(BaseModel):
    """
    Decision Tree Regressor implemented from scratch.
    
    This model builds a decision tree for regression tasks using
    mean squared error as the splitting criterion.
    """
    
    def __init__(
        self,
        max_depth: int = 5,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        chunk_size: int = 10000
    ):
        """
        Initialize the Decision Tree Regressor.
        
        Parameters
        ----------
        max_depth : int, default=5
            Maximum depth of the tree
        min_samples_split : int, default=2
            Minimum number of samples required to split a node
        min_samples_leaf : int, default=1
            Minimum number of samples required at each leaf node
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root = None
    
    def _mse(self, y: np.ndarray) -> float:
        """Calculate mean squared error."""
        return np.mean((y - np.mean(y)) ** 2)
    
    def _best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[Optional[int], Optional[float]]:
        """
        Find the best split for the data.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
            
        Returns
        -------
        Tuple[Optional[int], Optional[float]]
            Best feature index and threshold
        """
        n_samples, n_features = X.shape
        best_mse = float('inf')
        best_feature_idx = None
        best_threshold = None
        
        # Calculate parent MSE
        parent_mse = self._mse(y)
        
        # Try each feature
        for feature_idx in range(n_features):
            # Get unique values for the feature
            thresholds = np.unique(X[:, feature_idx])
            
            # Try each threshold
            for threshold in thresholds:
                # Split the data
                left_mask = X[:, feature_idx] <= threshold
                right_mask = ~left_mask
                
                # Skip if split doesn't meet minimum samples
                if (np.sum(left_mask) < self.min_samples_leaf or 
                    np.sum(right_mask) < self.min_samples_leaf):
                    continue
                
                # Calculate MSE for this split
                left_mse = self._mse(y[left_mask])
                right_mse = self._mse(y[right_mask])
                split_mse = (np.sum(left_mask) * left_mse + 
                           np.sum(right_mask) * right_mse) / n_samples
                
                # Update best split if better
                if split_mse < best_mse:
                    best_mse = split_mse
                    best_feature_idx = feature_idx
                    best_threshold = threshold
        
        return best_feature_idx, best_threshold
    
    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
        """
        Build the decision tree recursively.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
        depth : int, default=0
            Current depth of the tree
            
        Returns
        -------
        Node
            Root node of the tree
        """
        n_samples, n_features = X.shape
        
        # Check stopping criteria
        if (depth >= self.max_depth or 
            n_samples < self.min_samples_split or 
            len(np.unique(y)) == 1):
            return Node(value=np.mean(y))
        
        # Find best split
        best_feature_idx, best_threshold = self._best_split(X, y)
        
        # If no split found, create leaf node
        if best_feature_idx is None:
            return Node(value=np.mean(y))
        
        # Split the data
        left_mask = X[:, best_feature_idx] <= best_threshold
        right_mask = ~left_mask
        
        # Create child nodes
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)
        
        return Node(best_feature_idx, best_threshold, left_child, right_child)
    
    def fit(self, X, y):
        """
        Fit the Decision Tree Regressor to the data.
        
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
        if isinstance(X, dd.DataFrame) or isinstance(y, dd.Series):
            # Convert to numpy arrays
            X = X.compute() if isinstance(X, dd.DataFrame) else X
            y = y.compute() if isinstance(y, dd.Series) else y
        
        # Build the tree
        self.root = self._build_tree(X, y)
        self.is_fitted = True
        return self
    
    def _traverse_tree(self, x: np.ndarray, node: Node) -> float:
        """
        Traverse the tree to make a prediction.
        
        Parameters
        ----------
        x : np.ndarray
            Single sample
        node : Node
            Current node
            
        Returns
        -------
        float
            Predicted value
        """
        if node.value is not None:
            return node.value
        
        if x[node.feature_idx] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)
    
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
            # Convert to numpy array
            X = X.compute()
        
        # Make predictions
        y_pred = np.array([self._traverse_tree(x, self.root) for x in X])
        
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
        self._check_is_fitted()
        
        # Preprocess data
        X, y = self._preprocess_data(X, y)
        
        # Make predictions
        y_pred = self.predict(X)
        
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

class DecisionTreeClassifier(BaseModel):
    """
    Decision Tree Classifier implemented from scratch.
    
    This model builds a decision tree for classification tasks using
    gini impurity as the splitting criterion.
    """
    
    def __init__(
        self,
        max_depth: int = 5,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        chunk_size: int = 10000
    ):
        """
        Initialize the Decision Tree Classifier.
        
        Parameters
        ----------
        max_depth : int, default=5
            Maximum depth of the tree
        min_samples_split : int, default=2
            Minimum number of samples required to split a node
        min_samples_leaf : int, default=1
            Minimum number of samples required at each leaf node
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root = None
        self.classes = None
    
    def _gini(self, y: np.ndarray) -> float:
        """Calculate gini impurity."""
        classes, counts = np.unique(y, return_counts=True)
        n_samples = len(y)
        gini = 1.0
        
        for count in counts:
            prob = count / n_samples
            gini -= prob ** 2
        
        return gini
    
    def _best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[Optional[int], Optional[float]]:
        """
        Find the best split for the data.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
            
        Returns
        -------
        Tuple[Optional[int], Optional[float]]
            Best feature index and threshold
        """
        n_samples, n_features = X.shape
        best_gini = float('inf')
        best_feature_idx = None
        best_threshold = None
        
        # Calculate parent gini
        parent_gini = self._gini(y)
        
        # Try each feature
        for feature_idx in range(n_features):
            # Get unique values for the feature
            thresholds = np.unique(X[:, feature_idx])
            
            # Try each threshold
            for threshold in thresholds:
                # Split the data
                left_mask = X[:, feature_idx] <= threshold
                right_mask = ~left_mask
                
                # Skip if split doesn't meet minimum samples
                if (np.sum(left_mask) < self.min_samples_leaf or 
                    np.sum(right_mask) < self.min_samples_leaf):
                    continue
                
                # Calculate gini for this split
                left_gini = self._gini(y[left_mask])
                right_gini = self._gini(y[right_mask])
                split_gini = (np.sum(left_mask) * left_gini + 
                            np.sum(right_mask) * right_gini) / n_samples
                
                # Update best split if better
                if split_gini < best_gini:
                    best_gini = split_gini
                    best_feature_idx = feature_idx
                    best_threshold = threshold
        
        return best_feature_idx, best_threshold
    
    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
        """
        Build the decision tree recursively.
        
        Parameters
        ----------
        X : np.ndarray
            Feature matrix
        y : np.ndarray
            Target values
        depth : int, default=0
            Current depth of the tree
            
        Returns
        -------
        Node
            Root node of the tree
        """
        n_samples, n_features = X.shape
        
        # Check stopping criteria
        if (depth >= self.max_depth or 
            n_samples < self.min_samples_split or 
            len(np.unique(y)) == 1):
            # Return most common class
            return Node(value=np.argmax(np.bincount(y)))
        
        # Find best split
        best_feature_idx, best_threshold = self._best_split(X, y)
        
        # If no split found, create leaf node
        if best_feature_idx is None:
            return Node(value=np.argmax(np.bincount(y)))
        
        # Split the data
        left_mask = X[:, best_feature_idx] <= best_threshold
        right_mask = ~left_mask
        
        # Create child nodes
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)
        
        return Node(best_feature_idx, best_threshold, left_child, right_child)
    
    def fit(self, X, y):
        """
        Fit the Decision Tree Classifier to the data.
        
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
        if isinstance(X, dd.DataFrame) or isinstance(y, dd.Series):
            # Convert to numpy arrays
            X = X.compute() if isinstance(X, dd.DataFrame) else X
            y = y.compute() if isinstance(y, dd.Series) else y
        
        # Store classes
        self.classes = np.unique(y)
        
        # Build the tree
        self.root = self._build_tree(X, y)
        self.is_fitted = True
        return self
    
    def _traverse_tree(self, x: np.ndarray, node: Node) -> int:
        """
        Traverse the tree to make a prediction.
        
        Parameters
        ----------
        x : np.ndarray
            Single sample
        node : Node
            Current node
            
        Returns
        -------
        int
            Predicted class
        """
        if node.value is not None:
            return node.value
        
        if x[node.feature_idx] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)
    
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
        self._check_is_fitted()
        
        # Preprocess data
        X = self._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # Convert to numpy array
            X = X.compute()
        
        # Make predictions
        y_pred = np.array([self._traverse_tree(x, self.root) for x in X])
        
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
        self._check_is_fitted()
        
        # Preprocess data
        X = self._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # Convert to numpy array
            X = X.compute()
        
        # Make predictions
        y_pred = self.predict(X)
        
        # Convert to probabilities
        n_samples = len(X)
        n_classes = len(self.classes)
        proba = np.zeros((n_samples, n_classes))
        
        for i, pred in enumerate(y_pred):
            proba[i, pred] = 1
        
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
        self._check_is_fitted()
        
        # Preprocess data
        X, y = self._preprocess_data(X, y)
        
        # Make predictions
        y_pred = self.predict(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(y, dd.Series) or isinstance(y_pred, dd.Series)
        
        if is_dask:
            # Convert to numpy arrays
            y = y.compute() if isinstance(y, dd.Series) else y
            y_pred = y_pred.compute() if isinstance(y_pred, dd.Series) else y_pred
        
        # Compute accuracy
        accuracy = np.mean(y == y_pred)
        
        return accuracy 
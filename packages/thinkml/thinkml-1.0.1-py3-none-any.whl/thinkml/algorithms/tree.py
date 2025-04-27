"""
Tree-based models for classification and regression.

This module provides implementations of:
- Decision Tree Classifier
- Decision Tree Regressor
- Random Forest Classifier
- Random Forest Regressor
"""

import numpy as np
from typing import Optional, Union, List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter

@dataclass
class Node:
    """Node in a decision tree."""
    feature: Optional[int] = None
    threshold: Optional[float] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    value: Optional[Union[float, int]] = None

class DecisionTreeClassifier:
    """Decision Tree Classifier.
    
    Parameters
    ----------
    max_depth : Optional[int], default=None
        Maximum depth of the tree
    min_samples_split : int, default=2
        Minimum number of samples required to split a node
    min_samples_leaf : int, default=1
        Minimum number of samples required at each leaf node
    criterion : str, default='gini'
        Function to measure the quality of a split ('gini' or 'entropy')
    random_state : Optional[int], default=None
        Random seed for reproducibility
    """
    
    def __init__(
        self,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        criterion: str = 'gini',
        random_state: Optional[int] = None
    ):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.random_state = random_state
        self.root = None
        
    def _gini(self, y: np.ndarray) -> float:
        """Calculate Gini impurity."""
        counter = Counter(y)
        impurity = 1
        for count in counter.values():
            prob = count / len(y)
            impurity -= prob ** 2
        return impurity
    
    def _entropy(self, y: np.ndarray) -> float:
        """Calculate entropy."""
        counter = Counter(y)
        entropy = 0
        for count in counter.values():
            prob = count / len(y)
            entropy -= prob * np.log2(prob)
        return entropy
    
    def _information_gain(
        self,
        parent: np.ndarray,
        left_child: np.ndarray,
        right_child: np.ndarray
    ) -> float:
        """Calculate information gain."""
        weight_left = len(left_child) / len(parent)
        weight_right = len(right_child) / len(parent)
        
        if self.criterion == 'gini':
            gain = self._gini(parent) - (
                weight_left * self._gini(left_child) +
                weight_right * self._gini(right_child)
            )
        else:  # entropy
            gain = self._entropy(parent) - (
                weight_left * self._entropy(left_child) +
                weight_right * self._entropy(right_child)
            )
        return gain
    
    def _best_split(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> Tuple[Optional[int], Optional[float], Optional[float]]:
        """Find the best split for the data."""
        best_gain = -1
        best_feature = None
        best_threshold = None
        
        n_features = X.shape[1]
        parent_gain = (
            self._gini(y) if self.criterion == 'gini' else self._entropy(y)
        )
        
        for feature in range(n_features):
            X_column = X[:, feature]
            thresholds = np.unique(X_column)
            
            for threshold in thresholds:
                left_idx = X_column <= threshold
                right_idx = ~left_idx
                
                if (
                    np.sum(left_idx) < self.min_samples_leaf or
                    np.sum(right_idx) < self.min_samples_leaf
                ):
                    continue
                    
                gain = self._information_gain(
                    y,
                    y[left_idx],
                    y[right_idx]
                )
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
                    
        return best_feature, best_threshold, best_gain
    
    def _build_tree(
        self,
        X: np.ndarray,
        y: np.ndarray,
        depth: int = 0
    ) -> Node:
        """Build the decision tree recursively."""
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))
        
        # Check stopping criteria
        if (
            self.max_depth is not None and depth >= self.max_depth or
            n_labels == 1 or
            n_samples < self.min_samples_split
        ):
            leaf_value = Counter(y).most_common(1)[0][0]
            return Node(value=leaf_value)
            
        # Find best split
        best_feature, best_threshold, best_gain = self._best_split(X, y)
        
        # If no split found, create leaf node
        if best_feature is None:
            leaf_value = Counter(y).most_common(1)[0][0]
            return Node(value=leaf_value)
            
        # Create child nodes
        left_idx = X[:, best_feature] <= best_threshold
        right_idx = ~left_idx
        
        left_child = self._build_tree(
            X[left_idx],
            y[left_idx],
            depth + 1
        )
        right_child = self._build_tree(
            X[right_idx],
            y[right_idx],
            depth + 1
        )
        
        return Node(
            feature=best_feature,
            threshold=best_threshold,
            left=left_child,
            right=right_child
        )
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'DecisionTreeClassifier':
        """Fit the model to the data."""
        X = np.asarray(X)
        y = np.asarray(y)
        
        if self.random_state is not None:
            np.random.seed(self.random_state)
            
        self.root = self._build_tree(X, y)
        return self
    
    def _traverse_tree(self, x: np.ndarray, node: Node) -> int:
        """Traverse the tree to make a prediction."""
        if node.value is not None:
            return node.value
            
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        X = np.asarray(X)
        return np.array([
            self._traverse_tree(x, self.root) for x in X
        ])

class DecisionTreeRegressor:
    """Decision Tree Regressor.
    
    Parameters
    ----------
    max_depth : Optional[int], default=None
        Maximum depth of the tree
    min_samples_split : int, default=2
        Minimum number of samples required to split a node
    min_samples_leaf : int, default=1
        Minimum number of samples required at each leaf node
    criterion : str, default='mse'
        Function to measure the quality of a split ('mse' or 'mae')
    random_state : Optional[int], default=None
        Random seed for reproducibility
    """
    
    def __init__(
        self,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        criterion: str = 'mse',
        random_state: Optional[int] = None
    ):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.random_state = random_state
        self.root = None
        
    def _mse(self, y: np.ndarray) -> float:
        """Calculate mean squared error."""
        return np.mean((y - np.mean(y)) ** 2)
    
    def _mae(self, y: np.ndarray) -> float:
        """Calculate mean absolute error."""
        return np.mean(np.abs(y - np.median(y)))
    
    def _best_split(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> Tuple[Optional[int], Optional[float], Optional[float]]:
        """Find the best split for the data."""
        best_gain = -1
        best_feature = None
        best_threshold = None
        
        n_features = X.shape[1]
        parent_error = (
            self._mse(y) if self.criterion == 'mse' else self._mae(y)
        )
        
        for feature in range(n_features):
            X_column = X[:, feature]
            thresholds = np.unique(X_column)
            
            for threshold in thresholds:
                left_idx = X_column <= threshold
                right_idx = ~left_idx
                
                if (
                    np.sum(left_idx) < self.min_samples_leaf or
                    np.sum(right_idx) < self.min_samples_leaf
                ):
                    continue
                    
                left_error = (
                    self._mse(y[left_idx])
                    if self.criterion == 'mse'
                    else self._mae(y[left_idx])
                )
                right_error = (
                    self._mse(y[right_idx])
                    if self.criterion == 'mse'
                    else self._mae(y[right_idx])
                )
                
                gain = parent_error - (
                    len(y[left_idx]) / len(y) * left_error +
                    len(y[right_idx]) / len(y) * right_error
                )
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
                    
        return best_feature, best_threshold, best_gain
    
    def _build_tree(
        self,
        X: np.ndarray,
        y: np.ndarray,
        depth: int = 0
    ) -> Node:
        """Build the decision tree recursively."""
        n_samples, n_features = X.shape
        
        # Check stopping criteria
        if (
            self.max_depth is not None and depth >= self.max_depth or
            n_samples < self.min_samples_split or
            len(np.unique(y)) == 1
        ):
            leaf_value = (
                np.mean(y) if self.criterion == 'mse' else np.median(y)
            )
            return Node(value=leaf_value)
            
        # Find best split
        best_feature, best_threshold, best_gain = self._best_split(X, y)
        
        # If no split found, create leaf node
        if best_feature is None:
            leaf_value = (
                np.mean(y) if self.criterion == 'mse' else np.median(y)
            )
            return Node(value=leaf_value)
            
        # Create child nodes
        left_idx = X[:, best_feature] <= best_threshold
        right_idx = ~left_idx
        
        left_child = self._build_tree(
            X[left_idx],
            y[left_idx],
            depth + 1
        )
        right_child = self._build_tree(
            X[right_idx],
            y[right_idx],
            depth + 1
        )
        
        return Node(
            feature=best_feature,
            threshold=best_threshold,
            left=left_child,
            right=right_child
        )
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'DecisionTreeRegressor':
        """Fit the model to the data."""
        X = np.asarray(X)
        y = np.asarray(y)
        
        if self.random_state is not None:
            np.random.seed(self.random_state)
            
        self.root = self._build_tree(X, y)
        return self
    
    def _traverse_tree(self, x: np.ndarray, node: Node) -> float:
        """Traverse the tree to make a prediction."""
        if node.value is not None:
            return node.value
            
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values."""
        X = np.asarray(X)
        return np.array([
            self._traverse_tree(x, self.root) for x in X
        ])

class RandomForestClassifier:
    """Random Forest Classifier.
    
    Parameters
    ----------
    n_estimators : int, default=100
        Number of trees in the forest
    max_depth : Optional[int], default=None
        Maximum depth of each tree
    min_samples_split : int, default=2
        Minimum number of samples required to split a node
    min_samples_leaf : int, default=1
        Minimum number of samples required at each leaf node
    criterion : str, default='gini'
        Function to measure the quality of a split ('gini' or 'entropy')
    random_state : Optional[int], default=None
        Random seed for reproducibility
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        criterion: str = 'gini',
        random_state: Optional[int] = None
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.random_state = random_state
        self.trees = []
        
    def _bootstrap_sample(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create a bootstrap sample of the data."""
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, size=n_samples, replace=True)
        return X[idxs], y[idxs]
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RandomForestClassifier':
        """Fit the model to the data."""
        X = np.asarray(X)
        y = np.asarray(y)
        
        if self.random_state is not None:
            np.random.seed(self.random_state)
            
        self.trees = []
        for _ in range(self.n_estimators):
            tree = DecisionTreeClassifier(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf,
                criterion=self.criterion
            )
            X_sample, y_sample = self._bootstrap_sample(X, y)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)
            
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        X = np.asarray(X)
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        return np.array([
            Counter(predictions).most_common(1)[0][0]
            for predictions in tree_predictions.T
        ])

class RandomForestRegressor:
    """Random Forest Regressor.
    
    Parameters
    ----------
    n_estimators : int, default=100
        Number of trees in the forest
    max_depth : Optional[int], default=None
        Maximum depth of each tree
    min_samples_split : int, default=2
        Minimum number of samples required to split a node
    min_samples_leaf : int, default=1
        Minimum number of samples required at each leaf node
    criterion : str, default='mse'
        Function to measure the quality of a split ('mse' or 'mae')
    random_state : Optional[int], default=None
        Random seed for reproducibility
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        criterion: str = 'mse',
        random_state: Optional[int] = None
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.random_state = random_state
        self.trees = []
        
    def _bootstrap_sample(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create a bootstrap sample of the data."""
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, size=n_samples, replace=True)
        return X[idxs], y[idxs]
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RandomForestRegressor':
        """Fit the model to the data."""
        X = np.asarray(X)
        y = np.asarray(y)
        
        if self.random_state is not None:
            np.random.seed(self.random_state)
            
        self.trees = []
        for _ in range(self.n_estimators):
            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf,
                criterion=self.criterion
            )
            X_sample, y_sample = self._bootstrap_sample(X, y)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)
            
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values."""
        X = np.asarray(X)
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        return np.mean(tree_predictions, axis=0) 
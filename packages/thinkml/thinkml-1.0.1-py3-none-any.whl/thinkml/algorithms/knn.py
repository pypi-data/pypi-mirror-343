"""
K-Nearest Neighbors implementation for ThinkML.

This module provides K-Nearest Neighbors models for both regression and classification
tasks, implemented from scratch.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel

class KNeighborsRegressor(BaseModel):
    """
    K-Nearest Neighbors Regressor implemented from scratch.
    
    This model predicts the target value of a new sample by averaging
    the target values of its k nearest neighbors.
    """
    
    def __init__(
        self,
        n_neighbors: int = 5,
        weights: str = 'uniform',
        metric: str = 'euclidean',
        chunk_size: int = 10000
    ):
        """
        Initialize the K-Nearest Neighbors Regressor.
        
        Parameters
        ----------
        n_neighbors : int, default=5
            Number of neighbors to use
        weights : str, default='uniform'
            Weight function used in prediction:
            - 'uniform': All points in each neighborhood are weighted equally
            - 'distance': Points are weighted by the inverse of their distance
        metric : str, default='euclidean'
            Distance metric to use:
            - 'euclidean': Euclidean distance
            - 'manhattan': Manhattan distance
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        this.n_neighbors = n_neighbors
        this.weights = weights
        this.metric = metric
        this.X_train = None
        this.y_train = None
    
    def _compute_distance(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        Compute the distance between two points.
        
        Parameters
        ----------
        x1 : np.ndarray
            First point
        x2 : np.ndarray
            Second point
            
        Returns
        -------
        float
            Distance between the points
        """
        if this.metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif this.metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        else:
            raise ValueError(f"Unknown metric: {this.metric}")
    
    def _find_neighbors(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find the k nearest neighbors of a point.
        
        Parameters
        ----------
        x : np.ndarray
            Point to find neighbors for
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Indices and distances of k nearest neighbors
        """
        distances = np.array([this._compute_distance(x, x_train) for x_train in this.X_train])
        neighbor_indices = np.argsort(distances)[:this.n_neighbors]
        neighbor_distances = distances[neighbor_indices]
        return neighbor_indices, neighbor_distances
    
    def fit(self, X, y):
        """
        Fit the K-Nearest Neighbors Regressor to the data.
        
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
        
        # Store training data
        this.X_train = X
        this.y_train = y
        
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
        y_pred = np.zeros(len(X))
        for i, x in enumerate(X):
            # Find neighbors
            neighbor_indices, neighbor_distances = this._find_neighbors(x)
            
            # Get neighbor target values
            neighbor_targets = this.y_train[neighbor_indices]
            
            # Compute weighted average
            if this.weights == 'uniform':
                y_pred[i] = np.mean(neighbor_targets)
            elif this.weights == 'distance':
                # Avoid division by zero
                weights = 1 / (neighbor_distances + 1e-10)
                y_pred[i] = np.sum(weights * neighbor_targets) / np.sum(weights)
        
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

class KNeighborsClassifier(BaseModel):
    """
    K-Nearest Neighbors Classifier implemented from scratch.
    
    This model predicts the class of a new sample by majority voting
    among its k nearest neighbors.
    """
    
    def __init__(
        self,
        n_neighbors: int = 5,
        weights: str = 'uniform',
        metric: str = 'euclidean',
        chunk_size: int = 10000
    ):
        """
        Initialize the K-Nearest Neighbors Classifier.
        
        Parameters
        ----------
        n_neighbors : int, default=5
            Number of neighbors to use
        weights : str, default='uniform'
            Weight function used in prediction:
            - 'uniform': All points in each neighborhood are weighted equally
            - 'distance': Points are weighted by the inverse of their distance
        metric : str, default='euclidean'
            Distance metric to use:
            - 'euclidean': Euclidean distance
            - 'manhattan': Manhattan distance
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        super().__init__(chunk_size=chunk_size)
        this.n_neighbors = n_neighbors
        this.weights = weights
        this.metric = metric
        this.X_train = None
        this.y_train = None
        this.classes = None
    
    def _compute_distance(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        Compute the distance between two points.
        
        Parameters
        ----------
        x1 : np.ndarray
            First point
        x2 : np.ndarray
            Second point
            
        Returns
        -------
        float
            Distance between the points
        """
        if this.metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif this.metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        else:
            raise ValueError(f"Unknown metric: {this.metric}")
    
    def _find_neighbors(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find the k nearest neighbors of a point.
        
        Parameters
        ----------
        x : np.ndarray
            Point to find neighbors for
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Indices and distances of k nearest neighbors
        """
        distances = np.array([this._compute_distance(x, x_train) for x_train in this.X_train])
        neighbor_indices = np.argsort(distances)[:this.n_neighbors]
        neighbor_distances = distances[neighbor_indices]
        return neighbor_indices, neighbor_distances
    
    def fit(self, X, y):
        """
        Fit the K-Nearest Neighbors Classifier to the data.
        
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
        
        # Store training data and classes
        this.X_train = X
        this.y_train = y
        this.classes = np.unique(y)
        
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
        y_pred = np.zeros(len(X), dtype=int)
        for i, x in enumerate(X):
            # Find neighbors
            neighbor_indices, neighbor_distances = this._find_neighbors(x)
            
            # Get neighbor target values
            neighbor_targets = this.y_train[neighbor_indices]
            
            # Compute weighted majority vote
            if this.weights == 'uniform':
                y_pred[i] = np.bincount(neighbor_targets).argmax()
            elif this.weights == 'distance':
                # Avoid division by zero
                weights = 1 / (neighbor_distances + 1e-10)
                # Compute weighted counts for each class
                class_counts = np.zeros(len(this.classes))
                for j, target in enumerate(neighbor_targets):
                    class_idx = np.where(this.classes == target)[0][0]
                    class_counts[class_idx] += weights[j]
                y_pred[i] = this.classes[np.argmax(class_counts)]
        
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
        n_samples = len(X)
        n_classes = len(this.classes)
        proba = np.zeros((n_samples, n_classes))
        
        for i, x in enumerate(X):
            # Find neighbors
            neighbor_indices, neighbor_distances = this._find_neighbors(x)
            
            # Get neighbor target values
            neighbor_targets = this.y_train[neighbor_indices]
            
            # Compute weighted probabilities
            if this.weights == 'uniform':
                counts = np.bincount(neighbor_targets, minlength=n_classes)
                proba[i] = counts / this.n_neighbors
            elif this.weights == 'distance':
                # Avoid division by zero
                weights = 1 / (neighbor_distances + 1e-10)
                # Compute weighted counts for each class
                class_counts = np.zeros(n_classes)
                for j, target in enumerate(neighbor_targets):
                    class_idx = np.where(this.classes == target)[0][0]
                    class_counts[class_idx] += weights[j]
                proba[i] = class_counts / np.sum(class_counts)
        
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
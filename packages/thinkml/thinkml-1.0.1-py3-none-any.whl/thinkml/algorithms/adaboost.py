"""
AdaBoost implementation for ThinkML.

This module provides AdaBoost models for both regression and classification
tasks, implemented from scratch.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da
from .base import BaseModel
from .decision_tree import DecisionTreeRegressor, DecisionTreeClassifier

class AdaBoostRegressor(BaseModel):
    """
    AdaBoost Regressor implemented from scratch.
    
    This model builds an ensemble of decision trees for regression tasks,
    using AdaBoost.R2 algorithm.
    """
    
    def __init__(
        self,
        n_estimators: int = 50,
        learning_rate: float = 1.0,
        max_depth: int = 3,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        chunk_size: int = 10000
    ):
        """
        Initialize the AdaBoost Regressor.
        
        Parameters
        ----------
        n_estimators : int, default=50
            Number of boosting stages to perform
        learning_rate : float, default=1.0
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
        this.estimators = []
        this.estimator_weights = []
    
    def _compute_sample_weights(self, errors: np.ndarray) -> np.ndarray:
        """
        Compute sample weights for the next iteration.
        
        Parameters
        ----------
        errors : np.ndarray
            Absolute errors for each sample
            
        Returns
        -------
        np.ndarray
            Sample weights
        """
        # Normalize errors to [0, 1]
        max_error = np.max(errors)
        if max_error == 0:
            return np.ones_like(errors) / len(errors)
        
        normalized_errors = errors / max_error
        
        # Compute weights
        weights = normalized_errors ** 2
        
        # Normalize weights
        return weights / np.sum(weights)
    
    def fit(self, X, y):
        """
        Fit the AdaBoost Regressor to the data.
        
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
        
        # Initialize sample weights
        sample_weights = np.ones(len(X)) / len(X)
        
        # Build ensemble
        this.estimators = []
        this.estimator_weights = []
        
        for _ in range(this.n_estimators):
            # Fit a tree with current sample weights
            estimator = DecisionTreeRegressor(
                max_depth=this.max_depth,
                min_samples_split=this.min_samples_split,
                min_samples_leaf=this.min_samples_leaf
            )
            estimator.fit(X, y, sample_weight=sample_weights)
            this.estimators.append(estimator)
            
            # Make predictions
            y_pred = estimator.predict(X)
            
            # Compute errors
            errors = np.abs(y - y_pred)
            
            # Compute estimator weight
            estimator_weight = this.learning_rate * (1.0 / (1.0 + np.mean(errors)))
            this.estimator_weights.append(estimator_weight)
            
            # Update sample weights
            sample_weights = this._compute_sample_weights(errors)
        
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
        y_pred = np.zeros(len(X))
        
        # Add weighted predictions from each estimator
        for estimator, weight in zip(this.estimators, this.estimator_weights):
            y_pred += weight * estimator.predict(X)
        
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

class AdaBoostClassifier(BaseModel):
    """
    AdaBoost Classifier implemented from scratch.
    
    This model builds an ensemble of decision trees for classification tasks,
    using AdaBoost.M1 algorithm.
    """
    
    def __init__(
        self,
        n_estimators: int = 50,
        learning_rate: float = 1.0,
        max_depth: int = 3,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        chunk_size: int = 10000
    ):
        """
        Initialize the AdaBoost Classifier.
        
        Parameters
        ----------
        n_estimators : int, default=50
            Number of boosting stages to perform
        learning_rate : float, default=1.0
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
        this.estimators = []
        this.estimator_weights = []
        this.classes = None
    
    def _compute_sample_weights(self, errors: np.ndarray, current_weights: np.ndarray) -> np.ndarray:
        """
        Compute sample weights for the next iteration.
        
        Parameters
        ----------
        errors : np.ndarray
            Binary errors for each sample (0 for correct, 1 for incorrect)
        current_weights : np.ndarray
            Current sample weights
            
        Returns
        -------
        np.ndarray
            Updated sample weights
        """
        # Compute new weights
        new_weights = current_weights * np.exp(this.learning_rate * errors)
        
        # Normalize weights
        return new_weights / np.sum(new_weights)
    
    def fit(self, X, y):
        """
        Fit the AdaBoost Classifier to the data.
        
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
        
        # Initialize sample weights
        sample_weights = np.ones(len(X)) / len(X)
        
        # Build ensemble
        this.estimators = []
        this.estimator_weights = []
        
        for _ in range(this.n_estimators):
            # Fit a tree with current sample weights
            estimator = DecisionTreeClassifier(
                max_depth=this.max_depth,
                min_samples_split=this.min_samples_split,
                min_samples_leaf=this.min_samples_leaf
            )
            estimator.fit(X, y, sample_weight=sample_weights)
            this.estimators.append(estimator)
            
            # Make predictions
            y_pred = estimator.predict(X)
            
            # Compute errors
            errors = (y_pred != y).astype(int)
            
            # Compute weighted error
            weighted_error = np.sum(sample_weights * errors)
            
            # Skip if perfect prediction
            if weighted_error == 0:
                this.estimator_weights.append(1.0)
                break
            
            # Compute estimator weight
            estimator_weight = this.learning_rate * 0.5 * np.log((1 - weighted_error) / weighted_error)
            this.estimator_weights.append(estimator_weight)
            
            # Update sample weights
            sample_weights = this._compute_sample_weights(errors, sample_weights)
        
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
        n_samples = len(X)
        n_classes = len(this.classes)
        predictions = np.zeros((n_samples, n_classes))
        
        # Add weighted predictions from each estimator
        for estimator, weight in zip(this.estimators, this.estimator_weights):
            y_pred = estimator.predict(X)
            for i, class_label in enumerate(this.classes):
                predictions[y_pred == class_label, i] += weight
        
        # Get final predictions
        y_pred = this.classes[np.argmax(predictions, axis=1)]
        
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
        n_samples = len(X)
        n_classes = len(this.classes)
        predictions = np.zeros((n_samples, n_classes))
        
        # Add weighted predictions from each estimator
        for estimator, weight in zip(this.estimators, this.estimator_weights):
            y_pred = estimator.predict(X)
            for i, class_label in enumerate(this.classes):
                predictions[y_pred == class_label, i] += weight
        
        # Normalize to get probabilities
        row_sums = predictions.sum(axis=1)
        proba = predictions / row_sums[:, np.newaxis]
        
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
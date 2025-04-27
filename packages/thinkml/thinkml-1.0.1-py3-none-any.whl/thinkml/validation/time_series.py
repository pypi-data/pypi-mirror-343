"""
Time series validation techniques for ThinkML.
"""

import numpy as np
from sklearn.base import BaseEstimator, clone
from sklearn.metrics import make_scorer

class TimeSeriesValidator:
    """Time series cross-validation with expanding window."""
    
    def __init__(self, n_splits=5, min_train_size=None, test_size=None,
                 gap=0, scoring='neg_mean_squared_error'):
        """
        Initialize time series validator.
        
        Parameters:
        -----------
        n_splits : int, default=5
            Number of splits for cross-validation
        min_train_size : int or None, default=None
            Minimum size of the training set
        test_size : int or None, default=None
            Size of the test set
        gap : int, default=0
            Number of samples to exclude between training and test sets
        scoring : string, callable, or None, default='neg_mean_squared_error'
            Scoring metric to use
        """
        self.n_splits = n_splits
        self.min_train_size = min_train_size
        self.test_size = test_size
        self.gap = gap
        self.scoring = scoring
        
    def split(self, X, y=None, groups=None):
        """
        Generate indices to split data into training and test sets.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,), default=None
            Target values
        groups : array-like of shape (n_samples,), default=None
            Group labels for samples
        """
        n_samples = len(X)
        
        # Determine sizes
        if self.test_size is None:
            test_size = n_samples // (self.n_splits + 1)
        else:
            test_size = self.test_size
            
        if self.min_train_size is None:
            min_train_size = test_size
        else:
            min_train_size = self.min_train_size
            
        # Generate splits
        test_starts = np.linspace(min_train_size,
                                n_samples - test_size,
                                self.n_splits,
                                dtype=int)
        
        for test_start in test_starts:
            train_end = test_start - self.gap
            test_end = test_start + test_size
            
            if test_end > n_samples:
                continue
                
            yield np.arange(train_end), np.arange(test_start, test_end)
            
    def validate(self, estimator, X, y):
        """
        Validate estimator using time series cross-validation.
        
        Parameters:
        -----------
        estimator : estimator object
            Estimator to validate
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        scores = []
        predictions = np.zeros_like(y)
        
        for train_idx, test_idx in self.split(X, y):
            # Get train/test split
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Fit and evaluate
            estimator_clone = clone(estimator)
            estimator_clone.fit(X_train, y_train)
            
            # Score
            score = self._score(estimator_clone, X_test, y_test)
            scores.append(score)
            
            # Store predictions
            predictions[test_idx] = estimator_clone.predict(X_test)
            
        return {
            'scores': np.array(scores),
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
            'predictions': predictions
        }
        
    def _score(self, estimator, X, y):
        """Compute score for estimator."""
        if callable(self.scoring):
            return self.scoring(estimator, X, y)
        elif isinstance(self.scoring, str):
            scorer = make_scorer(self.scoring)
            return scorer(estimator, X, y)
        else:
            raise ValueError("scoring must be callable or string") 
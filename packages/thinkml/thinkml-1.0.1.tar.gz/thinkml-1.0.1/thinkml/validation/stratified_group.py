"""
Stratified group validation techniques for ThinkML.
"""

import numpy as np
from sklearn.base import BaseEstimator, clone
from sklearn.metrics import make_scorer
from sklearn.model_selection import StratifiedKFold

class StratifiedGroupValidator:
    """Stratified group cross-validation."""
    
    def __init__(self, n_splits=5, shuffle=True, random_state=None,
                 scoring='accuracy'):
        """
        Initialize stratified group validator.
        
        Parameters:
        -----------
        n_splits : int, default=5
            Number of splits for cross-validation
        shuffle : bool, default=True
            Whether to shuffle the data before splitting
        random_state : int or None, default=None
            Random state for reproducibility
        scoring : string, callable, or None, default='accuracy'
            Scoring metric to use
        """
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state
        self.scoring = scoring
        
    def split(self, X, y, groups):
        """
        Generate indices to split data into training and test sets.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        groups : array-like of shape (n_samples,)
            Group labels for samples
        """
        X = np.asarray(X)
        y = np.asarray(y)
        groups = np.asarray(groups)
        
        # Get unique groups and their indices
        unique_groups = np.unique(groups)
        group_indices = {g: np.where(groups == g)[0] for g in unique_groups}
        
        # Get group labels and counts
        group_y = np.array([np.mean(y[group_indices[g]]) for g in unique_groups])
        group_sizes = np.array([len(group_indices[g]) for g in unique_groups])
        
        # Create stratified k-fold for groups
        skf = StratifiedKFold(n_splits=self.n_splits,
                            shuffle=self.shuffle,
                            random_state=self.random_state)
        
        # Split groups
        for train_groups, test_groups in skf.split(unique_groups,
                                                 group_y > np.median(group_y)):
            # Get sample indices for each fold
            train_idx = np.concatenate([group_indices[g] for g in unique_groups[train_groups]])
            test_idx = np.concatenate([group_indices[g] for g in unique_groups[test_groups]])
            
            yield train_idx, test_idx
            
    def validate(self, estimator, X, y, groups):
        """
        Validate estimator using stratified group cross-validation.
        
        Parameters:
        -----------
        estimator : estimator object
            Estimator to validate
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        groups : array-like of shape (n_samples,)
            Group labels for samples
        """
        X = np.asarray(X)
        y = np.asarray(y)
        groups = np.asarray(groups)
        
        scores = []
        predictions = np.zeros_like(y)
        
        for train_idx, test_idx in self.split(X, y, groups):
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
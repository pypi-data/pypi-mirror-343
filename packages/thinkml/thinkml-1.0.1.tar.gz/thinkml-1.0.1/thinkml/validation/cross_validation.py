"""
Cross-validation techniques for ThinkML.
"""

import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.base import BaseEstimator, clone
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from typing import Dict, List, Union, Any, Optional
import pandas as pd

class NestedCrossValidator:
    """Nested cross-validation for model selection and evaluation."""
    
    def __init__(self, estimator=None, param_grid=None, outer_cv=5, inner_cv=3,
                 scoring='accuracy', refit=True, n_jobs=None):
        """
        Initialize nested cross-validator.
        
        Parameters:
        -----------
        estimator : estimator object
            Base estimator to validate
        param_grid : dict or list of dicts
            Parameter grid to search
        outer_cv : int or cross-validation generator, default=5
            Cross-validation generator for outer loop
        inner_cv : int or cross-validation generator, default=3
            Cross-validation generator for inner loop
        scoring : string, callable, or None, default='accuracy'
            Scoring metric to use
        refit : bool, default=True
            Whether to refit the estimator on the entire dataset
        n_jobs : int or None, default=None
            Number of jobs to run in parallel
        """
        self.estimator = estimator
        self.param_grid = param_grid
        self.outer_cv = outer_cv
        self.inner_cv = inner_cv
        self.scoring = scoring
        self.refit = refit
        self.n_jobs = n_jobs
        self.best_params_ = None
        self.best_score_ = None
        self.cv_results_ = None
        
    def fit(self, X, y, groups=None):
        """
        Fit the nested cross-validator.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        groups : array-like of shape (n_samples,), default=None
            Group labels for samples
            
        Returns:
        --------
        self : object
            Returns self.
        """
        if self.estimator is None:
            raise ValueError("estimator cannot be None")
        if self.param_grid is None:
            raise ValueError("param_grid cannot be None")
            
        # Convert to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Validate input dimensions
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
        if len(X) < 2:
            raise ValueError("Cannot perform cross-validation with less than 2 samples")
            
        # Check for NaN and infinite values
        if np.any(np.isnan(y)):
            raise ValueError("Target values contain NaN")
        if np.any(np.isinf(X)):
            raise ValueError("Features contain infinite values")
        
        # Create cross-validation generators
        if isinstance(self.outer_cv, int):
            if len(np.unique(y)) < 10:
                outer_cv = StratifiedKFold(n_splits=self.outer_cv, shuffle=True, random_state=42)
            else:
                outer_cv = KFold(n_splits=self.outer_cv, shuffle=True, random_state=42)
        else:
            outer_cv = self.outer_cv
            
        if isinstance(self.inner_cv, int):
            if len(np.unique(y)) < 10:
                inner_cv = StratifiedKFold(n_splits=self.inner_cv, shuffle=True, random_state=42)
            else:
                inner_cv = KFold(n_splits=self.inner_cv, shuffle=True, random_state=42)
        else:
            inner_cv = self.inner_cv
            
        # Initialize results storage
        outer_scores = []
        cv_results = []
        
        # Outer loop
        for train_idx, test_idx in outer_cv.split(X, y, groups):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Inner loop for model selection
            grid_search = GridSearchCV(
                estimator=clone(self.estimator),
                param_grid=self.param_grid,
                cv=inner_cv,
                scoring=self.scoring,
                n_jobs=self.n_jobs
            )
            grid_search.fit(X_train, y_train)
            
            # Store results
            cv_results.append({
                'params': grid_search.best_params_,
                'mean_score': grid_search.best_score_,
                'std_score': np.std(grid_search.cv_results_['mean_test_score'])
            })
            
            # Evaluate on test set
            best_model = grid_search.best_estimator_
            test_score = best_model.score(X_test, y_test)
            outer_scores.append(test_score)
        
        # Store results
        self.cv_results_ = cv_results
        self.best_score_ = np.mean(outer_scores)
        
        # Find overall best parameters
        best_idx = np.argmax([r['mean_score'] for r in cv_results])
        self.best_params_ = cv_results[best_idx]['params']
        
        # Refit on entire dataset if requested
        if self.refit:
            self.estimator = clone(self.estimator)
            self.estimator.set_params(**self.best_params_)
            self.estimator.fit(X, y)
        
        return self
        
    def predict(self, X):
        """
        Predict using the best estimator.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Samples
            
        Returns:
        --------
        array-like : Predictions
        """
        if not self.refit:
            raise ValueError("Must set refit=True to use predict")
        if self.estimator is None:
            raise ValueError("Must call fit before predict")
        return self.estimator.predict(X)
        
    def fit_predict(self, X, y, groups=None):
        """
        Fit the model and return cross-validation results.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        groups : array-like of shape (n_samples,), default=None
            Group labels for samples
            
        Returns:
        --------
        dict : Cross-validation results
        """
        self.fit(X, y, groups)
        return {
            'mean_score': self.best_score_,
            'std_score': np.std([r['mean_score'] for r in self.cv_results_]),
            'outer_scores': [r['mean_score'] for r in self.cv_results_],
            'best_params_list': [r['params'] for r in self.cv_results_]
        } 
"""
Advanced Validation Module for ThinkML.

This module provides advanced validation techniques for model evaluation.
"""

import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, TimeSeriesSplit
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.base import BaseEstimator, clone
from typing import Optional, Union, Dict, Any, List
import pandas as pd

class NestedCrossValidator:
    """
    Nested cross-validation for hyperparameter tuning and model evaluation.
    
    Parameters
    ----------
    estimator : estimator object
        The base estimator to use for nested cross-validation.
    param_grid : dict
        Dictionary with parameters names (string) as keys and lists of
        parameter settings to try as values.
    inner_cv : int, default=5
        Number of folds for inner cross-validation.
    outer_cv : int, default=5
        Number of folds for outer cross-validation.
    scoring : str, optional
        Scoring metric to use.
    n_jobs : int, default=None
        Number of jobs to run in parallel.
    """
    
    def __init__(
        self,
        estimator: BaseEstimator,
        param_grid: Dict[str, List[Any]],
        inner_cv: int = 5,
        outer_cv: int = 5,
        scoring: Optional[str] = None,
        n_jobs: Optional[int] = None
    ):
        self.estimator = estimator
        self.param_grid = param_grid
        self.inner_cv = inner_cv
        self.outer_cv = outer_cv
        self.scoring = scoring
        self.n_jobs = n_jobs
        
    def fit_predict(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series]
    ) -> Dict[str, Any]:
        """
        Perform nested cross-validation.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
            
        Returns
        -------
        dict
            Dictionary containing cross-validation results.
        """
        # Convert inputs to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Initialize cross-validation splits
        outer_cv_split = StratifiedKFold(
            n_splits=self.outer_cv,
            shuffle=True,
            random_state=42
        ) if len(np.unique(y)) < 10 else KFold(
            n_splits=self.outer_cv,
            shuffle=True,
            random_state=42
        )
        
        # Initialize results storage
        outer_scores = []
        best_params_list = []
        
        # Outer cross-validation loop
        for train_idx, test_idx in outer_cv_split.split(X, y):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Inner cross-validation for hyperparameter tuning
            inner_cv = StratifiedKFold(
                n_splits=self.inner_cv,
                shuffle=True,
                random_state=42
            ) if len(np.unique(y)) < 10 else KFold(
                n_splits=self.inner_cv,
                shuffle=True,
                random_state=42
            )
            
            # Create and fit GridSearchCV
            grid_search = GridSearchCV(
                estimator=clone(self.estimator),
                param_grid=self.param_grid,
                cv=inner_cv,
                scoring=self.scoring,
                n_jobs=self.n_jobs
            )
            grid_search.fit(X_train, y_train)
            
            # Store best parameters
            best_params_list.append(grid_search.best_params_)
            
            # Evaluate on test set
            best_model = grid_search.best_estimator_
            if self.scoring is None:
                score = best_model.score(X_test, y_test)
            else:
                from sklearn.metrics import get_scorer
                scorer = get_scorer(self.scoring)
                score = scorer(best_model, X_test, y_test)
            
            outer_scores.append(score)
        
        # Compute summary statistics
        results = {
            'mean_score': np.mean(outer_scores),
            'std_score': np.std(outer_scores),
            'outer_scores': outer_scores,
            'best_params_list': best_params_list
        }
        
        return results

class TimeSeriesValidator:
    """
    Time series cross-validation with optional gap between train and test sets.
    
    Parameters
    ----------
    n_splits : int, default=5
        Number of splits.
    test_size : float, default=0.2
        Proportion of the dataset to include in the test split.
    gap : int, default=0
        Number of samples to exclude from the end of each training set.
    scoring : str, optional
        Scoring metric to use.
    """
    
    def __init__(
        self,
        n_splits: int = 5,
        test_size: float = 0.2,
        gap: int = 0,
        scoring: Optional[str] = None
    ):
        self.n_splits = n_splits
        self.test_size = test_size
        self.gap = gap
        self.scoring = scoring
        
    def fit_predict(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
        estimator: BaseEstimator
    ) -> Dict[str, Any]:
        """
        Perform time series cross-validation.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
        estimator : estimator object
            The estimator to use for time series cross-validation.
            
        Returns
        -------
        dict
            Dictionary containing cross-validation results.
        """
        # Convert inputs to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Initialize time series split
        tscv = TimeSeriesSplit(
            n_splits=self.n_splits,
            gap=self.gap,
            test_size=int(len(X) * self.test_size)
        )
        
        # Initialize results storage
        scores = []
        predictions = []
        
        # Perform time series cross-validation
        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Fit model and make predictions
            model = clone(estimator)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            predictions.append(y_pred)
            
            # Compute score
            if self.scoring is None:
                score = model.score(X_test, y_test)
            else:
                from sklearn.metrics import get_scorer
                scorer = get_scorer(self.scoring)
                score = scorer(model, X_test, y_test)
            
            scores.append(score)
        
        # Compute summary statistics
        results = {
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
            'scores': scores,
            'predictions': predictions
        }
        
        return results

class StratifiedGroupValidator:
    """
    Stratified group cross-validation.
    
    Parameters
    ----------
    n_splits : int, default=5
        Number of splits.
    groups : array-like
        Group labels for the samples.
    scoring : str, optional
        Scoring metric to use.
    min_samples_per_split : int, default=1
        Minimum number of samples required for a split.
    """
    
    def __init__(
        self,
        n_splits: int = 5,
        groups: Optional[Union[np.ndarray, List]] = None,
        scoring: Optional[str] = None,
        min_samples_per_split: int = 1
    ):
        self.n_splits = n_splits
        self.groups = groups
        self.scoring = scoring
        self.min_samples_per_split = min_samples_per_split
        
    def fit_predict(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
        estimator: BaseEstimator
    ) -> Dict[str, Any]:
        """
        Perform stratified group cross-validation.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
        estimator : estimator object
            The estimator to use for cross-validation.
            
        Returns
        -------
        dict
            Dictionary containing cross-validation results.
        """
        # Convert inputs to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)
        groups = np.asarray(self.groups) if self.groups is not None else None
        
        # Validate inputs
        if len(X) < self.min_samples_per_split * self.n_splits:
            # Adjust n_splits if there are too few samples
            self.n_splits = max(2, len(X) // self.min_samples_per_split)
        
        # Initialize results storage
        scores = []
        predictions = []
        
        # Create group-wise stratified folds
        unique_groups = np.unique(groups) if groups is not None else np.arange(len(X))
        n_groups = len(unique_groups)
        
        # Use KFold for splitting groups
        group_kfold = KFold(n_splits=min(self.n_splits, n_groups), shuffle=True, random_state=42)
        
        # Perform cross-validation
        for train_group_idx, val_group_idx in group_kfold.split(unique_groups):
            # Get sample indices for each fold
            if groups is not None:
                train_idx = np.where(np.isin(groups, unique_groups[train_group_idx]))[0]
                val_idx = np.where(np.isin(groups, unique_groups[val_group_idx]))[0]
            else:
                train_idx = train_group_idx
                val_idx = val_group_idx
            
            # Split data
            X_train = X[train_idx]
            X_val = X[val_idx]
            y_train = y[train_idx]
            y_val = y[val_idx]
            
            # Skip if validation set is too small
            if len(y_val) < self.min_samples_per_split:
                continue
            
            # Fit and predict
            model = clone(estimator)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            
            # Store results
            if self.scoring is None:
                score = model.score(X_val, y_val)
            else:
                from sklearn.metrics import get_scorer
                scorer = get_scorer(self.scoring)
                score = scorer(model, X_val, y_val)
            
            scores.append(score)
            predictions.extend(y_pred)
        
        # Return results
        return {
            'mean_score': np.mean(scores) if scores else None,
            'std_score': np.std(scores) if scores else None,
            'scores': scores,
            'predictions': predictions
        }

class BootstrapValidator:
    """
    Bootstrap validation with optional stratification.
    
    Parameters
    ----------
    n_iterations : int, default=100
        Number of bootstrap iterations.
    sample_size : float, default=0.8
        Proportion of samples to include in each bootstrap.
    scoring : str, optional
        Scoring metric to use.
    stratify : bool, default=True
        Whether to stratify the bootstrap samples.
    """
    
    def __init__(
        self,
        n_iterations: int = 100,
        sample_size: float = 0.8,
        scoring: Optional[str] = None,
        stratify: bool = True
    ):
        self.n_iterations = n_iterations
        self.sample_size = sample_size
        self.scoring = scoring
        self.stratify = stratify
        
    def fit_predict(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
        estimator: BaseEstimator
    ) -> Dict[str, Any]:
        """
        Perform bootstrap validation.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
        estimator : estimator object
            The estimator to use for bootstrap validation.
            
        Returns
        -------
        dict
            Dictionary containing bootstrap results.
        """
        # Convert inputs to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Initialize results storage
        scores = []
        predictions = []
        
        n_samples = len(X)
        sample_size = int(n_samples * self.sample_size)
        
        for _ in range(self.n_iterations):
            # Generate bootstrap sample
            if self.stratify:
                bootstrap_idx = np.array([], dtype=int)
                for label in np.unique(y):
                    label_idx = np.where(y == label)[0]
                    label_size = int(len(label_idx) * self.sample_size)
                    bootstrap_idx = np.concatenate([
                        bootstrap_idx,
                        np.random.choice(label_idx, size=label_size, replace=True)
                    ])
            else:
                bootstrap_idx = np.random.choice(
                    n_samples,
                    size=sample_size,
                    replace=True
                )
            
            # Get out-of-bag indices
            oob_idx = np.array(list(set(range(n_samples)) - set(bootstrap_idx)))
            
            if len(oob_idx) > 0:
                X_train, X_test = X[bootstrap_idx], X[oob_idx]
                y_train, y_test = y[bootstrap_idx], y[oob_idx]
                
                # Fit model and make predictions
                model = clone(estimator)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                predictions.append(y_pred)
                
                # Compute score
                if self.scoring is None:
                    score = model.score(X_test, y_test)
                else:
                    from sklearn.metrics import get_scorer
                    scorer = get_scorer(self.scoring)
                    score = scorer(model, X_test, y_test)
                
                scores.append(score)
        
        # Compute summary statistics
        results = {
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
            'scores': scores,
            'predictions': predictions
        }
        
        return results 
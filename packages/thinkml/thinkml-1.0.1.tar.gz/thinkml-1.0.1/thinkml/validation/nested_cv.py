from sklearn.model_selection import KFold, ParameterGrid
import numpy as np
import pandas as pd
from typing import Dict, List, Union, Any

class NestedCrossValidator:
    def __init__(self, estimator, param_grid: Dict[str, List[Any]], 
                 outer_cv: int = 5, inner_cv: int = 3):
        """Initialize the nested cross-validator.
        
        Args:
            estimator: The estimator to use for nested CV
            param_grid: Dictionary with parameters names (string) as keys and lists of
                       parameter settings to try as values
            outer_cv: Number of folds for outer CV
            inner_cv: Number of folds for inner CV
        """
        self.estimator = estimator
        self.param_grid = param_grid
        self.outer_cv = KFold(n_splits=outer_cv, shuffle=True)
        self.inner_cv = KFold(n_splits=inner_cv, shuffle=True)
        
    def fit_predict(self, X: Union[pd.DataFrame, np.ndarray], 
                   y: Union[pd.Series, np.ndarray]) -> Dict[str, Any]:
        """Perform nested cross-validation.
        
        Args:
            X: Training data
            y: Target values
            
        Returns:
            Dictionary containing:
                - mean_score: Mean score across outer folds
                - std_score: Standard deviation of scores
                - outer_scores: List of scores for each outer fold
                - best_params_list: List of best parameters for each outer fold
        """
        outer_scores = []
        best_params_list = []
        
        for train_idx, test_idx in self.outer_cv.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
            # Inner CV for parameter tuning
            best_score = -np.inf
            best_params = None
            
            for params in ParameterGrid(self.param_grid):
                scores = []
                for inner_train_idx, inner_val_idx in self.inner_cv.split(X_train):
                    X_inner_train = X_train.iloc[inner_train_idx]
                    X_inner_val = X_train.iloc[inner_val_idx]
                    y_inner_train = y_train.iloc[inner_train_idx]
                    y_inner_val = y_train.iloc[inner_val_idx]
                    
                    # Clone and fit model
                    model = clone(self.estimator)
                    model.set_params(**params)
                    model.fit(X_inner_train, y_inner_train)
                    score = model.score(X_inner_val, y_inner_val)
                    scores.append(score)
                
                mean_score = np.mean(scores)
                if mean_score > best_score:
                    best_score = mean_score
                    best_params = params
            
            # Train on full training set with best parameters
            best_model = clone(self.estimator)
            best_model.set_params(**best_params)
            best_model.fit(X_train, y_train)
            outer_score = best_model.score(X_test, y_test)
            
            outer_scores.append(outer_score)
            best_params_list.append(best_params)
        
        return {
            'mean_score': np.mean(outer_scores),
            'std_score': np.std(outer_scores),
            'outer_scores': outer_scores,
            'best_params_list': best_params_list
        } 
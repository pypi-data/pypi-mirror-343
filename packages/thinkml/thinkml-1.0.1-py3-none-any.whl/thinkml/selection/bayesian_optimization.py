"""
Bayesian optimization techniques for ThinkML.
"""

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from scipy.stats import norm
from scipy.optimize import minimize
from skopt import BayesSearchCV
from typing import Dict, Any, Union
import pandas as pd

class BayesianOptimizer:
    """Bayesian optimization for hyperparameter tuning."""
    
    def __init__(self, estimator: BaseEstimator,
                 param_space: Dict[str, Any],
                 n_trials: int = 50,
                 cv: int = 5,
                 n_jobs: int = -1,
                 scoring: str = 'neg_mean_squared_error'):
        """Initialize the Bayesian optimizer.
        
        Args:
            estimator: The estimator to optimize
            param_space: Dictionary of parameter names and their search spaces
            n_trials: Number of trials for optimization
            cv: Number of cross-validation folds
            n_jobs: Number of parallel jobs
            scoring: Scoring metric to optimize
        """
        self.estimator = estimator
        self.param_space = param_space
        self.n_trials = n_trials
        self.cv = cv
        self.n_jobs = n_jobs
        self.scoring = scoring
        
        self.optimizer = BayesSearchCV(
            estimator=estimator,
            search_spaces=param_space,
            n_iter=n_trials,
            cv=cv,
            n_jobs=n_jobs,
            scoring=scoring,
            random_state=42
        )
        
    def fit(self, X: Union[pd.DataFrame, np.ndarray], 
            y: Union[pd.Series, np.ndarray]) -> 'BayesianOptimizer':
        """Fit the optimizer to find best parameters.
        
        Args:
            X: Training data
            y: Target values
            
        Returns:
            self
        """
        self.optimizer.fit(X, y)
        return self
        
    def get_best_params(self) -> Dict[str, Any]:
        """Get the best parameters found.
        
        Returns:
            Dictionary of best parameters
        """
        return self.optimizer.best_params_
        
    def get_best_score(self) -> float:
        """Get the best score achieved.
        
        Returns:
            Best score
        """
        return -self.optimizer.best_score_  # Convert back from neg_mean_squared_error
        
    def _sample_random_point(self):
        """Sample random point from parameter space."""
        point = {}
        for param, (low, high) in self.param_space.items():
            point[param] = self.rng.uniform(low, high)
        return point
        
    def _acquisition(self, X):
        """Compute acquisition function."""
        mean, std = self.gp.predict(X.reshape(-1, len(self.param_space)), return_std=True)
        
        if self.acquisition_func == 'ei':
            # Expected Improvement
            imp = mean - self.best_score_
            Z = imp / (std + 1e-8)
            ei = imp * norm.cdf(Z) + std * norm.pdf(Z)
            return ei
        elif self.acquisition_func == 'pi':
            # Probability of Improvement
            Z = (mean - self.best_score_) / (std + 1e-8)
            return norm.cdf(Z)
        else:  # Upper Confidence Bound
            return mean + 2 * std
            
    def _next_point(self):
        """Get next point to evaluate."""
        bounds = [(low, high) for low, high in self.param_space.values()]
        
        def objective(x):
            return -self._acquisition(x)
            
        # Try multiple random starts
        best_x = None
        best_acquisition_value = -np.inf
        
        for _ in range(10):
            x0 = [self.rng.uniform(low, high) for low, high in bounds]
            result = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')
            
            if result.fun < best_acquisition_value:
                best_acquisition_value = result.fun
                best_x = result.x
                
        return {param: value for param, value in zip(self.param_space.keys(), best_x)}
        
    def optimize(self, objective_func):
        """
        Run Bayesian optimization.
        
        Parameters:
        -----------
        objective_func : callable
            Function to optimize that takes parameters as input and returns score
        """
        # Initial random points
        for _ in range(self.n_initial_points):
            params = self._sample_random_point()
            score = objective_func(**params)
            
            self.X.append(list(params.values()))
            self.y.append(score)
            
        self.X = np.array(self.X)
        self.y = np.array(self.y)
        
        # Update best score
        best_idx = np.argmax(self.y)
        self.best_score_ = self.y[best_idx]
        self.best_params_ = {
            param: self.X[best_idx, i]
            for i, param in enumerate(self.param_space.keys())
        }
        
        # Main optimization loop
        for _ in range(self.n_iter - self.n_initial_points):
            # Fit GP
            self.gp.fit(self.X, self.y)
            
            # Get next point
            next_params = self._next_point()
            
            # Evaluate point
            score = objective_func(**next_params)
            
            # Update data
            self.X = np.vstack((self.X, list(next_params.values())))
            self.y = np.append(self.y, score)
            
            # Update best score
            if score > self.best_score_:
                self.best_score_ = score
                self.best_params_ = next_params
                
        return self 
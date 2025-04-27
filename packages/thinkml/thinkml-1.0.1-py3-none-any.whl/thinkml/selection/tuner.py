"""
Hyperparameter tuning and model selection functionality.
"""

import numpy as np
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from itertools import product
import random
from scipy.stats import norm
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ParameterGrid:
    """Parameter grid for hyperparameter tuning."""
    param_grid: Dict[str, List[Any]]
    
    def __iter__(self):
        """Generate all combinations of parameters."""
        keys = self.param_grid.keys()
        values = self.param_grid.values()
        for instance in product(*values):
            yield dict(zip(keys, instance))

def _evaluate_params(
    model: Any,
    params: Dict[str, Any],
    X: np.ndarray,
    y: np.ndarray,
    cv: int,
    scoring: Callable[[np.ndarray, np.ndarray], float]
) -> float:
    """
    Evaluate model with given parameters using cross-validation.
    
    Parameters
    ----------
    model : Any
        Model to evaluate
    params : Dict[str, Any]
        Model parameters
    X : np.ndarray
        Training data
    y : np.ndarray
        Target values
    cv : int
        Number of cross-validation folds
    scoring : Callable
        Scoring function
        
    Returns
    -------
    float
        Mean score across folds
    """
    # Set model parameters
    for param, value in params.items():
        setattr(model, param, value)
    
    # Perform cross-validation
    n_samples = len(X)
    fold_size = n_samples // cv
    scores = []
    
    for i in range(cv):
        # Create train and validation indices
        val_start = i * fold_size
        val_end = val_start + fold_size if i < cv - 1 else n_samples
        val_indices = np.arange(val_start, val_end)
        train_indices = np.concatenate([
            np.arange(0, val_start),
            np.arange(val_end, n_samples)
        ])
        
        # Split data
        X_train, X_val = X[train_indices], X[val_indices]
        y_train, y_val = y[train_indices], y[val_indices]
        
        # Fit and evaluate
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        score = scoring(y_val, y_pred)
        scores.append(score)
    
    return np.mean(scores)

def grid_search(
    model: Any,
    param_grid: Dict[str, List[Any]],
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5,
    scoring: Optional[Callable[[np.ndarray, np.ndarray], float]] = None
) -> Tuple[Dict[str, Any], float]:
    """
    Perform grid search for hyperparameter tuning.
    
    Parameters
    ----------
    model : Any
        Model to tune
    param_grid : Dict[str, List[Any]]
        Parameter grid to search
    X : np.ndarray
        Training data
    y : np.ndarray
        Target values
    cv : int, optional
        Number of cross-validation folds
    scoring : Optional[Callable], optional
        Scoring function
        
    Returns
    -------
    Tuple[Dict[str, Any], float]
        Best parameters and best score
    """
    if scoring is None:
        from ..evaluation.evaluator import r2_score
        scoring = r2_score
    
    grid = ParameterGrid(param_grid)
    best_score = float('-inf')
    best_params = None
    
    for params in grid:
        score = _evaluate_params(model, params, X, y, cv, scoring)
        if score > best_score:
            best_score = score
            best_params = params
    
    return best_params, best_score

def random_search(
    model: Any,
    param_distributions: Dict[str, List[Any]],
    X: np.ndarray,
    y: np.ndarray,
    n_iter: int = 100,
    cv: int = 5,
    scoring: Optional[Callable[[np.ndarray, np.ndarray], float]] = None
) -> Tuple[Dict[str, Any], float]:
    """
    Perform random search for hyperparameter tuning.
    
    Parameters
    ----------
    model : Any
        Model to tune
    param_distributions : Dict[str, List[Any]]
        Parameter distributions to sample from
    X : np.ndarray
        Training data
    y : np.ndarray
        Target values
    n_iter : int, optional
        Number of parameter settings to sample
    cv : int, optional
        Number of cross-validation folds
    scoring : Optional[Callable], optional
        Scoring function
        
    Returns
    -------
    Tuple[Dict[str, Any], float]
        Best parameters and best score
    """
    if scoring is None:
        from ..evaluation.evaluator import r2_score
        scoring = r2_score
    
    best_score = float('-inf')
    best_params = None
    
    for _ in range(n_iter):
        # Sample parameters
        params = {
            param: random.choice(values)
            for param, values in param_distributions.items()
        }
        
        score = _evaluate_params(model, params, X, y, cv, scoring)
        if score > best_score:
            best_score = score
            best_params = params
    
    return best_params, best_score

class GaussianProcess:
    """Simple Gaussian Process implementation for Bayesian optimization."""
    
    def __init__(self, kernel_func=None):
        """
        Initialize Gaussian Process.
        
        Parameters
        ----------
        kernel_func : Optional[Callable], optional
            Kernel function for GP
        """
        self.kernel_func = kernel_func or self._rbf_kernel
        self.X = None
        self.y = None
        
    def _rbf_kernel(self, X1: np.ndarray, X2: np.ndarray, l: float = 1.0) -> np.ndarray:
        """RBF kernel function."""
        sqdist = np.sum(X1**2, 1).reshape(-1, 1) + np.sum(X2**2, 1) - 2 * np.dot(X1, X2.T)
        return np.exp(-0.5 * sqdist / l**2)
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit the GP to the data."""
        self.X = X
        self.y = y
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict mean and variance."""
        K = self.kernel_func(self.X, self.X)
        K_s = self.kernel_func(self.X, X)
        K_ss = self.kernel_func(X, X)
        
        # Calculate mean and variance
        mu = K_s.T @ np.linalg.solve(K, self.y)
        sigma = np.diag(K_ss - K_s.T @ np.linalg.solve(K, K_s))
        
        return mu, sigma

def bayesian_optimization(
    model: Any,
    param_space: Dict[str, Tuple[float, float]],
    X: np.ndarray,
    y: np.ndarray,
    n_iter: int = 50,
    cv: int = 5,
    scoring: Optional[Callable[[np.ndarray, np.ndarray], float]] = None
) -> Tuple[Dict[str, Any], float]:
    """
    Perform Bayesian optimization for hyperparameter tuning.
    
    Parameters
    ----------
    model : Any
        Model to tune
    param_space : Dict[str, Tuple[float, float]]
        Parameter space to search (min, max for each parameter)
    X : np.ndarray
        Training data
    y : np.ndarray
        Target values
    n_iter : int, optional
        Number of iterations
    cv : int, optional
        Number of cross-validation folds
    scoring : Optional[Callable], optional
        Scoring function
        
    Returns
    -------
    Tuple[Dict[str, Any], float]
        Best parameters and best score
    """
    if scoring is None:
        from ..evaluation.evaluator import r2_score
        scoring = r2_score
    
    # Initialize GP
    gp = GaussianProcess()
    
    # Initialize storage for observations
    observed_params = []
    observed_scores = []
    
    # Random initial observations
    n_initial = min(5, n_iter)
    for _ in range(n_initial):
        params = {
            param: random.uniform(min_val, max_val)
            for param, (min_val, max_val) in param_space.items()
        }
        score = _evaluate_params(model, params, X, y, cv, scoring)
        observed_params.append(list(params.values()))
        observed_scores.append(score)
    
    # Convert to numpy arrays
    X_observed = np.array(observed_params)
    y_observed = np.array(observed_scores)
    
    # Bayesian optimization loop
    best_score = max(observed_scores)
    best_params = dict(zip(param_space.keys(), observed_params[np.argmax(observed_scores)]))
    
    for _ in range(n_iter - n_initial):
        # Fit GP
        gp.fit(X_observed, y_observed)
        
        # Generate candidate points
        n_candidates = 1000
        candidates = []
        for param, (min_val, max_val) in param_space.items():
            candidates.append(np.random.uniform(min_val, max_val, n_candidates))
        X_candidates = np.array(candidates).T
        
        # Predict mean and variance
        mu, sigma = gp.predict(X_candidates)
        
        # Calculate acquisition function (Expected Improvement)
        best_f = np.max(y_observed)
        with np.errstate(divide='warn'):
            imp = mu - best_f
            Z = imp / sigma
            ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
            ei[sigma == 0.0] = 0.0
        
        # Select next point
        next_idx = np.argmax(ei)
        next_params = dict(zip(param_space.keys(), X_candidates[next_idx]))
        
        # Evaluate
        score = _evaluate_params(model, next_params, X, y, cv, scoring)
        
        # Update observations
        X_observed = np.vstack([X_observed, X_candidates[next_idx]])
        y_observed = np.append(y_observed, score)
        
        # Update best
        if score > best_score:
            best_score = score
            best_params = next_params
    
    return best_params, best_score 
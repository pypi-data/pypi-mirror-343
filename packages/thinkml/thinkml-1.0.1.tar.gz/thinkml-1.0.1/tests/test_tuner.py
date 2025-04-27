"""
Tests for hyperparameter tuning functionality.
"""

import pytest
import numpy as np
from thinkml.selection.tuner import (
    grid_search,
    random_search,
    bayesian_optimization,
    ParameterGrid
)

class DummyModel:
    """Dummy model for testing."""
    def __init__(self):
        self.param1 = None
        self.param2 = None
        self.fitted = False
        
    def fit(self, X, y):
        self.fitted = True
        
    def predict(self, X):
        return np.zeros(len(X))

@pytest.fixture
def dummy_data():
    """Create dummy data for testing."""
    np.random.seed(42)
    X = np.random.randn(100, 5)
    y = np.random.randn(100)
    return X, y

@pytest.fixture
def dummy_model():
    """Create dummy model for testing."""
    return DummyModel()

def test_parameter_grid():
    """Test ParameterGrid class."""
    param_grid = {
        'param1': [1, 2, 3],
        'param2': ['a', 'b']
    }
    grid = ParameterGrid(param_grid)
    
    combinations = list(grid)
    assert len(combinations) == 6
    assert all(isinstance(params, dict) for params in combinations)
    assert all('param1' in params and 'param2' in params for params in combinations)

def test_grid_search(dummy_model, dummy_data):
    """Test grid search."""
    X, y = dummy_data
    param_grid = {
        'param1': [1, 2],
        'param2': ['a', 'b']
    }
    
    best_params, best_score = grid_search(dummy_model, param_grid, X, y)
    
    assert isinstance(best_params, dict)
    assert isinstance(best_score, float)
    assert 'param1' in best_params
    assert 'param2' in best_params
    assert dummy_model.fitted

def test_random_search(dummy_model, dummy_data):
    """Test random search."""
    X, y = dummy_data
    param_distributions = {
        'param1': [1, 2, 3, 4, 5],
        'param2': ['a', 'b', 'c']
    }
    
    best_params, best_score = random_search(
        dummy_model,
        param_distributions,
        X,
        y,
        n_iter=10
    )
    
    assert isinstance(best_params, dict)
    assert isinstance(best_score, float)
    assert 'param1' in best_params
    assert 'param2' in best_params
    assert dummy_model.fitted

def test_bayesian_optimization(dummy_model, dummy_data):
    """Test Bayesian optimization."""
    X, y = dummy_data
    param_space = {
        'param1': (0, 10),
        'param2': (-5, 5)
    }
    
    best_params, best_score = bayesian_optimization(
        dummy_model,
        param_space,
        X,
        y,
        n_iter=10
    )
    
    assert isinstance(best_params, dict)
    assert isinstance(best_score, float)
    assert 'param1' in best_params
    assert 'param2' in best_params
    assert 0 <= best_params['param1'] <= 10
    assert -5 <= best_params['param2'] <= 5
    assert dummy_model.fitted

def test_grid_search_custom_scoring(dummy_model, dummy_data):
    """Test grid search with custom scoring function."""
    X, y = dummy_data
    param_grid = {'param1': [1, 2]}
    
    def custom_scoring(y_true, y_pred):
        return -np.mean((y_true - y_pred) ** 2)  # Negative MSE
    
    best_params, best_score = grid_search(
        dummy_model,
        param_grid,
        X,
        y,
        scoring=custom_scoring
    )
    
    assert isinstance(best_params, dict)
    assert isinstance(best_score, float)
    assert best_score <= 0  # Negative MSE

def test_random_search_iterations(dummy_model, dummy_data):
    """Test random search with different numbers of iterations."""
    X, y = dummy_data
    param_distributions = {'param1': [1, 2, 3]}
    
    for n_iter in [5, 10, 20]:
        best_params, best_score = random_search(
            dummy_model,
            param_distributions,
            X,
            y,
            n_iter=n_iter
        )
        assert isinstance(best_params, dict)
        assert isinstance(best_score, float)

def test_bayesian_optimization_initial_points(dummy_model, dummy_data):
    """Test Bayesian optimization with different numbers of initial points."""
    X, y = dummy_data
    param_space = {'param1': (0, 1)}
    
    for n_iter in [5, 10]:
        best_params, best_score = bayesian_optimization(
            dummy_model,
            param_space,
            X,
            y,
            n_iter=n_iter
        )
        assert isinstance(best_params, dict)
        assert isinstance(best_score, float)
        assert 0 <= best_params['param1'] <= 1

def test_invalid_parameter_grid():
    """Test grid search with invalid parameter grid."""
    with pytest.raises(ValueError):
        ParameterGrid({})

def test_invalid_param_space(dummy_model, dummy_data):
    """Test Bayesian optimization with invalid parameter space."""
    X, y = dummy_data
    param_space = {'param1': (1, 0)}  # Invalid range
    
    with pytest.raises(ValueError):
        bayesian_optimization(dummy_model, param_space, X, y) 
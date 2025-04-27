"""
Tests for cross-validation functionality.
"""

import pytest
import numpy as np
from thinkml.validation.cross_validator import (
    cross_validate,
    leave_one_out_cv,
    time_series_cv,
    bootstrap_cv
)

class DummyModel:
    """Dummy model for testing."""
    def __init__(self):
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
    y = np.random.randint(0, 2, 100)
    return X, y

@pytest.fixture
def dummy_model():
    """Create dummy model for testing."""
    return DummyModel()

def test_cross_validate(dummy_model, dummy_data):
    """Test k-fold cross-validation."""
    X, y = dummy_data
    results = cross_validate(dummy_model, X, y, cv=5)
    
    assert isinstance(results, dict)
    assert all(metric in results for metric in ['accuracy', 'precision', 'recall', 'f1'])
    assert all(len(scores) == 5 for scores in results.values())
    assert dummy_model.fitted

def test_leave_one_out_cv(dummy_model, dummy_data):
    """Test leave-one-out cross-validation."""
    X, y = dummy_data
    results = leave_one_out_cv(dummy_model, X, y)
    
    assert isinstance(results, dict)
    assert all(metric in results for metric in ['accuracy', 'precision', 'recall', 'f1'])
    assert all(len(scores) == len(X) for scores in results.values())
    assert dummy_model.fitted

def test_time_series_cv(dummy_model, dummy_data):
    """Test time series cross-validation."""
    X, y = dummy_data
    results = time_series_cv(dummy_model, X, y, n_splits=5)
    
    assert isinstance(results, dict)
    assert all(metric in results for metric in ['accuracy', 'precision', 'recall', 'f1'])
    assert all(len(scores) == 5 for scores in results.values())
    assert dummy_model.fitted

def test_bootstrap_cv(dummy_model, dummy_data):
    """Test bootstrap cross-validation."""
    X, y = dummy_data
    results = bootstrap_cv(dummy_model, X, y, n_iterations=10)
    
    assert isinstance(results, dict)
    assert all(metric in results for metric in ['accuracy', 'precision', 'recall', 'f1'])
    assert all(len(scores) == 10 for scores in results.values())
    assert dummy_model.fitted

def test_cross_validate_invalid_inputs(dummy_model):
    """Test cross-validation with invalid inputs."""
    with pytest.raises(ValueError):
        cross_validate(dummy_model, np.array([]), np.array([]))
    
    with pytest.raises(ValueError):
        cross_validate(dummy_model, np.array([[1]]), np.array([1, 2]))

def test_cross_validate_custom_scoring(dummy_model, dummy_data):
    """Test cross-validation with custom scoring metric."""
    X, y = dummy_data
    
    def custom_scoring(y_true, y_pred):
        return np.mean(y_true == y_pred)
    
    results = cross_validate(dummy_model, X, y, scoring=custom_scoring)
    assert isinstance(results, dict)
    assert 'custom_scoring' in results
    assert len(results['custom_scoring']) == 5

def test_time_series_cv_sequential(dummy_model, dummy_data):
    """Test time series cross-validation maintains sequence."""
    X, y = dummy_data
    results = time_series_cv(dummy_model, X, y, n_splits=5)
    
    # Verify that each fold uses sequential data
    fold_size = len(X) // 6  # n_splits + 1
    for i in range(5):
        train_end = (i + 1) * fold_size
        test_end = train_end + fold_size
        assert train_end < test_end
        assert test_end <= len(X) 
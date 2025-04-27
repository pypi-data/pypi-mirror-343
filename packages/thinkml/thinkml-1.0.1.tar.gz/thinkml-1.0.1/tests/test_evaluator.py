"""
Tests for evaluation metrics.
"""

import pytest
import numpy as np
from thinkml.evaluation.evaluator import (
    confusion_matrix,
    roc_auc_score,
    mean_squared_error,
    root_mean_squared_error,
    mean_absolute_error,
    r2_score,
    evaluate_regression,
    evaluate_classification
)

@pytest.fixture
def classification_data():
    """Create dummy classification data."""
    np.random.seed(42)
    y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    y_pred = np.array([0, 1, 0, 0, 1, 1, 0, 1, 0, 1])
    y_score = np.array([0.1, 0.9, 0.2, 0.3, 0.8, 0.7, 0.1, 0.9, 0.2, 0.8])
    return y_true, y_pred, y_score

@pytest.fixture
def regression_data():
    """Create dummy regression data."""
    np.random.seed(42)
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.2, 1.8, 3.2, 3.8, 5.2])
    return y_true, y_pred

def test_confusion_matrix(classification_data):
    """Test confusion matrix calculation."""
    y_true, y_pred, _ = classification_data
    cm = confusion_matrix(y_true, y_pred)
    
    assert isinstance(cm, np.ndarray)
    assert cm.shape == (2, 2)
    assert np.sum(cm) == len(y_true)
    assert cm[0, 0] + cm[1, 1] == np.sum(y_true == y_pred)

def test_roc_auc_score(classification_data):
    """Test ROC-AUC score calculation."""
    y_true, _, y_score = classification_data
    auc = roc_auc_score(y_true, y_score)
    
    assert isinstance(auc, float)
    assert 0 <= auc <= 1
    assert auc > 0.5  # Should be better than random

def test_mean_squared_error(regression_data):
    """Test mean squared error calculation."""
    y_true, y_pred = regression_data
    mse = mean_squared_error(y_true, y_pred)
    
    assert isinstance(mse, float)
    assert mse >= 0
    assert mse == pytest.approx(0.04, rel=1e-10)

def test_root_mean_squared_error(regression_data):
    """Test root mean squared error calculation."""
    y_true, y_pred = regression_data
    rmse = root_mean_squared_error(y_true, y_pred)
    
    assert isinstance(rmse, float)
    assert rmse >= 0
    assert rmse == pytest.approx(np.sqrt(0.04), rel=1e-10)

def test_mean_absolute_error(regression_data):
    """Test mean absolute error calculation."""
    y_true, y_pred = regression_data
    mae = mean_absolute_error(y_true, y_pred)
    
    assert isinstance(mae, float)
    assert mae >= 0
    assert mae == pytest.approx(0.2, rel=1e-10)

def test_r2_score(regression_data):
    """Test R² score calculation."""
    y_true, y_pred = regression_data
    r2 = r2_score(y_true, y_pred)
    
    assert isinstance(r2, float)
    assert r2 <= 1
    assert r2 > 0  # Should be better than baseline

def test_evaluate_regression(regression_data):
    """Test regression evaluation."""
    y_true, y_pred = regression_data
    metrics = evaluate_regression(y_true, y_pred)
    
    assert isinstance(metrics, dict)
    assert all(metric in metrics for metric in ['mse', 'rmse', 'mae', 'r2'])
    assert all(isinstance(value, float) for value in metrics.values())

def test_evaluate_classification(classification_data):
    """Test classification evaluation."""
    y_true, y_pred, y_score = classification_data
    metrics = evaluate_classification(y_true, y_pred, y_score)
    
    assert isinstance(metrics, dict)
    assert 'confusion_matrix' in metrics
    assert 'roc_auc' in metrics
    assert isinstance(metrics['confusion_matrix'], np.ndarray)
    assert isinstance(metrics['roc_auc'], float)

def test_evaluate_classification_without_scores(classification_data):
    """Test classification evaluation without probability scores."""
    y_true, y_pred, _ = classification_data
    metrics = evaluate_classification(y_true, y_pred)
    
    assert isinstance(metrics, dict)
    assert 'confusion_matrix' in metrics
    assert 'roc_auc' not in metrics

def test_metrics_with_empty_inputs():
    """Test metrics with empty inputs."""
    with pytest.raises(ValueError):
        confusion_matrix(np.array([]), np.array([]))
    
    with pytest.raises(ValueError):
        roc_auc_score(np.array([]), np.array([]))
    
    with pytest.raises(ValueError):
        mean_squared_error(np.array([]), np.array([]))

def test_metrics_with_mismatched_inputs():
    """Test metrics with mismatched input lengths."""
    with pytest.raises(ValueError):
        confusion_matrix(np.array([0, 1]), np.array([0, 1, 2]))
    
    with pytest.raises(ValueError):
        roc_auc_score(np.array([0, 1]), np.array([0.1, 0.2, 0.3]))
    
    with pytest.raises(ValueError):
        mean_squared_error(np.array([1, 2]), np.array([1, 2, 3])) 
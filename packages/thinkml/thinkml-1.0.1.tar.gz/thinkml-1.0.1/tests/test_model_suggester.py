"""
Test cases for the model_suggester module.
"""

import pytest
import pandas as pd
import numpy as np
from thinkml.analyzer.model_suggester import suggest_model


@pytest.fixture
def classification_dataset():
    """Create a classification dataset with features X and categorical target y."""
    # Create a dataset with mixed features
    X = pd.DataFrame({
        'numeric1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'numeric2': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'categorical1': ['A', 'B', 'A', 'C', 'B', 'A', 'D', 'C', 'B', 'A'],
        'categorical2': ['X', 'Y', 'X', 'Z', 'Y', 'X', 'W', 'Z', 'Y', 'X']
    })
    
    # Create a categorical target with class imbalance
    y = pd.Series([0, 0, 0, 0, 0, 0, 0, 1, 1, 1])  # 7 class 0, 3 class 1
    
    return X, y


@pytest.fixture
def regression_dataset():
    """Create a regression dataset with features X and continuous target y."""
    # Create a dataset with mixed features
    X = pd.DataFrame({
        'numeric1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'numeric2': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'categorical1': ['A', 'B', 'A', 'C', 'B', 'A', 'D', 'C', 'B', 'A'],
        'categorical2': ['X', 'Y', 'X', 'Z', 'Y', 'X', 'W', 'Z', 'Y', 'X']
    })
    
    # Create a continuous target
    y = pd.Series([1.2, 2.4, 3.6, 4.8, 6.0, 7.2, 8.4, 9.6, 10.8, 12.0])
    
    return X, y


@pytest.fixture
def large_dataset():
    """Create a large dataset (>1 million rows) for testing Dask processing."""
    # Create a large dataset with 1.1 million rows
    n_samples = 1_100_000
    
    # Create features
    X = pd.DataFrame({
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.choice(['A', 'B', 'C'], n_samples)
    })
    
    # Create a target (alternating between classification and regression)
    if np.random.choice([True, False]):
        # Classification target
        y = pd.Series(np.random.choice([0, 1], n_samples))
    else:
        # Regression target
        y = pd.Series(np.random.randn(n_samples) * 10 + 50)
    
    return X, y


def test_classification_inference(classification_dataset):
    """Test automatic inference of classification problem."""
    X, y = classification_dataset
    
    result = suggest_model(X, y)
    
    # Check problem type
    assert result['problem_type'] == 'classification'
    
    # Check recommended models
    assert len(result['recommended_models']) == 3
    
    # Check model names
    model_names = [model['model'] for model in result['recommended_models']]
    assert 'Logistic Regression' in model_names
    assert 'Decision Tree Classifier' in model_names
    assert 'Random Forest Classifier' in model_names
    
    # Check complexity and reason fields
    for model in result['recommended_models']:
        assert 'complexity' in model
        assert 'reason' in model
        assert isinstance(model['complexity'], str)
        assert isinstance(model['reason'], str)
        assert model['complexity'].startswith('O(')


def test_regression_inference(regression_dataset):
    """Test automatic inference of regression problem."""
    X, y = regression_dataset
    
    result = suggest_model(X, y)
    
    # Check problem type
    assert result['problem_type'] == 'regression'
    
    # Check recommended models
    assert len(result['recommended_models']) == 3
    
    # Check model names
    model_names = [model['model'] for model in result['recommended_models']]
    assert 'Linear Regression' in model_names
    assert 'Ridge Regression' in model_names
    assert 'Decision Tree Regressor' in model_names
    
    # Check complexity and reason fields
    for model in result['recommended_models']:
        assert 'complexity' in model
        assert 'reason' in model
        assert isinstance(model['complexity'], str)
        assert isinstance(model['reason'], str)
        assert model['complexity'].startswith('O(')


def test_explicit_problem_type_classification(classification_dataset):
    """Test model suggestion with explicit classification problem type."""
    X, y = classification_dataset
    
    result = suggest_model(X, y, problem_type='classification')
    
    # Check problem type
    assert result['problem_type'] == 'classification'
    
    # Check recommended models
    assert len(result['recommended_models']) == 3
    
    # Check model names
    model_names = [model['model'] for model in result['recommended_models']]
    assert 'Logistic Regression' in model_names
    assert 'Decision Tree Classifier' in model_names
    assert 'Random Forest Classifier' in model_names


def test_explicit_problem_type_regression(regression_dataset):
    """Test model suggestion with explicit regression problem type."""
    X, y = regression_dataset
    
    result = suggest_model(X, y, problem_type='regression')
    
    # Check problem type
    assert result['problem_type'] == 'regression'
    
    # Check recommended models
    assert len(result['recommended_models']) == 3
    
    # Check model names
    model_names = [model['model'] for model in result['recommended_models']]
    assert 'Linear Regression' in model_names
    assert 'Ridge Regression' in model_names
    assert 'Decision Tree Regressor' in model_names


def test_invalid_inputs():
    """Test handling of invalid inputs."""
    X = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
    y = pd.Series([1, 2, 3])
    
    # Test with None inputs
    with pytest.raises(ValueError, match="Input features \\(X\\) and target \\(y\\) cannot be None"):
        suggest_model(None, y)
    with pytest.raises(ValueError, match="Input features \\(X\\) and target \\(y\\) cannot be None"):
        suggest_model(X, None)
    
    # Test with empty inputs
    with pytest.raises(ValueError, match="Input features \\(X\\) and target \\(y\\) cannot be empty"):
        suggest_model(pd.DataFrame(), y)
    with pytest.raises(ValueError, match="Input features \\(X\\) and target \\(y\\) cannot be empty"):
        suggest_model(X, pd.Series())
    
    # Test with invalid problem type
    with pytest.raises(ValueError, match="problem_type must be either 'classification' or 'regression'"):
        suggest_model(X, y, problem_type='invalid_type')


def test_y_length_mismatch():
    """Test handling of mismatched X and y lengths."""
    X = pd.DataFrame({'feature1': [1, 2, 3, 4, 5], 'feature2': [6, 7, 8, 9, 10]})
    y = pd.Series([1, 2, 3])  # Different length
    
    with pytest.raises(ValueError, match="Input features \\(X\\) and target \\(y\\) must have the same length"):
        suggest_model(X, y)


def test_large_dataset_dask_processing(large_dataset):
    """Test processing of large datasets using Dask."""
    X, y = large_dataset
    
    # This test will take some time to run due to the large dataset
    result = suggest_model(X, y)
    
    # Check that the result has the expected structure
    assert 'problem_type' in result
    assert 'recommended_models' in result
    assert len(result['recommended_models']) == 3
    
    # Check that each model has the required fields
    for model in result['recommended_models']:
        assert 'model' in model
        assert 'complexity' in model
        assert 'reason' in model
    
    # Check that the problem type is either classification or regression
    assert result['problem_type'] in ['classification', 'regression']
    
    # Check that the recommended models match the problem type
    if result['problem_type'] == 'classification':
        model_names = [model['model'] for model in result['recommended_models']]
        assert 'Logistic Regression' in model_names
        assert 'Decision Tree Classifier' in model_names
        assert 'Random Forest Classifier' in model_names
    else:
        model_names = [model['model'] for model in result['recommended_models']]
        assert 'Linear Regression' in model_names
        assert 'Ridge Regression' in model_names
        assert 'Decision Tree Regressor' in model_names 
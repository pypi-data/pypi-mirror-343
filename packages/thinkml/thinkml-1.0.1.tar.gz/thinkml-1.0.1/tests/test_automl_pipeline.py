"""
Test cases for the AutoML pipeline module.

This module contains comprehensive test cases for the AutoML pipeline,
including edge cases and error handling.
"""

import pytest
import numpy as np
import pandas as pd
import dask.dataframe as dd
from sklearn.datasets import make_classification, make_regression
from sklearn.exceptions import ConvergenceWarning

from thinkml.automl import automl_pipeline

# ===== Fixtures =====

@pytest.fixture
def classification_data():
    """Generate synthetic classification dataset."""
    X, y = make_classification(
        n_samples=100,
        n_features=5,
        n_informative=3,
        n_redundant=1,
        random_state=42
    )
    return pd.DataFrame(X, columns=[f'feature_{i}' for i in range(5)]), pd.Series(y)

@pytest.fixture
def regression_data():
    """Generate synthetic regression dataset."""
    X, y = make_regression(
        n_samples=100,
        n_features=5,
        n_informative=3,
        random_state=42
    )
    return pd.DataFrame(X, columns=[f'feature_{i}' for i in range(5)]), pd.Series(y)

@pytest.fixture
def large_classification_data():
    """Generate large synthetic classification dataset for Dask testing."""
    X, y = make_classification(
        n_samples=10000,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        random_state=42
    )
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(10)])
    df['target'] = y
    return dd.from_pandas(df, npartitions=4)

@pytest.fixture
def empty_dataframe():
    """Generate an empty DataFrame."""
    return pd.DataFrame(), pd.Series()

@pytest.fixture
def single_row_data():
    """Generate a dataset with a single row."""
    X = pd.DataFrame({'feature_0': [1.0], 'feature_1': [2.0]})
    y = pd.Series([0])
    return X, y

@pytest.fixture
def single_column_data():
    """Generate a dataset with a single column."""
    X = pd.DataFrame({'feature_0': [1.0, 2.0, 3.0, 4.0, 5.0]})
    y = pd.Series([0, 1, 0, 1, 0])
    return X, y

@pytest.fixture
def all_missing_data():
    """Generate a dataset with all missing values."""
    X = pd.DataFrame({
        'feature_0': [np.nan, np.nan, np.nan],
        'feature_1': [np.nan, np.nan, np.nan]
    })
    y = pd.Series([0, 1, 0])
    return X, y

@pytest.fixture
def all_categorical_data():
    """Generate a dataset with all categorical features."""
    X = pd.DataFrame({
        'feature_0': ['A', 'B', 'C', 'A', 'B'],
        'feature_1': ['X', 'Y', 'Z', 'X', 'Y']
    })
    y = pd.Series([0, 1, 0, 1, 0])
    return X, y

@pytest.fixture
def imbalanced_data():
    """Generate an imbalanced classification dataset."""
    X = pd.DataFrame({
        'feature_0': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        'feature_1': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    })
    y = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])  # 80% class 0, 20% class 1
    return X, y

@pytest.fixture
def constant_data():
    """Generate a dataset with constant values."""
    X = pd.DataFrame({
        'feature_0': [1.0, 1.0, 1.0, 1.0, 1.0],
        'feature_1': [2.0, 2.0, 2.0, 2.0, 2.0]
    })
    y = pd.Series([0, 1, 0, 1, 0])
    return X, y

@pytest.fixture
def duplicate_data():
    """Generate a dataset with duplicate rows."""
    X = pd.DataFrame({
        'feature_0': [1.0, 2.0, 1.0, 2.0, 1.0],
        'feature_1': [3.0, 4.0, 3.0, 4.0, 3.0]
    })
    y = pd.Series([0, 1, 0, 1, 0])
    return X, y

@pytest.fixture
def extreme_values_data():
    """Generate a dataset with extreme values."""
    X = pd.DataFrame({
        'feature_0': [1e-10, 1e10, 0.0, -1e10, 1e-10],
        'feature_1': [1e-10, 1e10, 0.0, -1e10, 1e-10]
    })
    y = pd.Series([0, 1, 0, 1, 0])
    return X, y

# ===== Basic Functionality Tests =====

def test_automl_classification_flow(classification_data):
    """Test AutoML pipeline for classification task."""
    X, y = classification_data
    
    # Add some missing values and categorical features
    X['categorical'] = np.random.choice(['A', 'B', 'C'], size=len(X))
    X.iloc[0:5, 0] = np.nan
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models
    
    # Check if metrics are present
    for model_metrics in evaluation_report.values():
        assert 'accuracy_mean' in model_metrics
        assert 'accuracy_std' in model_metrics

def test_automl_regression_flow(regression_data):
    """Test AutoML pipeline for regression task."""
    X, y = regression_data
    
    # Add some missing values and categorical features
    X['categorical'] = np.random.choice(['A', 'B', 'C'], size=len(X))
    X.iloc[0:5, 0] = np.nan
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='regression')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LinearRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models
    
    # Check if metrics are present
    for model_metrics in evaluation_report.values():
        assert 'mse_mean' in model_metrics
        assert 'mse_std' in model_metrics

def test_large_dataset_dask_handling(large_classification_data):
    """Test AutoML pipeline with large dataset using Dask."""
    # Split features and target
    X = large_classification_data.drop('target', axis=1)
    y = large_classification_data['target']
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models
    
    # Check if metrics are present
    for model_metrics in evaluation_report.values():
        assert 'accuracy_mean' in model_metrics
        assert 'accuracy_std' in model_metrics

# ===== Edge Cases =====

def test_empty_dataframe(empty_dataframe):
    """Test AutoML pipeline with empty DataFrame."""
    X, y = empty_dataframe
    
    with pytest.raises(ValueError, match="Empty DataFrame"):
        automl_pipeline(X, y, problem_type='classification')

def test_single_row_data(single_row_data):
    """Test AutoML pipeline with a single row of data."""
    X, y = single_row_data
    
    with pytest.raises(ValueError, match="Insufficient samples"):
        automl_pipeline(X, y, problem_type='classification')

def test_single_column_data(single_column_data):
    """Test AutoML pipeline with a single column."""
    X, y = single_column_data
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models

def test_all_missing_data(all_missing_data):
    """Test AutoML pipeline with all missing values."""
    X, y = all_missing_data
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models

def test_all_categorical_data(all_categorical_data):
    """Test AutoML pipeline with all categorical features."""
    X, y = all_categorical_data
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models

def test_imbalanced_data(imbalanced_data):
    """Test AutoML pipeline with imbalanced data."""
    X, y = imbalanced_data
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models

def test_constant_data(constant_data):
    """Test AutoML pipeline with constant data."""
    X, y = constant_data
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models

def test_duplicate_data(duplicate_data):
    """Test AutoML pipeline with duplicate rows."""
    X, y = duplicate_data
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models

def test_extreme_values_data(extreme_values_data):
    """Test AutoML pipeline with extreme values."""
    X, y = extreme_values_data
    
    best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None
    
    # Check if evaluation report contains all models
    expected_models = {'LogisticRegression', 'RandomForest', 'GradientBoosting', 
                      'SVM', 'NeuralNetwork'}
    assert set(evaluation_report.keys()) == expected_models

# ===== Error Handling Tests =====

def test_invalid_problem_type(classification_data):
    """Test AutoML pipeline with invalid problem type."""
    X, y = classification_data
    
    with pytest.raises(ValueError, match="Invalid problem type"):
        automl_pipeline(X, y, problem_type='invalid_type')

def test_mismatched_dimensions():
    """Test AutoML pipeline with mismatched dimensions."""
    X = pd.DataFrame({'feature_0': [1.0, 2.0, 3.0]})
    y = pd.Series([0, 1])  # Different length
    
    with pytest.raises(ValueError, match="Mismatched dimensions"):
        automl_pipeline(X, y, problem_type='classification')

def test_non_numeric_data():
    """Test AutoML pipeline with non-numeric data."""
    X = pd.DataFrame({'feature_0': ['a', 'b', 'c']})
    y = pd.Series([0, 1, 0])
    
    with pytest.raises(ValueError, match="Non-numeric data"):
        automl_pipeline(X, y, problem_type='classification')

def test_invalid_target_values():
    """Test AutoML pipeline with invalid target values for classification."""
    X = pd.DataFrame({'feature_0': [1.0, 2.0, 3.0]})
    y = pd.Series([0, 1, 2])  # Multi-class not supported
    
    with pytest.raises(ValueError, match="Binary classification only"):
        automl_pipeline(X, y, problem_type='classification')

# ===== Performance Tests =====

def test_performance_with_warnings(classification_data):
    """Test AutoML pipeline with convergence warnings."""
    X, y = classification_data
    
    # Add a feature that will cause convergence issues
    X['problematic'] = np.random.randn(len(X)) * 1e10
    
    with pytest.warns(ConvergenceWarning):
        best_model, evaluation_report = automl_pipeline(X, y, problem_type='classification')
    
    # Check if best model is returned despite warnings
    assert best_model is not None

def test_performance_with_timeout(classification_data):
    """Test AutoML pipeline with timeout."""
    X, y = classification_data
    
    # Create a very large dataset to test timeout
    X_large = pd.concat([X] * 100, ignore_index=True)
    y_large = pd.concat([y] * 100, ignore_index=True)
    
    # This should complete but might take longer
    best_model, evaluation_report = automl_pipeline(X_large, y_large, problem_type='classification')
    
    # Check if best model is returned
    assert best_model is not None 
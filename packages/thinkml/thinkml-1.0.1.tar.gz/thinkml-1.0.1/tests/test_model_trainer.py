"""
Tests for the model training and prediction functionality in ThinkML.
"""

import pytest
import numpy as np
import pandas as pd
import dask.dataframe as dd
from sklearn.datasets import make_classification, make_regression
from thinkml.model.trainer import train_multiple_models, predict_with_model

@pytest.fixture
def classification_dataset():
    """Create a classification dataset for testing."""
    np.random.seed(42)
    X, y = make_classification(
        n_samples=100,
        n_features=5,
        n_informative=3,
        n_redundant=1,
        n_repeated=1,
        n_classes=2,
        random_state=42
    )
    X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(5)])
    y = pd.Series(y)
    
    # Split into train and test sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    return X_train, X_test, y_train, y_test

@pytest.fixture
def regression_dataset():
    """Create a regression dataset for testing."""
    np.random.seed(42)
    X, y = make_regression(
        n_samples=100,
        n_features=5,
        n_informative=3,
        noise=0.1,
        random_state=42
    )
    X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(5)])
    y = pd.Series(y)
    
    # Split into train and test sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    return X_train, X_test, y_train, y_test

@pytest.fixture
def large_classification_dataset():
    """Create a large classification dataset for testing Dask functionality."""
    np.random.seed(42)
    X, y = make_classification(
        n_samples=1_100_000,  # More than 1 million rows
        n_features=5,
        n_informative=3,
        n_redundant=1,
        n_repeated=1,
        n_classes=2,
        random_state=42
    )
    X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(5)])
    y = pd.Series(y)
    
    # Convert to Dask DataFrames
    X_dask = dd.from_pandas(X, npartitions=10)
    y_dask = dd.from_pandas(y, npartitions=10)
    
    # Split into train and test sets
    # For Dask, we'll use a simple random split
    train_size = int(0.8 * len(X))
    X_train = X_dask.iloc[:train_size]
    X_test = X_dask.iloc[train_size:]
    y_train = y_dask.iloc[:train_size]
    y_test = y_dask.iloc[train_size:]
    
    return X_train, X_test, y_train, y_test

def test_train_multiple_models_classification(classification_dataset):
    """Test training and evaluation of classification models."""
    X_train, X_test, y_train, y_test = classification_dataset
    
    # Train models
    trained_models, evaluation_scores = train_multiple_models(
        X_train, y_train, X_test, y_test, problem_type='classification'
    )
    
    # Check that all expected models are trained
    expected_models = [
        'Logistic Regression', 'Decision Tree', 
        'Random Forest', 'KNN'
    ]
    for model_name in expected_models:
        assert model_name in trained_models, f"{model_name} not in trained models"
    
    # Check that evaluation scores are returned
    for model_name in expected_models:
        assert model_name in evaluation_scores, f"{model_name} not in evaluation scores"
        assert 'accuracy' in evaluation_scores[model_name], "Accuracy not in evaluation scores"
        assert 'f1_score' in evaluation_scores[model_name], "F1-score not in evaluation scores"
        
        # Check that scores are within expected ranges
        assert 0 <= evaluation_scores[model_name]['accuracy'] <= 1, "Accuracy out of range"
        assert 0 <= evaluation_scores[model_name]['f1_score'] <= 1, "F1-score out of range"

def test_train_multiple_models_regression(regression_dataset):
    """Test training and evaluation of regression models."""
    X_train, X_test, y_train, y_test = regression_dataset
    
    # Train models
    trained_models, evaluation_scores = train_multiple_models(
        X_train, y_train, X_test, y_test, problem_type='regression'
    )
    
    # Check that all expected models are trained
    expected_models = [
        'Linear Regression', 'Ridge Regression', 
        'Decision Tree', 'Random Forest'
    ]
    for model_name in expected_models:
        assert model_name in trained_models, f"{model_name} not in trained models"
    
    # Check that evaluation scores are returned
    for model_name in expected_models:
        assert model_name in evaluation_scores, f"{model_name} not in evaluation scores"
        assert 'rmse' in evaluation_scores[model_name], "RMSE not in evaluation scores"
        assert 'r2_score' in evaluation_scores[model_name], "R² not in evaluation scores"
        
        # Check that scores are within expected ranges
        assert evaluation_scores[model_name]['rmse'] >= 0, "RMSE should be non-negative"
        # R² can be negative for poor models, but should be between -1 and 1
        assert -1 <= evaluation_scores[model_name]['r2_score'] <= 1, "R² out of range"

def test_prediction_with_model(classification_dataset):
    """Test making predictions with a trained model."""
    X_train, X_test, y_train, y_test = classification_dataset
    
    # Train models
    trained_models, _ = train_multiple_models(
        X_train, y_train, X_test, y_test, problem_type='classification'
    )
    
    # Select a model for prediction
    model = trained_models['Logistic Regression']
    
    # Make predictions
    predictions = predict_with_model(model, X_test)
    
    # Check that predictions have the expected shape
    assert len(predictions) == len(X_test), "Predictions length doesn't match test set length"
    
    # Check that predictions are binary for classification
    assert np.all(np.isin(predictions, [0, 1])), "Predictions should be binary for classification"

def test_large_dataset_dask_handling(large_classification_dataset):
    """Test handling of large datasets with Dask."""
    X_train, X_test, y_train, y_test = large_classification_dataset
    
    # Train models
    trained_models, evaluation_scores = train_multiple_models(
        X_train, y_train, X_test, y_test, problem_type='classification'
    )
    
    # Check that all expected models are trained
    expected_models = [
        'Logistic Regression', 'Decision Tree', 
        'Random Forest', 'KNN'
    ]
    for model_name in expected_models:
        assert model_name in trained_models, f"{model_name} not in trained models"
    
    # Check that evaluation scores are returned
    for model_name in expected_models:
        assert model_name in evaluation_scores, f"{model_name} not in evaluation scores"
        assert 'accuracy' in evaluation_scores[model_name], "Accuracy not in evaluation scores"
        assert 'f1_score' in evaluation_scores[model_name], "F1-score not in evaluation scores"
        
        # Check that scores are within expected ranges
        assert 0 <= evaluation_scores[model_name]['accuracy'] <= 1, "Accuracy out of range"
        assert 0 <= evaluation_scores[model_name]['f1_score'] <= 1, "F1-score out of range"
    
    # Test prediction with a trained model
    model = trained_models['Logistic Regression']
    predictions = predict_with_model(model, X_test)
    
    # Check that predictions have the expected type (should be a Dask Series)
    assert isinstance(predictions, dd.Series), "Predictions should be a Dask Series for large datasets" 
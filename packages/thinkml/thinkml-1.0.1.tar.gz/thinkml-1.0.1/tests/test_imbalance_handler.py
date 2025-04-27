"""
Test cases for the imbalance_handler module.
"""

import pytest
import pandas as pd
import numpy as np
from thinkml.preprocessor.imbalance_handler import handle_imbalance


@pytest.fixture
def imbalanced_dataset():
    """Create a sample imbalanced dataset for testing."""
    # Create features
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, 1000),
        'feature2': np.random.normal(0, 1, 1000),
        'feature3': np.random.normal(0, 1, 1000)
    })
    
    # Create imbalanced target (90% class 0, 10% class 1)
    y = pd.Series([0] * 900 + [1] * 100)
    
    return X, y


@pytest.fixture
def regression_dataset():
    """Create a sample regression dataset for testing."""
    # Create features
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, 1000),
        'feature2': np.random.normal(0, 1, 1000),
        'feature3': np.random.normal(0, 1, 1000)
    })
    
    # Create continuous target
    y = pd.Series(np.random.normal(0, 1, 1000))
    
    return X, y


def test_smote_oversampling(imbalanced_dataset):
    """Test SMOTE oversampling method."""
    X, y = imbalanced_dataset
    
    # Apply SMOTE
    X_resampled, y_resampled = handle_imbalance(X, y, method='smote')
    
    # Check that the dataset size increased
    assert len(X_resampled) > len(X)
    assert len(y_resampled) > len(y)
    
    # Check that classes are balanced
    class_counts = y_resampled.value_counts()
    assert len(class_counts) == 2  # Two classes
    assert abs(class_counts[0] - class_counts[1]) <= 1  # Equal number of samples
    
    # Check that original data is preserved
    assert X_resampled.columns.equals(X.columns)
    
    # Check that synthetic samples are different from original ones
    # (SMOTE creates new samples, so there should be more unique rows)
    assert len(X_resampled.drop_duplicates()) > len(X.drop_duplicates())


def test_random_oversampling(imbalanced_dataset):
    """Test random oversampling method."""
    X, y = imbalanced_dataset
    
    # Apply random oversampling
    X_resampled, y_resampled = handle_imbalance(X, y, method='oversample')
    
    # Check that the dataset size increased
    assert len(X_resampled) > len(X)
    assert len(y_resampled) > len(y)
    
    # Check that classes are balanced
    class_counts = y_resampled.value_counts()
    assert len(class_counts) == 2  # Two classes
    assert abs(class_counts[0] - class_counts[1]) <= 1  # Equal number of samples
    
    # Check that original data is preserved
    assert X_resampled.columns.equals(X.columns)
    
    # Check that there are duplicate samples (random oversampling duplicates)
    assert len(X_resampled.drop_duplicates()) < len(X_resampled)


def test_random_undersampling(imbalanced_dataset):
    """Test random undersampling method."""
    X, y = imbalanced_dataset
    
    # Apply random undersampling
    X_resampled, y_resampled = handle_imbalance(X, y, method='undersample')
    
    # Check that the dataset size decreased
    assert len(X_resampled) < len(X)
    assert len(y_resampled) < len(y)
    
    # Check that classes are balanced
    class_counts = y_resampled.value_counts()
    assert len(class_counts) == 2  # Two classes
    assert abs(class_counts[0] - class_counts[1]) <= 1  # Equal number of samples
    
    # Check that original data is preserved
    assert X_resampled.columns.equals(X.columns)
    
    # Check that all samples in the resampled dataset are from the original dataset
    # (undersampling only removes samples, doesn't create new ones)
    for i in range(len(X_resampled)):
        row = X_resampled.iloc[i]
        # Check if this row exists in the original dataset
        exists = False
        for j in range(len(X)):
            if row.equals(X.iloc[j]):
                exists = True
                break
        assert exists, "Resampled row not found in original dataset"


def test_none_method(imbalanced_dataset):
    """Test 'none' method (no resampling)."""
    X, y = imbalanced_dataset
    
    # Apply 'none' method
    X_resampled, y_resampled = handle_imbalance(X, y, method='none')
    
    # Check that the dataset is unchanged
    pd.testing.assert_frame_equal(X_resampled, X)
    pd.testing.assert_series_equal(y_resampled, y)
    
    # Check that class distribution is still imbalanced
    class_counts = y_resampled.value_counts()
    assert class_counts[0] == 900  # 90% class 0
    assert class_counts[1] == 100  # 10% class 1


def test_invalid_method(imbalanced_dataset):
    """Test that invalid method raises ValueError."""
    X, y = imbalanced_dataset
    
    with pytest.raises(ValueError):
        handle_imbalance(X, y, method='invalid_method')


def test_regression_target(regression_dataset):
    """Test handling of regression target (continuous values)."""
    X, y = regression_dataset
    
    # For regression targets, imbalance handling should be skipped or raise a warning/error
    with pytest.raises(ValueError):
        handle_imbalance(X, y, method='smote')


def test_empty_input():
    """Test handling of empty input."""
    # Empty DataFrame and Series
    empty_X = pd.DataFrame()
    empty_y = pd.Series()
    
    with pytest.raises(ValueError):
        handle_imbalance(empty_X, empty_y, method='smote')
    
    # Empty DataFrame with non-empty Series
    non_empty_y = pd.Series([0, 1, 0, 1])
    
    with pytest.raises(ValueError):
        handle_imbalance(empty_X, non_empty_y, method='smote')
    
    # Non-empty DataFrame with empty Series
    non_empty_X = pd.DataFrame({'feature1': [1, 2, 3, 4]})
    
    with pytest.raises(ValueError):
        handle_imbalance(non_empty_X, empty_y, method='smote')


def test_single_class_target(imbalanced_dataset):
    """Test handling of single class target."""
    X, _ = imbalanced_dataset
    single_class_y = pd.Series([0] * 1000)  # All samples belong to class 0
    
    with pytest.raises(ValueError):
        handle_imbalance(X, single_class_y, method='smote')


def test_multi_class_target():
    """Test handling of multi-class target (more than 2 classes)."""
    # Create features
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, 1000),
        'feature2': np.random.normal(0, 1, 1000),
        'feature3': np.random.normal(0, 1, 1000)
    })
    
    # Create multi-class target (3 classes with imbalanced distribution)
    y = pd.Series([0] * 600 + [1] * 300 + [2] * 100)
    
    # Apply SMOTE
    X_resampled, y_resampled = handle_imbalance(X, y, method='smote')
    
    # Check that the dataset size increased
    assert len(X_resampled) > len(X)
    assert len(y_resampled) > len(y)
    
    # Check that classes are balanced
    class_counts = y_resampled.value_counts()
    assert len(class_counts) == 3  # Three classes
    # All classes should have approximately the same number of samples
    max_count = class_counts.max()
    min_count = class_counts.min()
    assert max_count - min_count <= 1  # Allow for small differences due to rounding 
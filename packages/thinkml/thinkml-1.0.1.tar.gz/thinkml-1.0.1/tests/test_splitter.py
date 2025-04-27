"""
Tests for the data splitting functionality in ThinkML.
"""

import pytest
import pandas as pd
import numpy as np
import dask.dataframe as dd
from thinkml.data_split.splitter import standardize_and_split

@pytest.fixture
def sample_data():
    """Create a sample dataset for testing."""
    np.random.seed(42)
    n_samples = 100
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(5, 2, n_samples),
        'feature3': np.random.uniform(-1, 1, n_samples)
    })
    y = pd.Series(np.random.randint(0, 2, n_samples))
    return X, y

@pytest.fixture
def sample_dask_data(sample_data):
    """Create a sample Dask dataset for testing."""
    X, y = sample_data
    X_dask = dd.from_pandas(X, npartitions=2)
    y_dask = dd.from_pandas(y, npartitions=2)
    return X_dask, y_dask

@pytest.fixture
def imbalanced_classification_data():
    """Create an imbalanced classification dataset for testing."""
    np.random.seed(42)
    n_samples = 1000
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(5, 2, n_samples),
        'feature3': np.random.uniform(-1, 1, n_samples)
    })
    # Create imbalanced classes: 80% class 0, 20% class 1
    y = pd.Series(np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2]))
    return X, y

@pytest.fixture
def data_with_outliers():
    """Create a dataset with extreme outliers for testing."""
    np.random.seed(42)
    n_samples = 100
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(5, 2, n_samples),
        'feature3': np.random.uniform(-1, 1, n_samples)
    })
    
    # Add extreme outliers
    X.loc[0, 'feature1'] = 100  # Extreme positive outlier
    X.loc[1, 'feature1'] = -100  # Extreme negative outlier
    X.loc[2, 'feature2'] = 200  # Extreme positive outlier
    X.loc[3, 'feature2'] = -200  # Extreme negative outlier
    
    y = pd.Series(np.random.randint(0, 2, n_samples))
    return X, y

def test_basic_split(sample_data):
    """Test basic splitting without scaling."""
    X, y = sample_data
    X_train, X_test, y_train, y_test = standardize_and_split(X, y, scaler=None)
    
    # Check shapes
    assert len(X_train) + len(X_test) == len(X)
    assert len(y_train) + len(y_test) == len(y)
    assert X_train.columns.equals(X.columns)
    assert X_test.columns.equals(X.columns)

def test_split_with_scaling(sample_data):
    """Test splitting with different scaling methods."""
    X, y = sample_data
    
    # Test with standard scaling
    X_train_std, X_test_std, _, _ = standardize_and_split(X, y, scaler='standard')
    assert np.allclose(X_train_std.mean(), 0, atol=1e-10)
    assert np.allclose(X_train_std.std(), 1, atol=1e-10)
    
    # Test with minmax scaling
    X_train_minmax, X_test_minmax, _, _ = standardize_and_split(X, y, scaler='minmax')
    assert X_train_minmax.min().min() >= 0
    assert X_train_minmax.max().max() <= 1
    
    # Test with robust scaling
    X_train_robust, X_test_robust, _, _ = standardize_and_split(X, y, scaler='robust')
    assert np.allclose(X_train_robust.median(), 0, atol=1e-10)

def test_dask_support(sample_dask_data):
    """Test splitting with Dask DataFrames."""
    X_dask, y_dask = sample_dask_data
    
    # Test without scaling
    X_train, X_test, y_train, y_test = standardize_and_split(X_dask, y_dask, scaler=None)
    assert isinstance(X_train, dd.DataFrame)
    assert isinstance(X_test, dd.DataFrame)
    
    # Test with scaling
    X_train_scaled, X_test_scaled, _, _ = standardize_and_split(X_dask, y_dask, scaler='standard')
    assert isinstance(X_train_scaled, dd.DataFrame)
    assert isinstance(X_test_scaled, dd.DataFrame)

def test_invalid_scaler(sample_data):
    """Test that invalid scaler options raise ValueError."""
    X, y = sample_data
    with pytest.raises(ValueError):
        standardize_and_split(X, y, scaler='invalid')

def test_no_target(sample_data):
    """Test splitting without target variable."""
    X, _ = sample_data
    X_train, X_test, y_train, y_test = standardize_and_split(X)
    assert y_train is None
    assert y_test is None
    assert len(X_train) + len(X_test) == len(X)

def test_custom_test_size(sample_data):
    """Test splitting with custom test size."""
    X, y = sample_data
    test_size = 0.3
    X_train, X_test, y_train, y_test = standardize_and_split(X, y, test_size=test_size)
    assert len(X_test) == int(len(X) * test_size)
    assert len(y_test) == int(len(y) * test_size)

def test_random_state(sample_data):
    """Test that random_state produces consistent splits."""
    X, y = sample_data
    random_state = 42
    
    # First split
    X_train1, X_test1, y_train1, y_test1 = standardize_and_split(
        X, y, random_state=random_state
    )
    
    # Second split with same random state
    X_train2, X_test2, y_train2, y_test2 = standardize_and_split(
        X, y, random_state=random_state
    )
    
    # Check that splits are identical
    pd.testing.assert_frame_equal(X_train1, X_train2)
    pd.testing.assert_frame_equal(X_test1, X_test2)
    pd.testing.assert_series_equal(y_train1, y_train2)
    pd.testing.assert_series_equal(y_test1, y_test2)

def test_stratified_split_classification(imbalanced_classification_data):
    """Test that class distribution is preserved in train/test splits."""
    X, y = imbalanced_classification_data
    
    # Calculate original class distribution
    original_dist = y.value_counts(normalize=True)
    
    # Perform split
    X_train, X_test, y_train, y_test = standardize_and_split(X, y, random_state=42)
    
    # Calculate class distribution in train and test sets
    train_dist = y_train.value_counts(normalize=True)
    test_dist = y_test.value_counts(normalize=True)
    
    # Check that class distribution is preserved within 5% margin
    for class_label in original_dist.index:
        assert abs(original_dist[class_label] - train_dist[class_label]) < 0.05, \
            f"Train set class distribution differs by more than 5% for class {class_label}"
        assert abs(original_dist[class_label] - test_dist[class_label]) < 0.05, \
            f"Test set class distribution differs by more than 5% for class {class_label}"

def test_scaling_validation_statistics(sample_data):
    """Test that scaling methods produce correct statistical properties."""
    X, y = sample_data
    
    # Test StandardScaler
    X_train_std, X_test_std, _, _ = standardize_and_split(X, y, scaler='standard')
    
    # Check that mean is approximately 0 and std is approximately 1 for each feature
    for col in X_train_std.columns:
        assert np.abs(X_train_std[col].mean()) < 1e-10, f"Mean of {col} is not close to 0"
        assert np.abs(X_train_std[col].std() - 1) < 1e-10, f"Std of {col} is not close to 1"
    
    # Test MinMaxScaler
    X_train_minmax, X_test_minmax, _, _ = standardize_and_split(X, y, scaler='minmax')
    
    # Check that min is 0 and max is 1 for each feature
    for col in X_train_minmax.columns:
        assert X_train_minmax[col].min() == 0, f"Min of {col} is not 0"
        assert X_train_minmax[col].max() == 1, f"Max of {col} is not 1"

def test_extreme_data_robust_scaler(data_with_outliers):
    """Test that RobustScaler handles extreme outliers correctly."""
    X, y = data_with_outliers
    
    # Apply RobustScaler
    X_train_robust, X_test_robust, _, _ = standardize_and_split(X, y, scaler='robust')
    
    # Check that median is approximately 0 for each feature
    for col in X_train_robust.columns:
        assert np.abs(X_train_robust[col].median()) < 1e-10, f"Median of {col} is not close to 0"
    
    # Check that IQR is approximately 1 for each feature
    # Calculate IQR manually since pandas doesn't have a direct IQR method
    for col in X_train_robust.columns:
        q1 = X_train_robust[col].quantile(0.25)
        q3 = X_train_robust[col].quantile(0.75)
        iqr = q3 - q1
        assert np.abs(iqr - 1) < 1e-10, f"IQR of {col} is not close to 1" 
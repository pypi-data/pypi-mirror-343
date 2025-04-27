"""
Test cases for the data_describer module.
"""

import pytest
import pandas as pd
import numpy as np
from thinkml.describer.data_describer import describe_data


@pytest.fixture
def sample_dataset():
    """Create a sample dataset with numerical and categorical features, missing values, and duplicate rows."""
    # Create a dataset with mixed features
    X = pd.DataFrame({
        'numeric1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'numeric2': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'categorical1': ['A', 'B', 'A', 'C', 'B', 'A', 'D', 'C', 'B', 'A'],
        'categorical2': ['X', 'Y', 'X', 'Z', 'Y', 'X', 'W', 'Z', 'Y', 'X']
    })
    
    # Add missing values
    X.loc[1, 'numeric1'] = np.nan
    X.loc[3, 'numeric2'] = np.nan
    X.loc[5, 'categorical1'] = np.nan
    X.loc[7, 'categorical2'] = np.nan
    
    # Add duplicate rows
    X.loc[9] = X.loc[0]  # Duplicate of first row
    
    return X


@pytest.fixture
def classification_target():
    """Create a categorical target for classification tests."""
    # Create a categorical target with class imbalance
    y = pd.Series([0, 0, 0, 0, 0, 0, 0, 1, 1, 1])  # 7 class 0, 3 class 1
    
    # Add missing values
    y.loc[2] = np.nan
    y.loc[8] = np.nan
    
    return y


@pytest.fixture
def regression_target():
    """Create a continuous target for regression tests."""
    # Create a continuous target
    y = pd.Series([1.2, 2.4, 3.6, 4.8, 6.0, 7.2, 8.4, 9.6, 10.8, 12.0])
    
    # Add missing values
    y.loc[3] = np.nan
    y.loc[7] = np.nan
    
    return y


def test_basic_statistics(sample_dataset):
    """Test basic statistics of the dataset description."""
    result = describe_data(sample_dataset)
    
    # Check num_samples
    assert result['num_samples'] == 10
    
    # Check num_features
    assert result['num_features'] == 4
    
    # Check memory_usage
    assert isinstance(result['memory_usage'], float)
    assert result['memory_usage'] > 0


def test_feature_types_detection(sample_dataset):
    """Test detection of numerical and categorical features."""
    result = describe_data(sample_dataset)
    
    # Check feature types
    assert result['feature_types']['numeric1'] == 'numerical'
    assert result['feature_types']['numeric2'] == 'numerical'
    assert result['feature_types']['categorical1'] == 'categorical'
    assert result['feature_types']['categorical2'] == 'categorical'


def test_missing_values_detection(sample_dataset, classification_target):
    """Test detection of missing values in features and target."""
    result = describe_data(sample_dataset, classification_target)
    
    # Check missing values in features
    assert result['missing_values']['features']['numeric1'] == 1
    assert result['missing_values']['features']['numeric2'] == 1
    assert result['missing_values']['features']['categorical1'] == 1
    assert result['missing_values']['features']['categorical2'] == 1
    
    # Check missing values in target
    assert result['missing_values']['target'] == 2


def test_duplicate_rows_detection(sample_dataset):
    """Test detection of duplicate rows."""
    result = describe_data(sample_dataset)
    
    # Check duplicate rows count
    assert result['duplicate_rows'] == 1  # One duplicate row


def test_feature_summary(sample_dataset):
    """Test feature summary statistics."""
    result = describe_data(sample_dataset)
    
    # Check numerical feature summary
    for feature in ['numeric1', 'numeric2']:
        assert result['feature_summary'][feature]['type'] == 'numerical'
        assert 'min' in result['feature_summary'][feature]
        assert 'max' in result['feature_summary'][feature]
        assert 'mean' in result['feature_summary'][feature]
        assert 'std' in result['feature_summary'][feature]
        assert 'median' in result['feature_summary'][feature]
    
    # Check categorical feature summary
    for feature in ['categorical1', 'categorical2']:
        assert result['feature_summary'][feature]['type'] == 'categorical'
        assert 'unique_count' in result['feature_summary'][feature]
        assert 'top' in result['feature_summary'][feature]
        assert 'frequency' in result['feature_summary'][feature]
        
        # Verify specific values for categorical1
        if feature == 'categorical1':
            assert result['feature_summary'][feature]['unique_count'] == 4  # A, B, C, D
            assert result['feature_summary'][feature]['top'] == 'A'
            assert result['feature_summary'][feature]['frequency'] == 4


def test_correlation_matrix(sample_dataset):
    """Test generation of correlation matrix for numerical features."""
    result = describe_data(sample_dataset)
    
    # Check correlation matrix
    assert 'correlation_matrix' in result
    assert len(result['correlation_matrix']) == 2  # 2 numerical features
    assert all(len(correlations) == 2 for correlations in result['correlation_matrix'].values())
    
    # Check that correlation matrix contains the correct features
    assert 'numeric1' in result['correlation_matrix']
    assert 'numeric2' in result['correlation_matrix']
    assert 'categorical1' not in result['correlation_matrix']
    assert 'categorical2' not in result['correlation_matrix']


def test_target_summary_classification(sample_dataset, classification_target):
    """Test target summary for classification tasks."""
    result = describe_data(sample_dataset, classification_target)
    
    # Check target summary
    assert 'target_summary' in result
    assert result['target_summary']['type'] == 'categorical'
    assert result['target_summary']['unique_count'] == 2
    
    # Check class balance
    assert 'class_balance' in result
    assert 'counts' in result['class_balance']
    assert 'percentages' in result['class_balance']
    assert result['class_balance']['counts'][0] == 5  # 7 - 2 missing
    assert result['class_balance']['counts'][1] == 1  # 3 - 2 missing
    
    # Check imbalance status
    assert result['imbalance_status'] == 'imbalanced'  # 5/6 ≈ 83% is > 60%


def test_target_summary_regression(sample_dataset, regression_target):
    """Test target summary for regression tasks."""
    result = describe_data(sample_dataset, regression_target)
    
    # Check target summary
    assert 'target_summary' in result
    assert result['target_summary']['type'] == 'numerical'
    assert result['target_summary']['unique_count'] == 8  # 10 - 2 missing
    
    # Check that class_balance is not present for regression
    assert 'class_balance' not in result
    assert 'imbalance_status' not in result


def test_empty_dataframe():
    """Test handling of empty DataFrame."""
    with pytest.raises(ValueError, match="Input DataFrame cannot be empty"):
        describe_data(pd.DataFrame())


def test_y_length_mismatch(sample_dataset):
    """Test handling of mismatched X and y lengths."""
    # Create a target with different length
    y = pd.Series([0, 1, 0, 1, 0])
    
    with pytest.raises(ValueError, match="X and y must have the same length"):
        describe_data(sample_dataset, y)


def test_large_dataset_chunk_processing():
    """Test processing of large datasets using chunking."""
    # Create a large dataset
    n_samples = 150000  # Larger than default chunk_size
    X = pd.DataFrame({
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.choice(['A', 'B', 'C'], n_samples)
    })
    
    # Add some missing values
    X.loc[np.random.choice(n_samples, 1000), 'feature1'] = np.nan
    X.loc[np.random.choice(n_samples, 1000), 'feature2'] = np.nan
    X.loc[np.random.choice(n_samples, 1000), 'feature3'] = np.nan
    
    # Process with default chunk_size
    result = describe_data(X)
    
    # Check basic information
    assert result['num_samples'] == n_samples
    assert result['num_features'] == 3
    
    # Check feature types
    assert result['feature_types']['feature1'] == 'numerical'
    assert result['feature_types']['feature2'] == 'numerical'
    assert result['feature_types']['feature3'] == 'categorical'
    
    # Check missing values
    assert result['missing_values']['features']['feature1'] == 1000
    assert result['missing_values']['features']['feature2'] == 1000
    assert result['missing_values']['features']['feature3'] == 1000
    
    # Check correlation matrix
    assert 'correlation_matrix' in result
    assert len(result['correlation_matrix']) == 2  # 2 numerical features


def test_very_large_dataset_dask_processing():
    """Test processing of very large datasets using Dask."""
    # Create a very large dataset (>1M rows)
    n_samples = 1_100_000
    X = pd.DataFrame({
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.choice(['A', 'B', 'C'], n_samples)
    })
    
    # Add some missing values
    X.loc[np.random.choice(n_samples, 10000), 'feature1'] = np.nan
    X.loc[np.random.choice(n_samples, 10000), 'feature2'] = np.nan
    X.loc[np.random.choice(n_samples, 10000), 'feature3'] = np.nan
    
    # Process with Dask
    result = describe_data(X)
    
    # Check basic information
    assert result['num_samples'] == n_samples
    assert result['num_features'] == 3
    
    # Check feature types
    assert result['feature_types']['feature1'] == 'numerical'
    assert result['feature_types']['feature2'] == 'numerical'
    assert result['feature_types']['feature3'] == 'categorical'
    
    # Check missing values (approximate due to sampling in Dask)
    assert 9000 <= result['missing_values']['features']['feature1'] <= 11000
    assert 9000 <= result['missing_values']['features']['feature2'] <= 11000
    assert 9000 <= result['missing_values']['features']['feature3'] <= 11000 
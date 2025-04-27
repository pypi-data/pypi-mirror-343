"""
Tests for the outlier detection functionality in ThinkML.
"""

import pytest
import pandas as pd
import numpy as np
from thinkml.outliers.detector import detect_outliers

@pytest.fixture
def sample_data():
    """Create a sample DataFrame with known outliers."""
    np.random.seed(42)
    n_samples = 100
    
    # Create normal distribution data
    normal_data = np.random.normal(0, 1, n_samples)
    
    # Add some outliers
    outliers = np.array([10, -10, 8, -8, 5, -5])
    data = np.concatenate([normal_data, outliers])
    
    # Create DataFrame
    df = pd.DataFrame({
        'normal': data,
        'skewed': np.concatenate([
            np.random.normal(0, 1, n_samples),
            np.array([20, -20, 15, -15])
        ]),
        'uniform': np.random.uniform(-1, 1, n_samples + 6)
    })
    
    return df

@pytest.fixture
def empty_data():
    """Create an empty DataFrame."""
    return pd.DataFrame()

@pytest.fixture
def non_numeric_data():
    """Create a DataFrame with non-numeric columns."""
    return pd.DataFrame({
        'numeric': [1, 2, 3],
        'string': ['a', 'b', 'c'],
        'category': pd.Categorical(['x', 'y', 'z'])
    })

def test_zscore_method(sample_data):
    """Test outlier detection using Z-score method."""
    result = detect_outliers(sample_data, method='zscore', report=False, visualize=False)
    
    # Check result structure
    assert isinstance(result, dict)
    assert 'outlier_counts' in result
    assert 'outlier_percentage' in result
    assert 'outlier_indices' in result
    assert 'feature_outliers' in result
    
    # Check that outliers were detected
    assert len(result['outlier_indices']) > 0
    assert result['outlier_percentage'] > 0
    
    # Check that 'normal' column has more outliers than 'uniform'
    assert result['outlier_counts']['normal'] > result['outlier_counts']['uniform']

def test_iqr_method(sample_data):
    """Test outlier detection using IQR method."""
    result = detect_outliers(sample_data, method='iqr', report=False, visualize=False)
    
    # Check result structure
    assert isinstance(result, dict)
    assert 'outlier_counts' in result
    assert 'outlier_percentage' in result
    assert 'outlier_indices' in result
    assert 'feature_outliers' in result
    
    # Check that outliers were detected
    assert len(result['outlier_indices']) > 0
    assert result['outlier_percentage'] > 0
    
    # Check that 'skewed' column has more outliers than 'uniform'
    assert result['outlier_counts']['skewed'] > result['outlier_counts']['uniform']

def test_isolation_forest_method(sample_data):
    """Test outlier detection using Isolation Forest method."""
    result = detect_outliers(sample_data, method='isolation_forest', report=False, visualize=False)
    
    # Check result structure
    assert isinstance(result, dict)
    assert 'outlier_counts' in result
    assert 'outlier_percentage' in result
    assert 'outlier_indices' in result
    assert 'feature_outliers' in result
    
    # Check that outliers were detected
    assert len(result['outlier_indices']) > 0
    assert result['outlier_percentage'] > 0

def test_invalid_method(sample_data):
    """Test that invalid method raises ValueError."""
    with pytest.raises(ValueError):
        detect_outliers(sample_data, method='invalid_method')

def test_empty_dataframe(empty_data):
    """Test that empty DataFrame raises ValueError."""
    with pytest.raises(ValueError):
        detect_outliers(empty_data)

def test_non_numeric_data(non_numeric_data):
    """Test that non-numeric data raises ValueError."""
    with pytest.raises(ValueError):
        detect_outliers(non_numeric_data)

def test_large_dataset():
    """Test handling of large datasets."""
    # Create a large dataset
    n_samples = 1_100_000  # Just over the threshold for Dask
    df = pd.DataFrame({
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(0, 1, n_samples)
    })
    
    # Add some outliers
    df.loc[0:5, 'feature1'] = 10
    
    result = detect_outliers(df, method='zscore', report=False, visualize=False)
    
    # Check that outliers were detected
    assert len(result['outlier_indices']) > 0
    assert result['outlier_counts']['feature1'] > 0

def test_chunk_size_parameter(sample_data):
    """Test that chunk_size parameter is respected."""
    # Create a larger dataset
    df = pd.concat([sample_data] * 1000, ignore_index=True)
    
    result = detect_outliers(df, method='zscore', chunk_size=1000, report=False, visualize=False)
    
    # Check that outliers were detected
    assert len(result['outlier_indices']) > 0

def test_report_parameter(sample_data, capsys):
    """Test that report parameter controls output."""
    # Test with report=True
    detect_outliers(sample_data, method='zscore', report=True, visualize=False)
    captured = capsys.readouterr()
    assert "OUTLIER DETECTION REPORT" in captured.out
    
    # Test with report=False
    detect_outliers(sample_data, method='zscore', report=False, visualize=False)
    captured = capsys.readouterr()
    assert "OUTLIER DETECTION REPORT" not in captured.out

def test_visualize_parameter(sample_data):
    """Test that visualize parameter controls plotting."""
    # This test is mainly to ensure no errors occur
    # Actual visualization testing would require more complex setup
    detect_outliers(sample_data, method='zscore', report=False, visualize=True)
    detect_outliers(sample_data, method='zscore', report=False, visualize=False)

def test_multiple_features(sample_data):
    """Test detection across multiple features."""
    result = detect_outliers(sample_data, method='zscore', report=False, visualize=False)
    
    # Check that all features are analyzed
    assert set(result['outlier_counts'].keys()) == set(sample_data.columns)
    assert set(result['feature_outliers'].keys()) == set(sample_data.columns)

def test_outlier_indices_consistency(sample_data):
    """Test that outlier indices are consistent across different methods."""
    zscore_result = detect_outliers(sample_data, method='zscore', report=False, visualize=False)
    iqr_result = detect_outliers(sample_data, method='iqr', report=False, visualize=False)
    
    # Check that both methods detect some outliers
    assert len(zscore_result['outlier_indices']) > 0
    assert len(iqr_result['outlier_indices']) > 0
    
    # Check that the indices are lists
    assert isinstance(zscore_result['outlier_indices'], list)
    assert isinstance(iqr_result['outlier_indices'], list)
    
    # Check that indices are sorted
    assert zscore_result['outlier_indices'] == sorted(zscore_result['outlier_indices'])
    assert iqr_result['outlier_indices'] == sorted(iqr_result['outlier_indices']) 
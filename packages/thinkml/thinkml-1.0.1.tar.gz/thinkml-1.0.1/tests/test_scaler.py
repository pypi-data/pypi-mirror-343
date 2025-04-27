"""
Test cases for the scaler module.
"""

import pytest
import pandas as pd
import numpy as np
from thinkml.preprocessor.scaler import scale_features


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame with numerical features for testing."""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 100],  # Including an outlier
        'feature2': [10, 20, 30, 40, 50, 200],  # Including an outlier
        'feature3': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        'categorical': ['A', 'B', 'C', 'D', 'E', 'F']  # Non-numeric column
    })


def test_standard_scaler(sample_dataframe):
    """Test standard scaling method."""
    result = scale_features(sample_dataframe, method='standard')
    
    # Check that categorical column is unchanged
    assert 'categorical' in result.columns
    pd.testing.assert_series_equal(result['categorical'], sample_dataframe['categorical'])
    
    # Check that numeric columns are scaled
    assert 'feature1' in result.columns
    assert 'feature2' in result.columns
    assert 'feature3' in result.columns
    
    # Check that scaled columns have mean ≈ 0 and std ≈ 1
    # We use a small tolerance for floating point comparison
    for col in ['feature1', 'feature2', 'feature3']:
        assert abs(result[col].mean()) < 1e-10
        assert abs(result[col].std() - 1.0) < 1e-10


def test_minmax_scaler(sample_dataframe):
    """Test min-max scaling method."""
    result = scale_features(sample_dataframe, method='minmax')
    
    # Check that categorical column is unchanged
    assert 'categorical' in result.columns
    pd.testing.assert_series_equal(result['categorical'], sample_dataframe['categorical'])
    
    # Check that numeric columns are scaled
    assert 'feature1' in result.columns
    assert 'feature2' in result.columns
    assert 'feature3' in result.columns
    
    # Check that all values are between 0 and 1
    for col in ['feature1', 'feature2', 'feature3']:
        assert result[col].min() >= 0
        assert result[col].max() <= 1


def test_robust_scaler(sample_dataframe):
    """Test robust scaling method."""
    result = scale_features(sample_dataframe, method='robust')
    
    # Check that categorical column is unchanged
    assert 'categorical' in result.columns
    pd.testing.assert_series_equal(result['categorical'], sample_dataframe['categorical'])
    
    # Check that numeric columns are scaled
    assert 'feature1' in result.columns
    assert 'feature2' in result.columns
    assert 'feature3' in result.columns
    
    # Check that scaling is based on IQR (outliers minimally affect scaling)
    # For robust scaling, the median should be 0 and the IQR should be 1
    for col in ['feature1', 'feature2', 'feature3']:
        assert abs(result[col].median()) < 1e-10
        # Calculate IQR
        q1 = result[col].quantile(0.25)
        q3 = result[col].quantile(0.75)
        iqr = q3 - q1
        assert abs(iqr - 1.0) < 1e-10


def test_normalize(sample_dataframe):
    """Test normalization method."""
    result = scale_features(sample_dataframe, method='normalize')
    
    # Check that categorical column is unchanged
    assert 'categorical' in result.columns
    pd.testing.assert_series_equal(result['categorical'], sample_dataframe['categorical'])
    
    # Check that numeric columns are scaled
    assert 'feature1' in result.columns
    assert 'feature2' in result.columns
    assert 'feature3' in result.columns
    
    # Check that rows are normalized (L2 norm = 1)
    # We need to exclude the categorical column for this check
    numeric_cols = ['feature1', 'feature2', 'feature3']
    for i in range(len(result)):
        row_norm = np.sqrt(sum(result.loc[i, col]**2 for col in numeric_cols))
        assert abs(row_norm - 1.0) < 1e-10


def test_specific_columns(sample_dataframe):
    """Test scaling specific columns."""
    result = scale_features(sample_dataframe, method='standard', columns=['feature1'])
    
    # Check that only feature1 is scaled
    assert 'feature1' in result.columns
    assert abs(result['feature1'].mean()) < 1e-10
    assert abs(result['feature1'].std() - 1.0) < 1e-10
    
    # Check that other columns are unchanged
    pd.testing.assert_series_equal(result['feature2'], sample_dataframe['feature2'])
    pd.testing.assert_series_equal(result['feature3'], sample_dataframe['feature3'])
    pd.testing.assert_series_equal(result['categorical'], sample_dataframe['categorical'])


def test_invalid_method(sample_dataframe):
    """Test that invalid method raises ValueError."""
    with pytest.raises(ValueError):
        scale_features(sample_dataframe, method='invalid_method')


def test_invalid_columns(sample_dataframe):
    """Test that invalid columns raises ValueError."""
    with pytest.raises(ValueError):
        scale_features(sample_dataframe, columns=['non_existent_column'])


def test_empty_dataframe():
    """Test scaling with empty DataFrame."""
    empty_df = pd.DataFrame()
    result = scale_features(empty_df, method='standard')
    
    # Check that the result is an empty DataFrame
    assert result.empty
    assert len(result.columns) == 0


def test_dataframe_without_numeric_columns():
    """Test scaling with DataFrame without numeric columns."""
    df = pd.DataFrame({
        'categorical1': ['A', 'B', 'C', 'D', 'E'],
        'categorical2': ['X', 'Y', 'Z', 'W', 'V']
    })
    
    result = scale_features(df, method='standard')
    
    # Check that the result is identical to the input
    pd.testing.assert_frame_equal(result, df) 
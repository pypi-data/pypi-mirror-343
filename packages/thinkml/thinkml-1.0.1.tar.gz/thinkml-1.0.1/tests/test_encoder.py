"""
Test cases for the encoder module.
"""

import pytest
import pandas as pd
import numpy as np
from thinkml.preprocessor.encoder import encode_categorical


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame with categorical features for testing."""
    return pd.DataFrame({
        'categorical1': ['A', 'B', 'A', 'C', 'B'],
        'categorical2': ['X', 'Y', 'X', 'Z', 'Y'],
        'numeric': [1, 2, 3, 4, 5]
    })


def test_onehot_encoding(sample_dataframe):
    """Test one-hot encoding method."""
    result = encode_categorical(sample_dataframe, method='onehot')
    
    # Check that the numeric column is unchanged
    assert 'numeric' in result.columns
    
    # Check that categorical columns are encoded
    assert 'categorical1_A' in result.columns
    assert 'categorical1_B' in result.columns
    assert 'categorical1_C' in result.columns
    assert 'categorical2_X' in result.columns
    assert 'categorical2_Y' in result.columns
    assert 'categorical2_Z' in result.columns
    
    # Check that the original categorical columns are removed
    assert 'categorical1' not in result.columns
    assert 'categorical2' not in result.columns
    
    # Check that the encoding is correct
    assert result['categorical1_A'].sum() == 2  # 'A' appears twice
    assert result['categorical1_B'].sum() == 2  # 'B' appears twice
    assert result['categorical1_C'].sum() == 1  # 'C' appears once
    assert result['categorical2_X'].sum() == 2  # 'X' appears twice
    assert result['categorical2_Y'].sum() == 2  # 'Y' appears twice
    assert result['categorical2_Z'].sum() == 1  # 'Z' appears once


def test_onehot_encoding_drop_first(sample_dataframe):
    """Test one-hot encoding method with drop_first=True."""
    result = encode_categorical(sample_dataframe, method='onehot', drop_first=True)
    
    # Check that the numeric column is unchanged
    assert 'numeric' in result.columns
    
    # Check that one category is dropped for each categorical column
    assert 'categorical1_A' not in result.columns
    assert 'categorical1_B' in result.columns
    assert 'categorical1_C' in result.columns
    assert 'categorical2_X' not in result.columns
    assert 'categorical2_Y' in result.columns
    assert 'categorical2_Z' in result.columns
    
    # Check that the original categorical columns are removed
    assert 'categorical1' not in result.columns
    assert 'categorical2' not in result.columns


def test_label_encoding(sample_dataframe):
    """Test label encoding method."""
    result = encode_categorical(sample_dataframe, method='label')
    
    # Check that the numeric column is unchanged
    assert 'numeric' in result.columns
    
    # Check that categorical columns are encoded
    assert 'categorical1' in result.columns
    assert 'categorical2' in result.columns
    
    # Check that the encoding is numeric
    assert pd.api.types.is_numeric_dtype(result['categorical1'])
    assert pd.api.types.is_numeric_dtype(result['categorical2'])
    
    # Check that each category has a unique label
    assert len(result['categorical1'].unique()) == 3  # A, B, C
    assert len(result['categorical2'].unique()) == 3  # X, Y, Z


def test_ordinal_encoding(sample_dataframe):
    """Test ordinal encoding method."""
    result = encode_categorical(sample_dataframe, method='ordinal')
    
    # Check that the numeric column is unchanged
    assert 'numeric' in result.columns
    
    # Check that categorical columns are encoded
    assert 'categorical1' in result.columns
    assert 'categorical2' in result.columns
    
    # Check that the encoding is numeric
    assert pd.api.types.is_numeric_dtype(result['categorical1'])
    assert pd.api.types.is_numeric_dtype(result['categorical2'])
    
    # Check that each category has a unique label
    assert len(result['categorical1'].unique()) == 3  # A, B, C
    assert len(result['categorical2'].unique()) == 3  # X, Y, Z


def test_binary_encoding(sample_dataframe):
    """Test binary encoding method."""
    result = encode_categorical(sample_dataframe, method='binary')
    
    # Check that the numeric column is unchanged
    assert 'numeric' in result.columns
    
    # Check that categorical columns are encoded
    assert 'categorical1_0' in result.columns
    assert 'categorical1_1' in result.columns
    assert 'categorical2_0' in result.columns
    assert 'categorical2_1' in result.columns
    
    # Check that the original categorical columns are removed
    assert 'categorical1' not in result.columns
    assert 'categorical2' not in result.columns
    
    # Check that the encoding is binary (0 or 1)
    assert result['categorical1_0'].isin([0, 1]).all()
    assert result['categorical1_1'].isin([0, 1]).all()
    assert result['categorical2_0'].isin([0, 1]).all()
    assert result['categorical2_1'].isin([0, 1]).all()


def test_specific_columns(sample_dataframe):
    """Test encoding specific columns."""
    result = encode_categorical(sample_dataframe, method='onehot', columns=['categorical1'])
    
    # Check that only categorical1 is encoded
    assert 'categorical1_A' in result.columns
    assert 'categorical1_B' in result.columns
    assert 'categorical1_C' in result.columns
    
    # Check that categorical2 is unchanged
    assert 'categorical2' in result.columns
    assert 'categorical2_X' not in result.columns
    assert 'categorical2_Y' not in result.columns
    assert 'categorical2_Z' not in result.columns
    
    # Check that the numeric column is unchanged
    assert 'numeric' in result.columns


def test_invalid_method(sample_dataframe):
    """Test that invalid method raises ValueError."""
    with pytest.raises(ValueError):
        encode_categorical(sample_dataframe, method='invalid_method')


def test_invalid_columns(sample_dataframe):
    """Test that invalid columns raises ValueError."""
    with pytest.raises(ValueError):
        encode_categorical(sample_dataframe, columns=['non_existent_column'])


def test_empty_dataframe():
    """Test encoding with empty DataFrame."""
    empty_df = pd.DataFrame()
    result = encode_categorical(empty_df, method='onehot')
    
    # Check that the result is an empty DataFrame
    assert result.empty
    assert len(result.columns) == 0


def test_dataframe_without_categorical_columns():
    """Test encoding with DataFrame without categorical columns."""
    df = pd.DataFrame({
        'numeric1': [1, 2, 3, 4, 5],
        'numeric2': [10, 20, 30, 40, 50]
    })
    
    result = encode_categorical(df, method='onehot')
    
    # Check that the result is identical to the input
    pd.testing.assert_frame_equal(result, df) 
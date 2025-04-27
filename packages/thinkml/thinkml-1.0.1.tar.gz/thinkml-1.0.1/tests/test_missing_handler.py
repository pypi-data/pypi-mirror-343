"""
Test cases for the missing_handler module.
"""

import pytest
import pandas as pd
import numpy as np
from thinkml.preprocessor.missing_handler import handle_missing_values


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame with missing values for testing."""
    return pd.DataFrame({
        'numeric1': [1, 2, np.nan, 4, 5],
        'numeric2': [10, np.nan, 30, 40, 50],
        'categorical': ['A', 'B', np.nan, 'D', 'E']
    })


def test_mean_strategy(sample_dataframe):
    """Test handling missing values with mean strategy."""
    result = handle_missing_values(sample_dataframe, strategy='mean')
    
    # Check that numeric columns have missing values filled with mean
    assert result['numeric1'].isna().sum() == 0
    assert result['numeric2'].isna().sum() == 0
    
    # Check that categorical column still has missing values
    assert result['categorical'].isna().sum() == 1
    
    # Check that the mean values are correct
    assert result['numeric1'].mean() == sample_dataframe['numeric1'].mean()
    assert result['numeric2'].mean() == sample_dataframe['numeric2'].mean()


def test_median_strategy(sample_dataframe):
    """Test handling missing values with median strategy."""
    result = handle_missing_values(sample_dataframe, strategy='median')
    
    # Check that numeric columns have missing values filled with median
    assert result['numeric1'].isna().sum() == 0
    assert result['numeric2'].isna().sum() == 0
    
    # Check that categorical column still has missing values
    assert result['categorical'].isna().sum() == 1
    
    # Check that the median values are correct
    assert result['numeric1'].median() == sample_dataframe['numeric1'].median()
    assert result['numeric2'].median() == sample_dataframe['numeric2'].median()


def test_mode_strategy(sample_dataframe):
    """Test handling missing values with mode strategy."""
    result = handle_missing_values(sample_dataframe, strategy='mode')
    
    # Check that all columns have missing values filled with mode
    assert result['numeric1'].isna().sum() == 0
    assert result['numeric2'].isna().sum() == 0
    assert result['categorical'].isna().sum() == 0
    
    # Check that the mode values are correct
    assert result['numeric1'].mode().iloc[0] == sample_dataframe['numeric1'].mode().iloc[0]
    assert result['numeric2'].mode().iloc[0] == sample_dataframe['numeric2'].mode().iloc[0]
    assert result['categorical'].mode().iloc[0] == sample_dataframe['categorical'].mode().iloc[0]


def test_constant_strategy(sample_dataframe):
    """Test handling missing values with constant strategy."""
    # Test with a single value
    result = handle_missing_values(sample_dataframe, strategy='constant', fill_value=0)
    
    # Check that all numeric columns have missing values filled with 0
    assert result['numeric1'].isna().sum() == 0
    assert result['numeric2'].isna().sum() == 0
    assert result['categorical'].isna().sum() == 0
    
    # Check that the constant values are correct
    assert result.loc[result['numeric1'].isna() == False, 'numeric1'].iloc[0] == 0
    assert result.loc[result['numeric2'].isna() == False, 'numeric2'].iloc[0] == 0
    
    # Test with a dictionary of values
    fill_values = {'numeric1': 100, 'numeric2': 200, 'categorical': 'MISSING'}
    result = handle_missing_values(sample_dataframe, strategy='constant', fill_value=fill_values)
    
    # Check that the constant values are correct
    assert result.loc[result['numeric1'].isna() == False, 'numeric1'].iloc[0] == 100
    assert result.loc[result['numeric2'].isna() == False, 'numeric2'].iloc[0] == 200
    assert result.loc[result['categorical'].isna() == False, 'categorical'].iloc[0] == 'MISSING'


def test_drop_strategy(sample_dataframe):
    """Test handling missing values with drop strategy."""
    result = handle_missing_values(sample_dataframe, strategy='drop')
    
    # Check that all rows with missing values are dropped
    assert result.isna().sum().sum() == 0
    
    # Check that the number of rows is reduced
    assert len(result) < len(sample_dataframe)


def test_invalid_strategy(sample_dataframe):
    """Test that invalid strategy raises ValueError."""
    with pytest.raises(ValueError):
        handle_missing_values(sample_dataframe, strategy='invalid_strategy')


def test_constant_strategy_without_fill_value(sample_dataframe):
    """Test that constant strategy without fill_value raises ValueError."""
    with pytest.raises(ValueError):
        handle_missing_values(sample_dataframe, strategy='constant')


def test_empty_dataframe():
    """Test handling missing values with empty DataFrame."""
    empty_df = pd.DataFrame()
    result = handle_missing_values(empty_df, strategy='mean')
    
    # Check that the result is an empty DataFrame
    assert result.empty
    assert len(result.columns) == 0


def test_dataframe_without_missing_values():
    """Test handling missing values with DataFrame without missing values."""
    df = pd.DataFrame({
        'numeric1': [1, 2, 3, 4, 5],
        'numeric2': [10, 20, 30, 40, 50],
        'categorical': ['A', 'B', 'C', 'D', 'E']
    })
    
    result = handle_missing_values(df, strategy='mean')
    
    # Check that the result is identical to the input
    pd.testing.assert_frame_equal(result, df) 
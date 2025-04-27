"""
Tests for the DataInspector module.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from thinkml.inspector import DataInspector


@pytest.fixture
def sample_data():
    """Create a sample DataFrame with various data issues."""
    # Create a DataFrame with missing values
    data = pd.DataFrame({
        'numeric': [1, 2, np.nan, 4, 5],
        'categorical': ['A', 'B', np.nan, 'D', 'E'],
        'mixed_types': [1, '2', 3, '4', 5],
        'unicode': ['normal', 'émoji', 'unicode', 'text', 'data'],
        'special_chars': ['col1', 'col-2', 'col@3', 'col#4', 'col$5'],
        'datetime': pd.date_range(start='2023-01-01', periods=5),
        'nested_dict': [
            {'a': 1, 'b': 2},
            {'a': 3, 'b': 4},
            None,
            {'a': 5, 'b': 6},
            {'a': 7, 'b': 8}
        ],
        'nested_list': [[1, 2], [3, 4], None, [5, 6], [7, 8]],
        'correlated1': [1, 2, 3, 4, 5],
        'correlated2': [2, 4, 6, 8, 10],  # Highly correlated with correlated1
        'imbalanced': ['A', 'A', 'A', 'A', 'B'],  # Imbalanced classes
        'sparse': [0, 0, 0, 1, 0]  # Sparse column
    })
    
    # Introduce some outliers
    data.loc[0, 'numeric'] = 100  # Outlier
    
    # Introduce some missing dates
    data.loc[2, 'datetime'] = np.nan
    
    return data


@pytest.fixture
def inspector():
    """Create a DataInspector instance."""
    return DataInspector()


def test_inspect_data(inspector, sample_data):
    """Test the inspect_data method."""
    results = inspector.inspect_data(sample_data)
    
    # Check basic dataset info
    assert results['shape'] == (5, 12)
    assert len(results['columns']) == 12
    assert isinstance(results['dtypes'], dict)
    
    # Check missing data detection
    assert results['missing_data']['has_missing']
    assert 'numeric' in results['missing_data']['columns_with_missing']
    assert 'categorical' in results['missing_data']['columns_with_missing']
    
    # Check outlier detection
    assert results['outliers']['has_outliers']
    assert 'numeric' in results['outliers']['columns_with_outliers']
    
    # Check mixed types detection
    assert results['mixed_types']['has_mixed_types']
    assert 'mixed_types' in results['mixed_types']['mixed_type_columns']
    
    # Check unicode issues detection
    assert results['unicode_issues']['has_unicode_issues']
    assert 'unicode' in results['unicode_issues']['unicode_issues_by_column']
    
    # Check special characters detection
    assert results['special_chars']['has_special_chars']
    assert 'special_chars' in results['special_chars']['columns_with_special_chars']
    
    # Check time series issues detection
    assert results['time_series_issues']['has_time_series_issues']
    assert 'datetime' in results['time_series_issues']['datetime_columns']
    assert results['time_series_issues']['missing_dates']
    
    # Check nested data detection
    assert results['nested_data']['has_nested_data']
    assert 'nested_dict' in results['nested_data']['nested_columns']
    assert 'nested_list' in results['nested_data']['nested_columns']
    
    # Check correlations detection
    assert results['correlations']['has_high_correlations']
    assert len(results['correlations']['high_correlation_pairs']) > 0
    
    # Check imbalanced dataset detection
    assert results['imbalanced']['is_imbalanced']
    assert results['imbalanced']['target_column'] == 'imbalanced'
    
    # Check sparse dataset detection
    assert results['sparse']['is_sparse']
    assert 'sparse' in results['sparse']['sparsity_by_column']


def test_auto_fix_data(inspector, sample_data):
    """Test the auto_fix_data method."""
    fixed_data, fixes = inspector.auto_fix_data(sample_data)
    
    # Check missing data fixes
    assert 'missing_data' in fixes
    assert len(fixes['missing_data']['columns_fixed']) > 0
    
    # Check outlier fixes
    assert 'outliers' in fixes
    assert len(fixes['outliers']['columns_fixed']) > 0
    
    # Check mixed types fixes
    assert 'mixed_types' in fixes
    assert len(fixes['mixed_types']['columns_fixed']) > 0
    
    # Check unicode fixes
    assert 'unicode_issues' in fixes
    assert len(fixes['unicode_issues']['columns_fixed']) > 0
    
    # Check special characters fixes
    assert 'special_chars' in fixes
    assert len(fixes['special_chars']['columns_renamed']) > 0
    
    # Check time series fixes
    assert 'time_series_issues' in fixes
    assert len(fixes['time_series_issues']['columns_fixed']) > 0
    
    # Check nested data fixes
    assert 'nested_data' in fixes
    assert len(fixes['nested_data']['columns_flattened']) > 0
    
    # Check correlations fixes
    assert 'correlations' in fixes
    assert len(fixes['correlations']['columns_removed']) > 0
    
    # Check imbalanced fixes
    assert 'imbalanced' in fixes
    assert fixes['imbalanced']['method_applied'] == 'class_weights'
    
    # Check sparse fixes
    assert 'sparse' in fixes
    assert len(fixes['sparse']['columns_optimized']) > 0
    
    # Verify that the fixed data has no missing values
    assert not fixed_data.isnull().any().any()
    
    # Verify that outliers are capped
    assert fixed_data['numeric'].max() < 100
    
    # Verify that mixed types are converted to strings
    assert all(isinstance(x, str) for x in fixed_data['mixed_types'])
    
    # Verify that unicode is normalized
    assert 'émoji' not in fixed_data['unicode'].values
    
    # Verify that special characters are removed from column names
    assert all(col.isidentifier() for col in fixed_data.columns)
    
    # Verify that missing dates are filled
    assert not fixed_data['datetime'].isnull().any()
    
    # Verify that nested data is flattened
    assert 'nested_dict_a' in fixed_data.columns
    assert 'nested_dict_b' in fixed_data.columns
    
    # Verify that highly correlated columns are removed
    assert 'correlated2' not in fixed_data.columns
    
    # Verify that sparse columns are optimized
    assert isinstance(fixed_data['sparse'].dtype, pd.SparseDtype)


def test_generate_report(inspector, sample_data, tmp_path):
    """Test the generate_report method."""
    # Run inspection and fixes
    inspector.inspect_data(sample_data)
    inspector.auto_fix_data(sample_data)
    
    # Generate report
    report_path = os.path.join(tmp_path, 'report.json')
    report = inspector.generate_report(report_path)
    
    # Check report structure
    assert 'inspection_results' in report
    assert 'fix_results' in report
    assert 'timestamp' in report
    assert 'summary' in report
    
    # Check summary
    assert 'total_issues' in report['summary']
    assert 'issues_fixed' in report['summary']
    assert 'issues_by_type' in report['summary']
    
    # Check if report file was created
    assert os.path.exists(report_path)
    
    # Check report file content
    with open(report_path, 'r') as f:
        saved_report = json.load(f)
    assert saved_report == report


def test_empty_dataset(inspector):
    """Test handling of empty dataset."""
    empty_data = pd.DataFrame()
    results = inspector.inspect_data(empty_data)
    
    assert results['empty_dataset']
    assert 'shape' not in results
    assert 'columns' not in results
    assert 'dtypes' not in results


def test_single_row_dataset(inspector):
    """Test handling of single row dataset."""
    single_row = pd.DataFrame({
        'col1': [1],
        'col2': ['A']
    })
    results = inspector.inspect_data(single_row)
    
    assert results['shape'] == (1, 2)
    assert len(results['columns']) == 2
    assert not results['missing_data']['has_missing']
    assert not results['outliers']['has_outliers']


def test_single_column_dataset(inspector):
    """Test handling of single column dataset."""
    single_col = pd.DataFrame({
        'col1': [1, 2, 3, 4, 5]
    })
    results = inspector.inspect_data(single_col)
    
    assert results['shape'] == (5, 1)
    assert len(results['columns']) == 1
    assert not results['correlations']['has_high_correlations']


def test_all_missing_dataset(inspector):
    """Test handling of dataset with all missing values."""
    all_missing = pd.DataFrame({
        'col1': [np.nan, np.nan, np.nan],
        'col2': [np.nan, np.nan, np.nan]
    })
    results = inspector.inspect_data(all_missing)
    
    assert results['missing_data']['has_missing']
    assert all(col in results['missing_data']['columns_with_missing'] for col in ['col1', 'col2'])
    assert all(results['missing_data']['missing_percentages'][col] == 100.0 for col in ['col1', 'col2'])


def test_extreme_values_dataset(inspector):
    """Test handling of dataset with extreme values."""
    extreme_data = pd.DataFrame({
        'normal': [1, 2, 3, 4, 5],
        'extreme': [1e10, 1e20, 1e30, 1e40, 1e50]
    })
    results = inspector.inspect_data(extreme_data)
    
    assert results['outliers']['has_outliers']
    assert 'extreme' in results['outliers']['columns_with_outliers']
    
    # Test fixing extreme values
    fixed_data, fixes = inspector.auto_fix_data(extreme_data)
    assert 'extreme' in fixes['outliers']['columns_fixed']
    assert fixed_data['extreme'].max() < 1e50


def test_mixed_data_types_dataset(inspector):
    """Test handling of dataset with mixed data types."""
    mixed_data = pd.DataFrame({
        'mixed': [1, '2', 3.0, True, None]
    })
    results = inspector.inspect_data(mixed_data)
    
    assert results['mixed_types']['has_mixed_types']
    assert 'mixed' in results['mixed_types']['mixed_type_columns']
    
    # Test fixing mixed types
    fixed_data, fixes = inspector.auto_fix_data(mixed_data)
    assert 'mixed' in fixes['mixed_types']['columns_fixed']
    assert all(isinstance(x, str) for x in fixed_data['mixed'].dropna())


def test_unicode_dataset(inspector):
    """Test handling of dataset with unicode characters."""
    unicode_data = pd.DataFrame({
        'text': ['normal', 'émoji', 'unicode', 'text', 'data']
    })
    results = inspector.inspect_data(unicode_data)
    
    assert results['unicode_issues']['has_unicode_issues']
    assert 'text' in results['unicode_issues']['unicode_issues_by_column']
    
    # Test fixing unicode issues
    fixed_data, fixes = inspector.auto_fix_data(unicode_data)
    assert 'text' in fixes['unicode_issues']['columns_fixed']
    assert 'émoji' not in fixed_data['text'].values


def test_special_chars_dataset(inspector):
    """Test handling of dataset with special characters in column names."""
    special_chars_data = pd.DataFrame({
        'col-1': [1, 2, 3],
        'col@2': [4, 5, 6],
        'col#3': [7, 8, 9]
    })
    results = inspector.inspect_data(special_chars_data)
    
    assert results['special_chars']['has_special_chars']
    assert all(col in results['special_chars']['columns_with_special_chars'] for col in ['col-1', 'col@2', 'col#3'])
    
    # Test fixing special characters
    fixed_data, fixes = inspector.auto_fix_data(special_chars_data)
    assert len(fixes['special_chars']['columns_renamed']) > 0
    assert all(col.isidentifier() for col in fixed_data.columns)


def test_time_series_dataset(inspector):
    """Test handling of time series dataset."""
    # Create a time series with missing dates and irregular intervals
    dates = pd.date_range(start='2023-01-01', periods=5, freq='D')
    dates = dates.drop(dates[2])  # Remove one date
    time_series_data = pd.DataFrame({
        'date': dates,
        'value': [1, 2, 4, 5]
    })
    results = inspector.inspect_data(time_series_data)
    
    assert results['time_series_issues']['has_time_series_issues']
    assert 'date' in results['time_series_issues']['datetime_columns']
    assert results['time_series_issues']['missing_dates']
    assert results['time_series_issues']['irregular_intervals']
    
    # Test fixing time series issues
    fixed_data, fixes = inspector.auto_fix_data(time_series_data)
    assert 'date' in fixes['time_series_issues']['columns_fixed']
    assert len(fixed_data) == 5  # Should have all dates
    assert not fixed_data['date'].isnull().any()


def test_nested_data_dataset(inspector):
    """Test handling of dataset with nested data structures."""
    nested_data = pd.DataFrame({
        'dict_col': [
            {'a': 1, 'b': 2},
            {'a': 3, 'b': 4},
            None,
            {'a': 5, 'b': 6}
        ],
        'list_col': [[1, 2], [3, 4], None, [5, 6]]
    })
    results = inspector.inspect_data(nested_data)
    
    assert results['nested_data']['has_nested_data']
    assert 'dict_col' in results['nested_data']['nested_columns']
    assert 'list_col' in results['nested_data']['nested_columns']
    
    # Test fixing nested data
    fixed_data, fixes = inspector.auto_fix_data(nested_data)
    assert 'dict_col' in fixes['nested_data']['columns_flattened']
    assert 'list_col' in fixes['nested_data']['columns_flattened']
    assert 'dict_col_a' in fixed_data.columns
    assert 'dict_col_b' in fixed_data.columns
    assert all(isinstance(x, str) for x in fixed_data['list_col'].dropna())


def test_highly_correlated_dataset(inspector):
    """Test handling of dataset with highly correlated features."""
    correlated_data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 4, 6, 8, 10],  # Perfect correlation
        'feature3': [1, 3, 5, 7, 9]   # High correlation
    })
    results = inspector.inspect_data(correlated_data)
    
    assert results['correlations']['has_high_correlations']
    assert len(results['correlations']['high_correlation_pairs']) > 0
    
    # Test fixing correlations
    fixed_data, fixes = inspector.auto_fix_data(correlated_data)
    assert len(fixes['correlations']['columns_removed']) > 0
    assert len(fixed_data.columns) < 3  # At least one column should be removed


def test_imbalanced_dataset(inspector):
    """Test handling of imbalanced dataset."""
    imbalanced_data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [6, 7, 8, 9, 10],
        'target': ['A', 'A', 'A', 'A', 'B']  # 80% class A, 20% class B
    })
    results = inspector.inspect_data(imbalanced_data)
    
    assert results['imbalanced']['is_imbalanced']
    assert results['imbalanced']['target_column'] == 'target'
    assert results['imbalanced']['imbalance_ratio'] == 4.0
    
    # Test fixing imbalanced data
    fixed_data, fixes = inspector.auto_fix_data(imbalanced_data)
    assert fixes['imbalanced']['method_applied'] == 'class_weights'
    assert 'target' in fixes['imbalanced']['class_weights']


def test_sparse_dataset(inspector):
    """Test handling of sparse dataset."""
    sparse_data = pd.DataFrame({
        'feature1': [0, 0, 0, 1, 0],  # 80% zeros
        'feature2': [0, 1, 0, 0, 0],  # 80% zeros
        'feature3': [1, 1, 1, 1, 1]   # No zeros
    })
    results = inspector.inspect_data(sparse_data)
    
    assert results['sparse']['is_sparse']
    assert 'feature1' in results['sparse']['sparsity_by_column']
    assert 'feature2' in results['sparse']['sparsity_by_column']
    assert results['sparse']['sparsity_by_column']['feature1'] == 0.8
    
    # Test fixing sparse data
    fixed_data, fixes = inspector.auto_fix_data(sparse_data)
    assert len(fixes['sparse']['columns_optimized']) > 0
    assert isinstance(fixed_data['feature1'].dtype, pd.SparseDtype)
    assert isinstance(fixed_data['feature2'].dtype, pd.SparseDtype)
    assert not isinstance(fixed_data['feature3'].dtype, pd.SparseDtype) 
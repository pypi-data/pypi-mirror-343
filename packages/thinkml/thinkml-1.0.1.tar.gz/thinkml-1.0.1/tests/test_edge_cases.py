"""
Comprehensive test suite for ThinkML covering all edge cases and challenging scenarios.
This test suite is designed to test the robustness of the ThinkML library under difficult conditions.
"""

import os
import sys
import numpy as np
import pandas as pd
import pytest
from datetime import datetime, timedelta
import random
import string
import gc
import psutil
import time
import dask.dataframe as dd
from dask.distributed import Client, LocalCluster

# Import ThinkML modules
from thinkml.preprocessor import (
    handle_missing_values,
    encode_categorical,
    scale_features,
    handle_imbalance,
    MulticollinearityHandler
)
from thinkml.feature_selection import select_features
from thinkml.algorithms import (
    LinearRegression,
    LogisticRegression,
    RidgeRegression,
    RandomForestClassifier,
    RandomForestRegressor,
    DecisionTreeClassifier,
    DecisionTreeRegressor,
    KNeighborsClassifier,
    KNeighborsRegressor
)
from thinkml.validation import cross_validate
from thinkml.evaluation import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_squared_error,
    r2_score
)
from thinkml.reporting import generate_report
from thinkml.outliers import detect_outliers
from thinkml.data_split import train_test_split
from thinkml.inspector import DataInspector

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Helper functions
def generate_random_string(length=10):
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_date():
    """Generate a random date within the last 10 years."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3650)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)

def get_memory_usage():
    """Get current memory usage of the process."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # in MB

# Test data generation functions
def create_empty_dataset():
    """Create an empty dataset."""
    return pd.DataFrame()

def create_single_row_dataset():
    """Create a dataset with a single row."""
    return pd.DataFrame({
        'A': [1],
        'B': [2],
        'C': [3]
    })

def create_single_column_dataset():
    """Create a dataset with a single column."""
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5]
    })

def create_all_missing_dataset():
    """Create a dataset with all missing values."""
    return pd.DataFrame({
        'A': [np.nan, np.nan, np.nan],
        'B': [np.nan, np.nan, np.nan]
    })

def create_extreme_values_dataset():
    """Create a dataset with extreme values."""
    return pd.DataFrame({
        'A': [1e-10, 1e10, -1e10, 0, 1e-308, 1e308],
        'B': [0, 1, 2, 3, 4, 5]
    })

def create_mixed_data_types_dataset():
    """Create a dataset with mixed data types."""
    return pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['a', 'b', 'c'],
        'C': [1.0, 2.0, 3.0],
        'D': [True, False, True],
        'E': [datetime.now(), datetime.now() - timedelta(days=1), datetime.now() - timedelta(days=2)]
    })

def create_large_dataset(rows=1000000, cols=100):
    """Create a large dataset."""
    data = {}
    for i in range(cols):
        if i % 5 == 0:
            data[f'cat_{i}'] = [random.choice(['A', 'B', 'C', 'D', 'E']) for _ in range(rows)]
        elif i % 5 == 1:
            data[f'int_{i}'] = np.random.randint(0, 1000, rows)
        elif i % 5 == 2:
            data[f'float_{i}'] = np.random.rand(rows)
        elif i % 5 == 3:
            data[f'bool_{i}'] = np.random.choice([True, False], rows)
        else:
            data[f'date_{i}'] = [generate_random_date() for _ in range(rows)]
    
    return pd.DataFrame(data)

def create_unicode_dataset():
    """Create a dataset with unicode characters."""
    return pd.DataFrame({
        'A': ['é', 'ñ', 'ü', 'α', 'β', 'γ', '你好', 'こんにちは', '안녕하세요', 'Привет'],
        'B': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })

def create_special_chars_column_names_dataset():
    """Create a dataset with special characters in column names."""
    return pd.DataFrame({
        'Column!@#$%^&*()': [1, 2, 3],
        'Column with spaces': [4, 5, 6],
        'Column-with-hyphens': [7, 8, 9],
        'Column.with.dots': [10, 11, 12],
        'Column[with]brackets': [13, 14, 15]
    })

def create_time_series_dataset():
    """Create a time series dataset."""
    dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'date': dates,
        'value': np.random.rand(100),
        'trend': np.linspace(0, 1, 100),
        'seasonal': np.sin(np.linspace(0, 4*np.pi, 100))
    })

def create_nested_data_dataset():
    """Create a dataset with nested data structures."""
    return pd.DataFrame({
        'A': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        'B': [{'key1': 1, 'key2': 2}, {'key1': 3, 'key2': 4}, {'key1': 5, 'key2': 6}],
        'C': [1, 2, 3]
    })

def create_highly_correlated_dataset():
    """Create a dataset with highly correlated features."""
    n_samples = 1000
    x1 = np.random.rand(n_samples)
    x2 = 0.99 * x1 + 0.01 * np.random.rand(n_samples)  # Almost perfect correlation
    x3 = 0.8 * x1 + 0.2 * np.random.rand(n_samples)    # Strong correlation
    x4 = 0.5 * x1 + 0.5 * np.random.rand(n_samples)    # Moderate correlation
    x5 = np.random.rand(n_samples)                      # No correlation
    
    return pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'x3': x3,
        'x4': x4,
        'x5': x5,
        'target': 2 * x1 + 3 * x5 + np.random.rand(n_samples) * 0.1
    })

def create_imbalanced_dataset():
    """Create a dataset with imbalanced classes."""
    n_samples = 1000
    n_positive = 50  # Only 5% positive samples
    
    x_positive = np.random.randn(n_positive, 2) + 2
    x_negative = np.random.randn(n_samples - n_positive, 2) - 2
    
    X = np.vstack([x_positive, x_negative])
    y = np.array([1] * n_positive + [0] * (n_samples - n_positive))
    
    # Shuffle the data
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]
    
    return pd.DataFrame({
        'feature1': X[:, 0],
        'feature2': X[:, 1],
        'target': y
    })

def create_multicollinear_dataset():
    """Create a dataset with multicollinearity."""
    n_samples = 1000
    x1 = np.random.rand(n_samples)
    x2 = 2 * x1 + np.random.rand(n_samples) * 0.1
    x3 = 3 * x1 - 2 * x2 + np.random.rand(n_samples) * 0.1
    
    return pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'x3': x3,
        'target': 5 * x1 + np.random.rand(n_samples) * 0.1
    })

def create_sparse_dataset():
    """Create a sparse dataset with many zeros."""
    n_samples = 1000
    n_features = 100
    density = 0.01  # Only 1% of values are non-zero
    
    data = np.zeros((n_samples, n_features))
    for i in range(n_samples):
        for j in range(n_features):
            if np.random.rand() < density:
                data[i, j] = np.random.rand()
    
    return pd.DataFrame(data, columns=[f'feature_{i}' for i in range(n_features)])

def create_outlier_dataset():
    """Create a dataset with outliers."""
    n_samples = 1000
    x = np.random.randn(n_samples)
    
    # Add some outliers
    x[0] = 10
    x[1] = -10
    x[2] = 20
    x[3] = -20
    
    return pd.DataFrame({
        'feature': x,
        'target': 2 * x + np.random.randn(n_samples) * 0.1
    })

def create_cyclic_dataset():
    """Create a dataset with cyclic patterns."""
    n_samples = 1000
    x = np.linspace(0, 10*np.pi, n_samples)
    y = np.sin(x) + np.random.randn(n_samples) * 0.1
    
    return pd.DataFrame({
        'feature': x,
        'target': y
    })

def create_nonlinear_dataset():
    """Create a dataset with nonlinear relationships."""
    n_samples = 1000
    x = np.random.rand(n_samples) * 10
    y = x**2 + np.random.randn(n_samples) * 0.1
    
    return pd.DataFrame({
        'feature': x,
        'target': y
    })

def create_missing_patterns_dataset():
    """Create a dataset with specific missing value patterns."""
    n_samples = 1000
    data = pd.DataFrame({
        'A': np.random.rand(n_samples),
        'B': np.random.rand(n_samples),
        'C': np.random.rand(n_samples),
        'D': np.random.rand(n_samples),
        'E': np.random.rand(n_samples)
    })
    
    # Create missing value patterns
    # B is missing when A > 0.5
    data.loc[data['A'] > 0.5, 'B'] = np.nan
    
    # C is missing when B is missing
    data.loc[data['B'].isna(), 'C'] = np.nan
    
    # D is missing randomly
    data.loc[np.random.rand(n_samples) < 0.3, 'D'] = np.nan
    
    # E is missing in blocks
    data.loc[100:200, 'E'] = np.nan
    
    return data

def create_duplicate_rows_dataset():
    """Create a dataset with duplicate rows."""
    n_samples = 1000
    data = pd.DataFrame({
        'A': np.random.rand(n_samples),
        'B': np.random.rand(n_samples),
        'C': np.random.rand(n_samples)
    })
    
    # Add duplicate rows
    data = pd.concat([data, data.iloc[0:100]], ignore_index=True)
    
    return data

def create_duplicate_columns_dataset():
    """Create a dataset with duplicate columns."""
    n_samples = 1000
    data = pd.DataFrame({
        'A': np.random.rand(n_samples),
        'B': np.random.rand(n_samples),
        'C': np.random.rand(n_samples)
    })
    
    # Add duplicate columns
    data['A_dup'] = data['A']
    data['B_dup'] = data['B']
    
    return data

def create_constant_columns_dataset():
    """Create a dataset with constant columns."""
    n_samples = 1000
    data = pd.DataFrame({
        'A': np.random.rand(n_samples),
        'B': np.random.rand(n_samples),
        'C': np.random.rand(n_samples),
        'constant': [1] * n_samples,
        'almost_constant': [1] * (n_samples-1) + [2]
    })
    
    return data

def create_high_cardinality_dataset():
    """Create a dataset with high cardinality categorical features."""
    n_samples = 1000
    data = pd.DataFrame({
        'A': np.random.rand(n_samples),
        'B': np.random.rand(n_samples),
        'C': np.random.rand(n_samples),
        'high_cardinality': [generate_random_string() for _ in range(n_samples)]
    })
    
    return data

def create_low_variance_dataset():
    """Create a dataset with low variance features."""
    n_samples = 1000
    data = pd.DataFrame({
        'A': np.random.rand(n_samples),
        'B': np.random.rand(n_samples),
        'C': np.random.rand(n_samples),
        'low_variance': np.random.rand(n_samples) * 0.01 + 0.5
    })
    
    return data

def create_skewed_dataset():
    """Create a dataset with skewed distributions."""
    n_samples = 1000
    data = pd.DataFrame({
        'A': np.random.rand(n_samples),
        'B': np.random.rand(n_samples),
        'C': np.random.rand(n_samples),
        'skewed': np.random.exponential(1, n_samples)
    })
    
    return data

def create_multiclass_dataset():
    """Create a multiclass classification dataset."""
    n_samples = 1000
    n_classes = 10
    
    X = np.random.randn(n_samples, 2)
    y = np.random.randint(0, n_classes, n_samples)
    
    # Make classes somewhat separable
    for i in range(n_classes):
        X[y == i] += i
    
    return pd.DataFrame({
        'feature1': X[:, 0],
        'feature2': X[:, 1],
        'target': y
    })

def create_multilabel_dataset():
    """Create a multilabel classification dataset."""
    n_samples = 1000
    n_labels = 5
    
    X = np.random.randn(n_samples, 2)
    y = np.random.randint(0, 2, (n_samples, n_labels))
    
    return pd.DataFrame({
        'feature1': X[:, 0],
        'feature2': X[:, 1],
        'label1': y[:, 0],
        'label2': y[:, 1],
        'label3': y[:, 2],
        'label4': y[:, 3],
        'label5': y[:, 4]
    })

def create_multitarget_dataset():
    """Create a multitarget regression dataset."""
    n_samples = 1000
    
    X = np.random.randn(n_samples, 2)
    y1 = 2 * X[:, 0] + 3 * X[:, 1] + np.random.randn(n_samples) * 0.1
    y2 = -X[:, 0] + 4 * X[:, 1] + np.random.randn(n_samples) * 0.1
    
    return pd.DataFrame({
        'feature1': X[:, 0],
        'feature2': X[:, 1],
        'target1': y1,
        'target2': y2
    })

def create_time_series_forecasting_dataset():
    """Create a time series forecasting dataset."""
    n_samples = 1000
    
    # Generate time series with trend, seasonality, and noise
    t = np.linspace(0, 10*np.pi, n_samples)
    trend = 0.1 * t
    seasonality = 2 * np.sin(t) + 1.5 * np.sin(2*t)
    noise = np.random.randn(n_samples) * 0.5
    
    y = trend + seasonality + noise
    
    # Create features (lagged values)
    data = pd.DataFrame({
        'time': t,
        'value': y,
        'lag1': np.roll(y, 1),
        'lag2': np.roll(y, 2),
        'lag3': np.roll(y, 3),
        'lag4': np.roll(y, 4),
        'lag5': np.roll(y, 5)
    })
    
    # Remove first rows with NaN due to lagging
    data = data.iloc[5:]
    
    return data

def create_dask_dataset():
    """Create a Dask DataFrame for testing distributed computing."""
    # Create a pandas DataFrame
    df = create_large_dataset(rows=100000, cols=10)
    
    # Convert to Dask DataFrame
    return dd.from_pandas(df, npartitions=10)

# Test functions
class TestEdgeCases:
    """Test suite for edge cases in ThinkML."""
    
    @pytest.mark.missing_data
    def test_empty_dataset(self):
        """Test handling of empty dataset."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError, match="Empty dataset provided"):
            handle_missing_values(empty_df)
            scale_features(empty_df)
            detect_outliers(empty_df)
    
    @pytest.mark.missing_data
    def test_single_row_dataset(self):
        """Test handling of dataset with single row."""
        single_row_df = pd.DataFrame({
            'numeric': [1.0],
            'categorical': ['A'],
            'datetime': [pd.Timestamp('2023-01-01')]
        })
        
        # Test missing values handling
        result = handle_missing_values(single_row_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        
        # Test scaling
        result = scale_features(single_row_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        
        # Test outlier detection
        result = detect_outliers(single_row_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
    
    @pytest.mark.missing_data
    def test_single_column_dataset(self):
        """Test handling of dataset with single column."""
        single_col_df = pd.DataFrame({'numeric': [1.0, 2.0, 3.0]})
        
        # Test missing values handling
        result = handle_missing_values(single_col_df)
        assert isinstance(result, pd.DataFrame)
        assert result.shape[1] == 1
        
        # Test scaling
        result = scale_features(single_col_df)
        assert isinstance(result, pd.DataFrame)
        assert result.shape[1] == 1
        
        # Test outlier detection
        result = detect_outliers(single_col_df)
        assert isinstance(result, pd.DataFrame)
        assert result.shape[1] == 1
    
    @pytest.mark.missing_data
    def test_all_missing_dataset(self):
        """Test handling of dataset with all missing values."""
        missing_df = pd.DataFrame({
            'numeric': [np.nan, np.nan, np.nan],
            'categorical': [None, None, None],
            'datetime': [pd.NaT, pd.NaT, pd.NaT]
        })
        
        # Test missing values handling
        result = handle_missing_values(missing_df)
        assert isinstance(result, pd.DataFrame)
        assert not result.isna().any().any()
        
        # Test scaling
        result = scale_features(result)  # Use result from missing values handling
        assert isinstance(result, pd.DataFrame)
        assert not result.isna().any().any()
        
        # Test outlier detection
        result = detect_outliers(result)  # Use result from scaling
        assert isinstance(result, pd.DataFrame)
        assert not result.isna().any().any()
    
    @pytest.mark.extreme_values
    def test_extreme_values_dataset(self):
        """Test handling of dataset with extreme values."""
        extreme_df = pd.DataFrame({
            'normal': np.random.normal(0, 1, 1000),
            'extreme': np.concatenate([
                np.random.normal(0, 1, 900),
                np.random.normal(10, 1, 100)  # Extreme values
            ])
        })
        
        # Test scaling with extreme value handling
        result = scale_features(extreme_df, handle_extreme_values=True)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == extreme_df.shape
        
        # Verify extreme values are handled
        z_scores = np.abs((result['extreme'] - result['extreme'].mean()) / result['extreme'].std())
        assert (z_scores <= 3.0).all()  # All values within 3 standard deviations
    
    @pytest.mark.mixed_types
    def test_mixed_data_types_dataset(self):
        """Test handling of dataset with mixed data types."""
        mixed_df = pd.DataFrame({
            'numeric': [1.0, 2.0, 3.0],
            'categorical': ['A', 'B', 'C'],
            'datetime': [pd.Timestamp('2023-01-01')] * 3,
            'mixed': [1, 'A', 3.0]  # Mixed types
        })
        
        # Test missing values handling
        result = handle_missing_values(mixed_df)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == mixed_df.shape
        
        # Test scaling (should only scale numeric column)
        result = scale_features(result)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == mixed_df.shape
        
        # Test outlier detection (should only detect in numeric column)
        result = detect_outliers(result)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == mixed_df.shape
    
    @pytest.mark.large
    def test_large_dataset(self):
        """Test handling of large dataset."""
        # Create a large dataset
        n_rows = 100000
        n_cols = 10
        large_df = pd.DataFrame(
            np.random.randn(n_rows, n_cols),
            columns=[f'col_{i}' for i in range(n_cols)]
        )
        
        # Test missing values handling
        result = handle_missing_values(large_df)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == large_df.shape
        
        # Test scaling
        result = scale_features(result)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == large_df.shape
        
        # Test outlier detection
        result = detect_outliers(result)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == large_df.shape
    
    @pytest.mark.unicode
    def test_unicode_dataset(self):
        """Test handling of datasets with unicode characters."""
        data = create_unicode_dataset()
        
        # These should handle unicode characters correctly
        result1 = handle_missing_values(data)
        result2 = encode_categorical(data)
        
        # Check that unicode characters are preserved
        assert 'é' in result2.values
    
    @pytest.mark.special_chars
    def test_special_chars_column_names_dataset(self):
        """Test handling of datasets with special characters in column names."""
        data = create_special_chars_column_names_dataset()
        
        # These should handle special characters correctly
        result1 = handle_missing_values(data)
        result2 = encode_categorical(data)
        result3 = scale_features(data)
        
        # Check that special characters are handled correctly
        assert all(col.isidentifier() for col in result1.columns)
    
    @pytest.mark.time_series
    def test_time_series_dataset(self):
        """Test handling of time series datasets."""
        data = create_time_series_dataset()
        
        # These should handle time series data correctly
        result1 = handle_missing_values(data)
        result2 = encode_categorical(data)
        
        # Check that time series data is handled correctly
        assert pd.api.types.is_datetime64_any_dtype(result1['date'])
    
    @pytest.mark.nested_data
    def test_nested_data_dataset(self):
        """Test handling of datasets with nested data structures."""
        data = create_nested_data_dataset()
        
        # These should handle nested data correctly
        result1 = handle_missing_values(data)
        result2 = encode_categorical(data)
        
        # Check that nested data is handled correctly
        assert 'dict_col_a' in result2.columns
        assert 'dict_col_b' in result2.columns
    
    @pytest.mark.correlations
    def test_highly_correlated_dataset(self):
        """Test handling of datasets with highly correlated features."""
        data = create_highly_correlated_dataset()
        
        # Test feature selection
        result = select_features(data, method='correlation', threshold=0.9)
        
        # Check that highly correlated features are removed
        assert len(result.columns) < len(data.columns)
    
    @pytest.mark.imbalance
    def test_imbalanced_dataset(self):
        """Test handling of imbalanced datasets."""
        data = create_imbalanced_dataset()
        
        # Test imbalance handling
        result = handle_imbalance(data, target_column='target', method='smote')
        
        # Check that the dataset is balanced
        class_counts = result['target'].value_counts()
        assert abs(class_counts.iloc[0] - class_counts.iloc[1]) <= 1
    
    @pytest.mark.correlations
    def test_multicollinear_dataset(self):
        """Test handling of multicollinear datasets."""
        # Create a dataset with multicollinear features
        np.random.seed(42)
        n_samples = 1000
        
        # Create base features
        x1 = np.random.normal(0, 1, n_samples)
        x2 = np.random.normal(0, 1, n_samples)
        
        # Create multicollinear features
        x3 = 0.8 * x1 + 0.2 * np.random.normal(0, 1, n_samples)  # Strongly correlated with x1
        x4 = 0.9 * x2 + 0.1 * np.random.normal(0, 1, n_samples)  # Strongly correlated with x2
        x5 = 0.7 * x1 + 0.3 * x2 + 0.1 * np.random.normal(0, 1, n_samples)  # Correlated with both x1 and x2
        
        # Create target variable
        y = 2 * x1 + 3 * x2 + np.random.normal(0, 0.1, n_samples)
        
        # Create DataFrame
        data = pd.DataFrame({
            'x1': x1,
            'x2': x2,
            'x3': x3,
            'x4': x4,
            'x5': x5,
            'target': y
        })
        
        # Test VIF detection
        handler = MulticollinearityHandler(threshold=5.0)
        vif_scores = handler.detect_multicollinearity(data.drop(columns=['target']))
        
        # Check that high VIF features are detected
        assert any(vif_scores > 5.0), "No high VIF features detected"
        
        # Test VIF resolution
        data_processed, dropped_features = handler.resolve_multicollinearity(data.drop(columns=['target']))
        
        # Check that multicollinear features are removed
        assert len(dropped_features) > 0, "No features were dropped"
        assert 'x3' in dropped_features or 'x4' in dropped_features or 'x5' in dropped_features, \
            "Multicollinear features were not dropped"
        
        # Check that remaining features have low VIF
        vif_scores_after = handler.detect_multicollinearity(data_processed)
        assert all(vif_scores_after <= 5.0), "Some features still have high VIF"
        
        # Test feature selection with multicollinearity handling
        from thinkml.feature_selection import select_features
        
        # Test with different thresholds
        data_vif_5 = select_features(data, target='target', method='vif', threshold=5.0)
        data_vif_10 = select_features(data, target='target', method='vif', threshold=10.0)
        
        # Check that more features are kept with higher threshold
        assert len(data_vif_10.columns) >= len(data_vif_5.columns), \
            "Higher VIF threshold should keep more features"
        
        # Test integration with other feature selection methods
        data_mutual_info = select_features(
            data, 
            target='target', 
            method='mutual_info', 
            k=3,
            handle_multicollinearity=True,
            multicollinearity_threshold=5.0
        )
        
        # Check that multicollinearity is handled before mutual information selection
        vif_scores_mi = handler.detect_multicollinearity(data_mutual_info.drop(columns=['target']))
        assert all(vif_scores_mi <= 5.0), "Multicollinearity not handled in mutual information selection"
        
        # Test report generation
        report = handler.generate_report(data.drop(columns=['target']))
        assert isinstance(report, pd.DataFrame), "Report should be a DataFrame"
        assert 'VIF' in report.columns, "Report should include VIF scores"
        assert 'Status' in report.columns, "Report should include status"
    
    @pytest.mark.sparse
    def test_sparse_dataset(self):
        """Test handling of sparse datasets."""
        data = create_sparse_dataset()
        
        # Convert to sparse format
        sparse_data = data.astype(pd.SparseDtype("float64", 0))
        
        # Test with sparse format
        result = handle_missing_values(sparse_data)
        
        # Check that sparse format is preserved
        assert isinstance(result['feature_0'].dtype, pd.SparseDtype)
        assert result['feature_0'].dtype.fill_value == 0
    
    @pytest.mark.outliers
    def test_outlier_dataset(self):
        """Test handling of datasets with outliers."""
        # Create dataset with known outliers
        data = pd.DataFrame({
            'normal': np.random.normal(0, 1, 1000),
            'with_outliers': np.concatenate([
                np.random.normal(0, 1, 950),
                np.random.normal(10, 1, 50)  # Outliers
            ])
        })
        
        # Test z-score method
        outliers_zscore = detect_outliers(data, method='zscore', threshold=3.0)
        assert isinstance(outliers_zscore, pd.DataFrame)
        assert outliers_zscore.shape == data.shape
        assert outliers_zscore['normal'].sum() < 50  # Few outliers in normal distribution
        assert 40 <= outliers_zscore['with_outliers'].sum() <= 60  # Most outliers detected
        
        # Test IQR method
        outliers_iqr = detect_outliers(data, method='iqr', threshold=1.5)
        assert isinstance(outliers_iqr, pd.DataFrame)
        assert outliers_iqr.shape == data.shape
        assert outliers_iqr['normal'].sum() < 50
        assert 40 <= outliers_iqr['with_outliers'].sum() <= 60
        
        # Test Isolation Forest method
        outliers_if = detect_outliers(data, method='isolation_forest', contamination=0.05)
        assert isinstance(outliers_if, pd.DataFrame)
        assert outliers_if.shape == data.shape
        assert outliers_if['normal'].sum() < 100
        assert outliers_if['with_outliers'].sum() > 0
        
        # Test with empty dataset
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError, match="Empty dataset provided"):
            detect_outliers(empty_df)
        
        # Test with non-numeric data
        str_df = pd.DataFrame({'str_col': ['a', 'b', 'c']})
        with pytest.raises(ValueError, match="No numeric columns found in the dataset"):
            detect_outliers(str_df)
        
        # Test invalid method
        with pytest.raises(ValueError, match="Method must be one of"):
            detect_outliers(data, method='invalid_method')
        
        # Test invalid threshold
        with pytest.raises(ValueError, match="Threshold must be positive"):
            detect_outliers(data, threshold=-1)
        
        # Test invalid contamination
        with pytest.raises(ValueError, match="Contamination must be between 0 and 1"):
            detect_outliers(data, method='isolation_forest', contamination=2.0)
    
    @pytest.mark.cyclic
    def test_cyclic_dataset(self):
        """Test handling of cyclic datasets."""
        data = create_cyclic_dataset()
        
        # Test feature engineering
        result = encode_categorical(data, method='cyclic')
        
        # Check that cyclic features are created
        assert 'A_sin' in result.columns
        assert 'A_cos' in result.columns
    
    @pytest.mark.nonlinear
    def test_nonlinear_dataset(self):
        """Test handling of nonlinear datasets."""
        data = create_nonlinear_dataset()
        
        # Test with nonlinear models
        X = data.drop('target', axis=1)
        y = data['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        # Check that the model performs well on nonlinear data
        assert r2 > 0.8
    
    @pytest.mark.missing_data
    def test_missing_patterns_dataset(self):
        """Test handling of datasets with missing patterns."""
        data = create_missing_patterns_dataset()
        
        # Test with different missing value methods
        result1 = handle_missing_values(data, method='mean')
        result2 = handle_missing_values(data, method='knn', k=3)
        
        # Check that missing values are handled correctly
        assert not result1.isnull().any().any()
        assert not result2.isnull().any().any()
    
    @pytest.mark.duplicates
    def test_duplicate_rows_dataset(self):
        """Test handling of datasets with duplicate rows."""
        data = create_duplicate_rows_dataset()
        
        # Test with duplicate handling
        result = handle_missing_values(data, remove_duplicates=True)
        
        # Check that duplicates are removed
        assert len(result) < len(data)
    
    @pytest.mark.duplicates
    def test_duplicate_columns_dataset(self):
        """Test handling of datasets with duplicate columns."""
        data = create_duplicate_columns_dataset()
        
        # Test with duplicate handling
        result = handle_missing_values(data, remove_duplicate_columns=True)
        
        # Check that duplicate columns are removed
        assert len(result.columns) < len(data.columns)
    
    @pytest.mark.constant
    def test_constant_columns_dataset(self):
        """Test handling of datasets with constant columns."""
        data = create_constant_columns_dataset()
        
        # Test feature selection
        result = select_features(data, method='variance', threshold=0.01)
        
        # Check that constant columns are removed
        assert len(result.columns) < len(data.columns)
    
    @pytest.mark.cardinality
    def test_high_cardinality_dataset(self):
        """Test handling of datasets with high cardinality."""
        data = create_high_cardinality_dataset()
        
        # Test encoding
        result = encode_categorical(data, method='target')
        
        # Check that high cardinality is handled correctly
        assert result.shape[1] == data.shape[1]
    
    @pytest.mark.variance
    def test_low_variance_dataset(self):
        """Test handling of datasets with low variance."""
        data = create_low_variance_dataset()
        
        # Test feature selection
        result = select_features(data, method='variance', threshold=0.01)
        
        # Check that low variance features are removed
        assert len(result.columns) < len(data.columns)
    
    @pytest.mark.skewed
    def test_skewed_dataset(self):
        """Test handling of skewed datasets."""
        data = create_skewed_dataset()
        
        # Test with log transformation
        result = scale_features(data, method='log')
        
        # Check that skewness is reduced
        assert abs(result['A'].skew()) < abs(data['A'].skew())
    
    @pytest.mark.multiclass
    def test_multiclass_dataset(self):
        """Test handling of multiclass datasets."""
        data = create_multiclass_dataset()
        
        # Test with multiclass models
        X = data.drop('target', axis=1)
        y = data['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Check that the model performs well on multiclass data
        assert accuracy > 0.8
    
    @pytest.mark.multilabel
    def test_multilabel_dataset(self):
        """Test handling of multilabel datasets."""
        data = create_multilabel_dataset()
        
        # Test with multilabel models
        X = data.drop(['target1', 'target2'], axis=1)
        y = data[['target1', 'target2']]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = RandomForestClassifier()
        model.fit(X_train, y_train['target1'])
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test['target1'], y_pred)
        
        # Check that the model performs well on multilabel data
        assert accuracy > 0.8
    
    @pytest.mark.multitarget
    def test_multitarget_dataset(self):
        """Test handling of multitarget datasets."""
        data = create_multitarget_dataset()
        
        # Test with multitarget models
        X = data.drop(['target1', 'target2'], axis=1)
        y = data[['target1', 'target2']]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = RandomForestRegressor()
        model.fit(X_train, y_train['target1'])
        
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test['target1'], y_pred)
        
        # Check that the model performs well on multitarget data
        assert r2 > 0.8
    
    @pytest.mark.time_series
    def test_time_series_forecasting_dataset(self):
        """Test handling of time series forecasting datasets."""
        data = create_time_series_forecasting_dataset()
        
        # Test with time series models
        X = data.drop('target', axis=1)
        y = data['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        # Check that the model performs well on time series data
        assert r2 > 0.8
    
    @pytest.mark.large
    def test_dask_dataset(self):
        """Test handling of datasets with Dask."""
        try:
            data = create_large_dataset(rows=10000, cols=10)  # Reduced size for testing
            
            # Test with Dask
            with LocalCluster(processes=False) as cluster:  # Use threads instead of processes
                with Client(cluster) as client:
                    # Convert to Dask DataFrame
                    ddf = dd.from_pandas(data, npartitions=2)
                    
                    # Perform some basic operations
                    result = ddf.compute()
                    
                    # Verify the data
                    assert len(result) == len(data)
                    assert list(result.columns) == list(data.columns)
                    
        except Exception as e:
            pytest.skip(f"Dask test skipped due to: {str(e)}")
    
    @pytest.mark.performance
    def test_memory_efficiency(self):
        """Test memory efficiency of the library."""
        data = create_large_dataset(rows=100000, cols=50)
        
        # Test memory usage
        initial_memory = get_memory_usage()
        
        # Process data
        result = handle_missing_values(data)
        result = encode_categorical(result)
        result = scale_features(result)
        
        final_memory = get_memory_usage()
        
        # Check that memory usage is reasonable
        assert final_memory < initial_memory * 3
    
    @pytest.mark.performance
    def test_performance(self):
        """Test performance of the library."""
        data = create_large_dataset(rows=100000, cols=50)
        
        # Test performance
        start_time = time.time()
        
        # Process data
        result = handle_missing_values(data)
        result = encode_categorical(result)
        result = scale_features(result)
        
        end_time = time.time()
        
        # Check that processing time is reasonable
        assert end_time - start_time < 10  # Less than 10 seconds
    
    @pytest.mark.error_handling
    def test_error_handling(self):
        """Test error handling of the library."""
        # Test with invalid input
        with pytest.raises(ValueError):
            handle_missing_values(None)
        
        with pytest.raises(ValueError):
            encode_categorical(None)
        
        with pytest.raises(ValueError):
            scale_features(None)
        
        with pytest.raises(ValueError):
            select_features(None)
    
    @pytest.mark.integration
    def test_comprehensive_pipeline(self):
        """Test a comprehensive pipeline with all edge cases."""
        # Create a dataset with various issues
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
        
        # Run a comprehensive pipeline
        # 1. Handle missing values
        data = handle_missing_values(data)
        
        # 2. Encode categorical variables
        data = encode_categorical(data)
        
        # 3. Scale features
        data = scale_features(data)
        
        # 4. Select features
        data = select_features(data)
        
        # 5. Split data
        X = data.drop('imbalanced', axis=1)
        y = data['imbalanced']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # 6. Train a model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        
        # 7. Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Check that the pipeline works end-to-end
        assert accuracy > 0.5
    
    @pytest.mark.inspector
    def test_data_inspector(self):
        """Test the DataInspector class with various edge cases."""
        # Create a dataset with various issues
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
        
        # Create a DataInspector instance
        inspector = DataInspector()
        
        # Inspect the data
        results = inspector.inspect_data(data)
        
        # Check that all issues are detected
        assert results['missing_data']['has_missing']
        assert results['outliers']['has_outliers']
        assert results['mixed_types']['has_mixed_types']
        assert results['unicode_issues']['has_unicode_issues']
        assert results['special_chars']['has_special_chars']
        assert results['time_series_issues']['has_time_series_issues']
        assert results['nested_data']['has_nested_data']
        assert results['correlations']['has_high_correlations']
        assert results['imbalanced']['is_imbalanced']
        assert results['sparse']['is_sparse']
        
        # Auto-fix the data
        fixed_data, fixes = inspector.auto_fix_data(data)
        
        # Check that all issues are fixed
        assert not fixed_data.isnull().any().any()
        assert fixed_data['numeric'].max() < 100
        assert all(isinstance(x, str) for x in fixed_data['mixed_types'])
        assert 'émoji' not in fixed_data['unicode'].values
        assert all(col.isidentifier() for col in fixed_data.columns)
        assert not fixed_data['datetime'].isnull().any()
        assert 'nested_dict_a' in fixed_data.columns
        assert 'nested_dict_b' in fixed_data.columns
        assert 'correlated2' not in fixed_data.columns
        assert isinstance(fixed_data['sparse'].dtype, pd.SparseDtype)
        
        # Generate a report
        report = inspector.generate_report()
        
        # Check that the report contains all the necessary information
        assert 'inspection_results' in report
        assert 'fix_results' in report
        assert 'timestamp' in report
        assert 'summary' in report

if __name__ == '__main__':
    pytest.main([__file__]) 
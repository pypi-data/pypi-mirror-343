"""
Test cases for ThinkML preprocessor modules.

This module contains comprehensive tests for:
- Missing values handling
- Feature scaling
- Categorical encoding
"""

import pytest
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.experimental import enable_iterative_imputer  # noqa
from thinkml.preprocessor.missing_values import handle_missing_values, detect_missing_patterns
from thinkml.preprocessor.scaler import scale_features, detect_outliers
from thinkml.preprocessor.encoder import encode_categorical

@pytest.fixture
def sample_data():
    """Create sample data with various edge cases."""
    np.random.seed(42)
    n_samples = 1000
    
    # Create DataFrame with different types of data
    data = {
        # Numerical columns with different distributions
        'normal': np.random.normal(0, 1, n_samples),
        'skewed': np.exp(np.random.normal(0, 1, n_samples)),
        'uniform': np.random.uniform(-1, 1, n_samples),
        'integers': np.random.randint(0, 100, n_samples),
        
        # Categorical columns
        'categorical': pd.Categorical(['A', 'B', 'C'] * (n_samples // 3 + 1))[:n_samples],
        'binary': np.random.choice(['Yes', 'No'], n_samples),
        'ordinal': pd.Categorical(['Low', 'Medium', 'High'] * (n_samples // 3 + 1),
                                categories=['Low', 'Medium', 'High'],
                                ordered=True)[:n_samples],
        
        # Special cases
        'with_missing': np.random.normal(0, 1, n_samples),
        'special_chars': ['Value_' + str(i % 5) for i in range(n_samples)],
        'unicode_text': ['Text_' + chr(0x0394 + i % 5) for i in range(n_samples)]  # Greek letters
    }
    
    df = pd.DataFrame(data)
    
    # Add missing values
    df.loc[np.random.choice(n_samples, n_samples // 10), 'with_missing'] = np.nan
    
    # Add extreme values
    df.loc[np.random.choice(n_samples, 5), 'normal'] = np.random.normal(10, 1, 5)
    
    return df

# Missing Values Tests
class TestMissingValues:
    def test_basic_imputation(self, sample_data):
        """Test basic imputation methods."""
        methods = ['mean', 'median', 'mode', 'constant', 'knn', 'iterative']
        for method in methods:
            result = handle_missing_values(sample_data, method=method)
            assert result['with_missing'].isnull().sum() == 0
    
    def test_categorical_handling(self, sample_data):
        """Test handling of categorical columns."""
        result = handle_missing_values(sample_data, 
                                     categorical_columns=['categorical', 'binary', 'ordinal'])
        assert result['categorical'].isnull().sum() == 0
    
    def test_max_missing_ratio(self, sample_data):
        """Test dropping columns with too many missing values."""
        # Add a column with >50% missing values
        sample_data['mostly_missing'] = np.nan
        result = handle_missing_values(sample_data, max_missing_ratio=0.5)
        assert 'mostly_missing' not in result.columns
    
    def test_chunk_processing(self):
        """Test processing of large datasets in chunks."""
        large_df = pd.DataFrame({
            'col': np.random.normal(0, 1, 200000)
        })
        large_df.iloc[::2, 0] = np.nan
        result = handle_missing_values(large_df, chunk_size=50000)
        assert result['col'].isnull().sum() == 0
    
    def test_pattern_detection(self, sample_data):
        """Test missing value pattern detection."""
        patterns = detect_missing_patterns(sample_data)
        assert isinstance(patterns, dict)
        assert 'missing_counts' in patterns
        assert 'correlation_matrix' in patterns

# Scaling Tests
class TestScaling:
    def test_basic_scaling(self, sample_data):
        """Test basic scaling methods."""
        methods = ['standard', 'robust', 'minmax', 'maxabs']
        for method in methods:
            result = scale_features(sample_data, method=method)
            if method in ['standard', 'robust']:
                assert abs(result['normal'].mean()) < 1e-10
            elif method == 'minmax':
                assert result['normal'].min() >= -1e-10
                assert result['normal'].max() <= 1 + 1e-10
    
    def test_extreme_value_handling(self, sample_data):
        """Test handling of extreme values."""
        result = scale_features(sample_data, handle_extreme=True, extreme_threshold=3.0)
        z_scores = np.abs((result['normal'] - result['normal'].mean()) / result['normal'].std())
        assert (z_scores > 3.0).sum() == 0
    
    def test_skewness_handling(self, sample_data):
        """Test handling of skewed distributions."""
        result = scale_features(sample_data, handle_skewness=True)
        skewness = abs(stats.skew(result['skewed'].dropna()))
        assert skewness < abs(stats.skew(sample_data['skewed'].dropna()))
    
    def test_outlier_detection(self, sample_data):
        """Test outlier detection methods."""
        methods = ['zscore', 'iqr', 'isolation_forest']
        for method in methods:
            outliers = detect_outliers(sample_data, method=method, threshold=0.1)
            assert isinstance(outliers, dict)
            assert 'normal' in outliers

# Encoding Tests
class TestEncoding:
    def test_basic_encoding(self, sample_data):
        """Test basic encoding methods."""
        methods = ['onehot', 'label', 'ordinal', 'binary', 'cyclic']
        for method in methods:
            result = encode_categorical(sample_data, method=method)
            assert 'categorical' not in result.columns  # Original column should be dropped
    
    def test_target_encoding(self, sample_data):
        """Test target encoding."""
        sample_data['target'] = np.random.randint(0, 2, len(sample_data))
        result = encode_categorical(sample_data, method='target', target_column='target')
        assert isinstance(result['categorical'].iloc[0], (np.float64, float))
    
    def test_special_characters(self, sample_data):
        """Test handling of special characters in column names."""
        result = encode_categorical(sample_data, columns=['special_chars'])
        assert all(c.isalnum() or c in ['_', '.'] for c in ''.join(result.columns))
    
    def test_unicode_handling(self, sample_data):
        """Test handling of unicode text."""
        result = encode_categorical(sample_data, columns=['unicode_text'])
        assert 'unicode_text' not in result.columns
    
    def test_unknown_categories(self, sample_data):
        """Test handling of unknown categories."""
        train = sample_data.copy()
        test = sample_data.copy()
        
        # Convert to string type first
        train['categorical'] = train['categorical'].astype(str)
        test['categorical'] = test['categorical'].astype(str)
        
        # Split the data
        train = train.iloc[:800]
        test = test.iloc[800:]
        test.loc[test.index[0], 'categorical'] = 'Unknown'
        
        result = encode_categorical(train, method='onehot')
        result_test = encode_categorical(test, method='onehot')
        assert set(result.columns) == set(result_test.columns)

# Edge Cases Tests
class TestEdgeCases:
    def test_empty_dataset(self):
        """Test handling of empty datasets."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError):
            handle_missing_values(empty_df)
        with pytest.raises(ValueError):
            scale_features(empty_df)
        with pytest.raises(ValueError):
            encode_categorical(empty_df)
    
    def test_single_column(self):
        """Test handling of single-column datasets."""
        single_col_df = pd.DataFrame({'A': [1, 2, np.nan, 4]})
        result = handle_missing_values(single_col_df)
        assert result['A'].isnull().sum() == 0
    
    def test_all_missing_column(self):
        """Test handling of columns with all missing values."""
        df = pd.DataFrame({'A': [np.nan] * 4})
        with pytest.raises(ValueError):
            handle_missing_values(df)
    
    def test_mixed_dtypes(self, sample_data):
        """Test handling of mixed data types."""
        df = pd.DataFrame({
            'mixed': ['1', 2, '3', 4.0, 'text'] * 200  # Repeat to match length
        })
        result = encode_categorical(df, columns=['mixed'])
        assert 'mixed' not in result.columns
    
    def test_large_categories(self):
        """Test handling of categorical columns with many unique values."""
        df = pd.DataFrame({
            'many_cats': [f'cat_{i}' for i in range(1000)]
        })
        result = encode_categorical(df, method='binary')
        assert len(result.columns) < 1000  # Binary encoding should be more compact
    
    def test_memory_efficiency(self):
        """Test memory-efficient processing of large datasets."""
        large_df = pd.DataFrame({
            'num': np.random.normal(0, 1, 200000),
            'cat': [f'cat_{i%5}' for i in range(200000)]
        })
        
        # Test all processors with chunk processing
        result1 = handle_missing_values(large_df, chunk_size=50000)
        result2 = scale_features(large_df, chunk_size=50000)
        result3 = encode_categorical(large_df, chunk_size=50000)
        
        assert len(result1) == len(large_df)
        assert len(result2) == len(large_df)
        assert len(result3) == len(large_df) 
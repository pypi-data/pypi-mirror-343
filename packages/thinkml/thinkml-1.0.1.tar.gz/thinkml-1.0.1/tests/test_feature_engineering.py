"""
Test cases for the feature engineering module.
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from thinkml.feature_engineering.feature_engineering import FeatureEngineer

class TestFeatureEngineering(unittest.TestCase):
    """Test cases for the FeatureEngineer class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data."""
        # Create sample numeric data
        cls.numeric_data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'feature3': np.random.normal(0, 1, 100)
        })
        
        # Create sample categorical data
        cls.categorical_data = pd.DataFrame({
            'cat1': ['A', 'B', 'C'] * 34,
            'cat2': ['X', 'Y', 'Z'] * 34
        })
        
        # Create sample datetime data
        base_date = datetime.now()
        cls.datetime_data = pd.DataFrame({
            'date': [base_date + timedelta(days=x) for x in range(100)]
        })
        
        # Create sample text data
        cls.text_data = pd.DataFrame({
            'text': ['This is a test sentence.'] * 100
        })
        
        # Create sample time series data
        cls.time_series_data = pd.DataFrame({
            'date': [base_date + timedelta(days=x) for x in range(100)],
            'value': np.random.normal(0, 1, 100)
        })
        
        # Initialize FeatureEngineer
        cls.fe = FeatureEngineer()
    
    def test_create_features_numeric(self):
        """Test numeric feature creation."""
        df_new = self.fe.create_features(
            self.numeric_data,
            numeric_cols=['feature1', 'feature2']
        )
        
        # Check if new features are created
        self.assertIn('feature1_squared', df_new.columns)
        self.assertIn('feature1_cubed', df_new.columns)
        self.assertIn('feature1_log', df_new.columns)
        self.assertIn('feature1_rolling_mean', df_new.columns)
        self.assertIn('feature1_rolling_std', df_new.columns)
        
        # Check if original features are preserved
        self.assertIn('feature1', df_new.columns)
        self.assertIn('feature2', df_new.columns)
        self.assertIn('feature3', df_new.columns)
    
    def test_create_features_categorical(self):
        """Test categorical feature creation."""
        df_new = self.fe.create_features(
            self.categorical_data,
            categorical_cols=['cat1', 'cat2']
        )
        
        # Check if frequency encoding is created
        self.assertIn('cat1_freq', df_new.columns)
        self.assertIn('cat2_freq', df_new.columns)
        
        # Check if one-hot encoding is created
        self.assertIn('cat1_A', df_new.columns)
        self.assertIn('cat1_B', df_new.columns)
        self.assertIn('cat1_C', df_new.columns)
        self.assertIn('cat2_X', df_new.columns)
        self.assertIn('cat2_Y', df_new.columns)
        self.assertIn('cat2_Z', df_new.columns)
    
    def test_create_features_datetime(self):
        """Test datetime feature creation."""
        df_new = self.fe.create_features(
            self.datetime_data,
            datetime_cols=['date']
        )
        
        # Check if datetime features are created
        self.assertIn('date_year', df_new.columns)
        self.assertIn('date_month', df_new.columns)
        self.assertIn('date_day', df_new.columns)
        self.assertIn('date_dayofweek', df_new.columns)
        self.assertIn('date_quarter', df_new.columns)
    
    def test_create_features_text(self):
        """Test text feature creation."""
        df_new = self.fe.create_features(
            self.text_data,
            text_cols=['text']
        )
        
        # Check if text features are created
        self.assertIn('text_length', df_new.columns)
        self.assertIn('text_word_count', df_new.columns)
        
        # Check if TF-IDF features are created
        self.assertTrue(any(col.startswith('text_tfidf_') for col in df_new.columns))
    
    def test_select_features(self):
        """Test feature selection."""
        # Create target variable
        y = np.random.normal(0, 1, 100)
        
        # Test mutual information selection
        X_selected, indices = self.fe.select_features(
            self.numeric_data,
            y,
            method='mutual_info',
            n_features=2,
            task='regression'
        )
        
        self.assertEqual(X_selected.shape[1], 2)
        self.assertEqual(len(indices), 2)
        
        # Test PCA selection
        X_selected, indices = self.fe.select_features(
            self.numeric_data,
            y,
            method='pca',
            n_features=2
        )
        
        self.assertEqual(X_selected.shape[1], 2)
        self.assertEqual(len(indices), 2)
    
    def test_scale_features(self):
        """Test feature scaling."""
        # Test standard scaling
        X_scaled = self.fe.scale_features(
            self.numeric_data,
            method='standard'
        )
        
        self.assertEqual(X_scaled.shape, self.numeric_data.shape)
        self.assertAlmostEqual(np.mean(X_scaled), 0, places=1)
        self.assertAlmostEqual(np.std(X_scaled), 1, places=1)
        
        # Test minmax scaling
        X_scaled = self.fe.scale_features(
            self.numeric_data,
            method='minmax'
        )
        
        self.assertEqual(X_scaled.shape, self.numeric_data.shape)
        self.assertTrue(np.all(X_scaled >= 0))
        self.assertTrue(np.all(X_scaled <= 1))
    
    def test_create_interactions(self):
        """Test feature interactions."""
        X_interactions = self.fe.create_interactions(
            self.numeric_data,
            degree=2
        )
        
        # Check if interactions are created
        self.assertGreater(X_interactions.shape[1], self.numeric_data.shape[1])
    
    def test_encode_categorical(self):
        """Test categorical encoding."""
        # Test target encoding
        X_encoded = self.fe.encode_categorical(
            self.categorical_data,
            method='target',
            cols=['cat1', 'cat2']
        )
        
        self.assertEqual(X_encoded.shape[0], self.categorical_data.shape[0])
        
        # Test one-hot encoding
        X_encoded = self.fe.encode_categorical(
            self.categorical_data,
            method='onehot',
            cols=['cat1', 'cat2']
        )
        
        self.assertEqual(X_encoded.shape[0], self.categorical_data.shape[0])
    
    def test_create_time_features(self):
        """Test time feature creation."""
        df_new = self.fe.create_time_features(
            self.time_series_data,
            time_col='date'
        )
        
        # Check if time features are created
        self.assertIn('date_year', df_new.columns)
        self.assertIn('date_month', df_new.columns)
        self.assertIn('date_day', df_new.columns)
        self.assertIn('date_dayofweek', df_new.columns)
        self.assertIn('date_quarter', df_new.columns)
        
        # Check if lag features are created
        self.assertIn('value_lag1', df_new.columns)
        self.assertIn('value_lag7', df_new.columns)
        self.assertIn('value_lag30', df_new.columns)
        
        # Check if rolling statistics are created
        self.assertIn('value_rolling_mean_7', df_new.columns)
        self.assertIn('value_rolling_std_7', df_new.columns)
        self.assertIn('value_rolling_mean_30', df_new.columns)
        self.assertIn('value_rolling_std_30', df_new.columns)

if __name__ == '__main__':
    unittest.main() 
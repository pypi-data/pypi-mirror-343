import unittest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split

import thinkml as tm
from thinkml.validation import NestedCrossValidator, TimeSeriesValidator, StratifiedGroupValidator, BootstrapValidator
from thinkml.optimization import EarlyStopping, GPUAccelerator, ParallelProcessor
from thinkml.selection import BayesianOptimizer, MultiObjectiveOptimizer
from thinkml.feature_engineering import create_features, select_features
from thinkml.interpretability import explain_model, get_feature_importance
from thinkml.regression import QuantileRegressor, RobustRegressor
from thinkml.classification import MultiLabelClassifier, CostSensitiveClassifier
from thinkml.calibration import calibrate_probabilities, plot_reliability_diagram
from thinkml.utils import preprocess_data, evaluate_model


class TestThinkML(unittest.TestCase):
    """Comprehensive test suite for ThinkML v1.0"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data once for all tests"""
        # Generate classification dataset
        X_clf, y_clf = make_classification(
            n_samples=1000, 
            n_features=20, 
            n_informative=15, 
            n_redundant=5,
            n_classes=2,
            random_state=42
        )
        cls.X_clf = pd.DataFrame(X_clf, columns=[f'feature_{i}' for i in range(20)])
        cls.y_clf = y_clf
        
        # Generate regression dataset
        X_reg, y_reg = make_regression(
            n_samples=1000, 
            n_features=20, 
            n_informative=15, 
            noise=0.1,
            random_state=42
        )
        cls.X_reg = pd.DataFrame(X_reg, columns=[f'feature_{i}' for i in range(20)])
        cls.y_reg = y_reg
        
        # Generate multi-label classification dataset
        X_ml, y_ml = make_classification(
            n_samples=1000, 
            n_features=20, 
            n_informative=15, 
            n_redundant=5,
            n_classes=3,
            random_state=42
        )
        cls.X_ml = pd.DataFrame(X_ml, columns=[f'feature_{i}' for i in range(20)])
        cls.y_ml = y_ml
        
        # Generate time series data
        t = np.linspace(0, 10, 1000)
        X_ts = np.column_stack([np.sin(t), np.cos(t), np.sin(2*t)])
        y_ts = np.sin(3*t) + np.random.normal(0, 0.1, 1000)
        cls.X_ts = pd.DataFrame(X_ts, columns=['sin', 'cos', 'sin2t'])
        cls.y_ts = y_ts
        
        # Generate data with missing values
        X_missing = cls.X_clf.copy()
        X_missing.iloc[::10, 0] = np.nan  # 10% missing in first column
        X_missing.iloc[::20, 1] = np.nan  # 5% missing in second column
        cls.X_missing = X_missing
        
        # Generate data with outliers
        X_outliers = cls.X_reg.copy()
        X_outliers.iloc[0, 0] = 1000  # Extreme outlier
        X_outliers.iloc[1, 1] = -1000  # Extreme outlier
        cls.X_outliers = X_outliers
        
        # Generate imbalanced classification data
        X_imb, y_imb = make_classification(
            n_samples=1000, 
            n_features=20, 
            n_informative=15, 
            n_redundant=5,
            n_classes=2,
            weights=[0.9, 0.1],  # 90% class 0, 10% class 1
            random_state=42
        )
        cls.X_imb = pd.DataFrame(X_imb, columns=[f'feature_{i}' for i in range(20)])
        cls.y_imb = y_imb
        
        # Generate categorical data
        X_cat = pd.DataFrame({
            'numeric': np.random.randn(1000),
            'category': np.random.choice(['A', 'B', 'C'], 1000),
            'binary': np.random.choice([0, 1], 1000),
            'ordinal': np.random.choice([1, 2, 3, 4, 5], 1000)
        })
        cls.X_cat = X_cat
        
        # Generate high-dimensional data
        X_high_dim, y_high_dim = make_classification(
            n_samples=100, 
            n_features=1000, 
            n_informative=100, 
            n_redundant=900,
            random_state=42
        )
        cls.X_high_dim = pd.DataFrame(X_high_dim, columns=[f'feature_{i}' for i in range(1000)])
        cls.y_high_dim = y_high_dim
        
        # Generate small dataset
        X_small, y_small = make_classification(
            n_samples=10, 
            n_features=5, 
            n_informative=3, 
            n_redundant=2,
            random_state=42
        )
        cls.X_small = pd.DataFrame(X_small, columns=[f'feature_{i}' for i in range(5)])
        cls.y_small = y_small
        
        # Generate groups for stratified group validation
        cls.groups = np.repeat(np.arange(10), 100)  # 10 groups, 100 samples each
        
        # Initialize models
        cls.clf_model = RandomForestClassifier(random_state=42)
        cls.reg_model = RandomForestRegressor(random_state=42)
        cls.lr_model = LogisticRegression(random_state=42)
        cls.lin_reg_model = LinearRegression()
    
    def test_validation_methods(self):
        """Test validation methods with various datasets"""
        
        # Test nested cross-validation
        param_grid = {
            'n_estimators': [10, 20],
            'max_depth': [3, 5]
        }
        validator = NestedCrossValidator(
            estimator=self.clf_model,
            param_grid=param_grid,
            inner_cv=3,
            outer_cv=3,
            scoring='accuracy'
        )
        results = validator.fit_predict(self.X_clf, self.y_clf)
        self.assertIsNotNone(results)
        self.assertIn('mean_score', results)
        self.assertIn('std_score', results)
        self.assertIn('outer_scores', results)
        self.assertIn('best_params_list', results)
        
        # Test time series cross-validation
        validator = TimeSeriesValidator(n_splits=3, test_size=0.2)
        results = validator.fit_predict(self.X_ts, self.y_ts, self.reg_model)
        self.assertIsNotNone(results)
        self.assertIn('mean_score', results)
        self.assertIn('std_score', results)
        self.assertIn('scores', results)
        self.assertIn('predictions', results)
        
        # Test stratified group cross-validation
        validator = StratifiedGroupValidator(n_splits=3, groups=self.groups)
        results = validator.fit_predict(self.X_clf, self.y_clf, self.clf_model)
        self.assertIsNotNone(results)
        self.assertIn('mean_score', results)
        self.assertIn('std_score', results)
        self.assertIn('scores', results)
        self.assertIn('predictions', results)
        
        # Test bootstrap validation
        validator = BootstrapValidator(n_iterations=10, sample_size=0.8)
        results = validator.fit_predict(self.X_clf, self.y_clf, self.clf_model)
        self.assertIsNotNone(results)
        self.assertIn('mean_score', results)
        self.assertIn('std_score', results)
        self.assertIn('scores', results)
        self.assertIn('predictions', results)
        
        # Edge case: Small dataset
        param_grid = {
            'n_estimators': [10],
            'max_depth': [3]
        }
        validator = NestedCrossValidator(
            estimator=self.clf_model,
            param_grid=param_grid,
            inner_cv=2,
            outer_cv=2,
            scoring='accuracy'
        )
        results = validator.fit_predict(self.X_small, self.y_small)
        self.assertIsNotNone(results)
        
        # Edge case: High-dimensional data
        param_grid = {
            'n_estimators': [10],
            'max_depth': [3]
        }
        validator = NestedCrossValidator(
            estimator=self.clf_model,
            param_grid=param_grid,
            inner_cv=2,
            outer_cv=2,
            scoring='accuracy'
        )
        results = validator.fit_predict(self.X_high_dim, self.y_high_dim)
        self.assertIsNotNone(results)
    
    def test_optimization_methods(self):
        """Test optimization methods with various datasets"""
        
        # Test early stopping
        early_stopping = EarlyStopping(patience=3, min_delta=0.001)
        self.assertFalse(early_stopping.should_stop(0.5))  # First call
        self.assertFalse(early_stopping.should_stop(0.49))  # Improvement
        self.assertFalse(early_stopping.should_stop(0.48))  # Improvement
        self.assertFalse(early_stopping.should_stop(0.48))  # No improvement, but within patience
        self.assertFalse(early_stopping.should_stop(0.48))  # No improvement, but within patience
        self.assertTrue(early_stopping.should_stop(0.48))   # No improvement, exceeded patience
        
        # Test parallel processor
        processor = ParallelProcessor(n_jobs=2)
        results = processor.parallel_transform(self.X_clf, lambda x: x * 2)
        self.assertEqual(results.shape, self.X_clf.shape)
        np.testing.assert_array_almost_equal(results, self.X_clf * 2)
        
        # Edge case: Empty dataset
        processor = ParallelProcessor(n_jobs=2)
        results = processor.parallel_transform(pd.DataFrame(), lambda x: x * 2)
        self.assertEqual(results.shape, (0, 0))
    
    def test_selection_methods(self):
        """Test selection methods with various datasets"""
        
        # Test Bayesian optimization
        optimizer = BayesianOptimizer(
            param_space={
                'n_estimators': (10, 100),
                'max_depth': (3, 10)
            },
            n_trials=5,
            scoring='accuracy'
        )
        best_params = optimizer.optimize(self.clf_model, self.X_clf, self.y_clf)
        self.assertIsNotNone(best_params)
        self.assertIn('n_estimators', best_params)
        self.assertIn('max_depth', best_params)
        
        # Test multi-objective optimization
        optimizer = MultiObjectiveOptimizer(
            param_space={
                'n_estimators': (10, 100),
                'max_depth': (3, 10)
            },
            objectives=['accuracy', 'f1'],
            n_trials=5
        )
        pareto_front = optimizer.optimize(self.clf_model, self.X_clf, self.y_clf)
        self.assertIsNotNone(pareto_front)
        self.assertGreater(len(pareto_front), 0)
        
        # Edge case: Small search space
        optimizer = BayesianOptimizer(
            param_space={
                'n_estimators': (10, 20),
                'max_depth': (3, 4)
            },
            n_trials=2,
            scoring='accuracy'
        )
        best_params = optimizer.optimize(self.clf_model, self.X_small, self.y_small)
        self.assertIsNotNone(best_params)
    
    def test_feature_engineering_methods(self):
        """Test feature engineering methods with various datasets"""
        
        # Test feature creation
        X_new = create_features(self.X_clf, operations=['interaction', 'polynomial'])
        self.assertGreater(X_new.shape[1], self.X_clf.shape[1])
        
        # Test feature selection
        X_selected = select_features(self.X_clf, self.y_clf, method='mutual_info')
        self.assertLessEqual(X_selected.shape[1], self.X_clf.shape[1])
        
        # Edge case: Empty dataset
        X_empty = pd.DataFrame()
        X_new = create_features(X_empty, operations=['interaction', 'polynomial'])
        self.assertEqual(X_new.shape[0], 0)
        
        # Edge case: Single feature
        X_single = self.X_clf.iloc[:, 0:1]
        X_new = create_features(X_single, operations=['interaction', 'polynomial'])
        self.assertGreater(X_new.shape[1], 1)
        
        # Edge case: Categorical data
        X_new = create_features(self.X_cat, operations=['interaction', 'polynomial'])
        self.assertGreater(X_new.shape[1], self.X_cat.shape[1])
    
    def test_interpretability_methods(self):
        """Test interpretability methods with various datasets"""
        
        # Train a model first
        self.clf_model.fit(self.X_clf, self.y_clf)
        
        # Test model explanation
        explanations = explain_model(self.clf_model, self.X_clf, method='shap')
        self.assertIsNotNone(explanations)
        
        # Test feature importance
        importance = get_feature_importance(self.clf_model, self.X_clf)
        self.assertIsNotNone(importance)
        self.assertEqual(len(importance), self.X_clf.shape[1])
        
        # Edge case: Small dataset
        self.clf_model.fit(self.X_small, self.y_small)
        explanations = explain_model(self.clf_model, self.X_small, method='shap')
        self.assertIsNotNone(explanations)
        
        # Edge case: High-dimensional data
        self.clf_model.fit(self.X_high_dim, self.y_high_dim)
        importance = get_feature_importance(self.clf_model, self.X_high_dim)
        self.assertIsNotNone(importance)
    
    def test_regression_methods(self):
        """Test regression methods with various datasets"""
        
        # Test quantile regression
        regressor = QuantileRegressor(quantile=0.5)
        regressor.fit(self.X_reg, self.y_reg)
        predictions = regressor.predict(self.X_reg)
        self.assertEqual(len(predictions), len(self.y_reg))
        
        # Test robust regression
        regressor = RobustRegressor(method='huber')
        regressor.fit(self.X_outliers, self.y_reg)
        predictions = regressor.predict(self.X_outliers)
        self.assertEqual(len(predictions), len(self.y_reg))
        
        # Edge case: Small dataset
        regressor = QuantileRegressor(quantile=0.5)
        regressor.fit(self.X_small, self.y_small)
        predictions = regressor.predict(self.X_small)
        self.assertEqual(len(predictions), len(self.y_small))
        
        # Edge case: High-dimensional data
        regressor = RobustRegressor(method='huber')
        regressor.fit(self.X_high_dim, self.y_high_dim)
        predictions = regressor.predict(self.X_high_dim)
        self.assertEqual(len(predictions), len(self.y_high_dim))
    
    def test_classification_methods(self):
        """Test classification methods with various datasets"""
        
        # Test multi-label classification
        classifier = MultiLabelClassifier(base_estimator=self.lr_model)
        classifier.fit(self.X_ml, self.y_ml)
        predictions = classifier.predict(self.X_ml)
        self.assertEqual(predictions.shape, self.y_ml.shape)
        
        # Test cost-sensitive classification
        classifier = CostSensitiveClassifier(
            cost_matrix=[[0, 1], [10, 0]]
        )
        classifier.fit(self.X_imb, self.y_imb)
        predictions = classifier.predict(self.X_imb)
        self.assertEqual(len(predictions), len(self.y_imb))
        
        # Edge case: Small dataset
        classifier = MultiLabelClassifier(base_estimator=self.lr_model)
        classifier.fit(self.X_small, self.y_small)
        predictions = classifier.predict(self.X_small)
        self.assertEqual(len(predictions), len(self.y_small))
        
        # Edge case: Imbalanced data
        classifier = CostSensitiveClassifier(
            cost_matrix=[[0, 1], [10, 0]]
        )
        classifier.fit(self.X_imb, self.y_imb)
        predictions = classifier.predict(self.X_imb)
        self.assertEqual(len(predictions), len(self.y_imb))
    
    def test_calibration_methods(self):
        """Test calibration methods with various datasets"""
        
        # Train a model first
        self.clf_model.fit(self.X_clf, self.y_clf)
        y_pred_proba = self.clf_model.predict_proba(self.X_clf)[:, 1]
        
        # Test probability calibration
        calibrated_probs = calibrate_probabilities(
            self.clf_model, self.X_clf, self.y_clf, method='isotonic'
        )
        self.assertIsNotNone(calibrated_probs)
        self.assertEqual(len(calibrated_probs), len(self.y_clf))
        
        # Edge case: Small dataset
        self.clf_model.fit(self.X_small, self.y_small)
        calibrated_probs = calibrate_probabilities(
            self.clf_model, self.X_small, self.y_small, method='isotonic'
        )
        self.assertIsNotNone(calibrated_probs)
    
    def test_utility_methods(self):
        """Test utility methods with various datasets"""
        
        # Test data preprocessing
        X_processed = preprocess_data(
            self.X_missing,
            operations=['impute', 'scale', 'encode']
        )
        self.assertEqual(X_processed.shape[0], self.X_missing.shape[0])
        self.assertFalse(X_processed.isna().any().any())
        
        # Test model evaluation
        self.clf_model.fit(self.X_clf, self.y_clf)
        metrics = evaluate_model(
            self.clf_model, self.X_clf, self.y_clf,
            metrics=['accuracy', 'precision', 'recall']
        )
        self.assertIsNotNone(metrics)
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        
        # Edge case: Empty dataset
        X_processed = preprocess_data(
            pd.DataFrame(),
            operations=['impute', 'scale', 'encode']
        )
        self.assertEqual(X_processed.shape[0], 0)
        
        # Edge case: All missing values
        X_all_missing = pd.DataFrame(np.nan, index=range(10), columns=range(5))
        X_processed = preprocess_data(
            X_all_missing,
            operations=['impute', 'scale', 'encode']
        )
        self.assertEqual(X_processed.shape, X_all_missing.shape)
        self.assertFalse(X_processed.isna().any().any())
        
        # Edge case: Categorical data
        X_processed = preprocess_data(
            self.X_cat,
            operations=['impute', 'scale', 'encode']
        )
        self.assertEqual(X_processed.shape[0], self.X_cat.shape[0])
    
    def test_integration_pipeline(self):
        """Test a complete machine learning pipeline using ThinkML"""
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            self.X_clf, self.y_clf, test_size=0.2, random_state=42
        )
        
        # Feature engineering
        X_train_engineered = create_features(
            X_train,
            operations=['interaction', 'polynomial']
        )
        X_test_engineered = create_features(
            X_test,
            operations=['interaction', 'polynomial']
        )
        
        # Preprocess data
        X_train_processed = preprocess_data(
            X_train_engineered,
            operations=['impute', 'scale']
        )
        X_test_processed = preprocess_data(
            X_test_engineered,
            operations=['impute', 'scale']
        )
        
        # Optimize hyperparameters
        optimizer = BayesianOptimizer(
            param_space={
                'n_estimators': (10, 100),
                'max_depth': (3, 10)
            }
        )
        best_params = optimizer.optimize(X_train_processed, y_train, self.clf_model)
        
        # Train model with best parameters
        self.clf_model.set_params(**best_params)
        self.clf_model.fit(X_train_processed, y_train)
        
        # Interpret model
        explanations = explain_model(self.clf_model, X_train_processed)
        
        # Evaluate model
        metrics = evaluate_model(
            self.clf_model, X_test_processed, y_test,
            metrics=['accuracy', 'precision', 'recall']
        )
        
        # Calibrate probabilities
        calibrated_probs = calibrate_probabilities(
            self.clf_model, X_test_processed, y_test
        )
        
        # Assertions
        self.assertIsNotNone(best_params)
        self.assertIsNotNone(explanations)
        self.assertIsNotNone(metrics)
        self.assertIsNotNone(calibrated_probs)
        self.assertGreater(metrics['accuracy'], 0.5)  # Should perform better than random
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        
        # Test with empty dataset
        with self.assertRaises(ValueError):
            NestedCrossValidator().fit_predict(pd.DataFrame(), np.array([]), self.clf_model)
        
        # Test with single sample
        X_single = self.X_clf.iloc[0:1]
        y_single = self.y_clf[0:1]
        with self.assertRaises(ValueError):
            NestedCrossValidator().fit_predict(X_single, y_single, self.clf_model)
        
        # Test with mismatched dimensions
        with self.assertRaises(ValueError):
            NestedCrossValidator().fit_predict(self.X_clf, self.y_clf[0:10], self.clf_model)
        
        # Test with invalid parameters
        with self.assertRaises(ValueError):
            NestedCrossValidator(inner_cv=0).fit_predict(self.X_clf, self.y_clf, self.clf_model)
        
        # Test with invalid model
        with self.assertRaises(TypeError):
            NestedCrossValidator().fit_predict(self.X_clf, self.y_clf, "not a model")
        
        # Test with NaN target
        y_nan = self.y_clf.copy()
        y_nan[0] = np.nan
        with self.assertRaises(ValueError):
            NestedCrossValidator().fit_predict(self.X_clf, y_nan, self.clf_model)
        
        # Test with infinite values
        X_inf = self.X_clf.copy()
        X_inf.iloc[0, 0] = np.inf
        with self.assertRaises(ValueError):
            NestedCrossValidator().fit_predict(X_inf, self.y_clf, self.clf_model)


if __name__ == '__main__':
    unittest.main() 
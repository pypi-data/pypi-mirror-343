"""
Test suite for all models in ThinkML.

This module contains comprehensive tests for all models, including edge cases
and various data scenarios.
"""

import numpy as np
import pandas as pd
import pytest
import dask.dataframe as dd
import dask.array as da

from thinkml.algorithms import (
    LinearRegression,
    RidgeRegression,
    LassoRegression,
    LogisticRegression,
    DecisionTreeClassifier,
    DecisionTreeRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
    KNeighborsClassifier
)

# Helper functions
def generate_regression_data(n_samples=1000, n_features=10, noise=0.1):
    """Generate synthetic regression data."""
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    # Generate target with some linear relationship and noise
    weights = np.random.randn(n_features)
    y = np.dot(X, weights) + noise * np.random.randn(n_samples)
    return X, y

def generate_classification_data(n_samples=1000, n_features=10, n_classes=2):
    """Generate synthetic classification data."""
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    # Generate labels based on feature combinations
    y = np.zeros(n_samples)
    for i in range(n_samples):
        y[i] = int(np.sum(X[i, :n_features//2]) > 0)
    return X, y

def create_test_data(n_samples=1000, n_features=10, classification=True):
    """Create test datasets for both classification and regression."""
    if classification:
        return generate_classification_data(n_samples, n_features)
    else:
        return generate_regression_data(n_samples, n_features)

def create_dask_data(X, y):
    """Convert numpy arrays to Dask DataFrames."""
    X_df = pd.DataFrame(X)
    y_series = pd.Series(y)
    return dd.from_pandas(X_df, npartitions=2), dd.from_pandas(y_series, npartitions=2)

def create_large_dask_data(n_samples=100000, n_features=100, classification=True):
    """Create large test datasets using Dask."""
    if classification:
        X = da.random.random((n_samples, n_features), chunks=(10000, n_features))
        y = da.random.randint(0, 2, size=(n_samples,), chunks=10000)
    else:
        X = da.random.random((n_samples, n_features), chunks=(10000, n_features))
        y = da.random.random((n_samples,), chunks=10000)
    return X, y

# Test fixtures
@pytest.fixture
def regression_data():
    """Fixture for regression test data."""
    X, y = create_test_data(classification=False)
    # Split data into train and test
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    return X_train, X_test, y_train, y_test

@pytest.fixture
def classification_data():
    """Fixture for classification test data."""
    X, y = create_test_data(classification=True)
    # Split data into train and test
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    return X_train, X_test, y_train, y_test

@pytest.fixture
def clustering_data():
    """Fixture for clustering test data."""
    X, _ = create_test_data(classification=True)
    return X

@pytest.fixture
def large_regression_data():
    """Fixture for large regression test data."""
    X, y = create_large_dask_data(classification=False)
    return X, y

@pytest.fixture
def large_classification_data():
    """Fixture for large classification test data."""
    X, y = create_large_dask_data(classification=True)
    return X, y

# Regression model tests
class TestLinearRegression:
    """Test suite for LinearRegression model."""
    
    def test_basic_functionality(self, regression_data):
        """Test basic functionality of LinearRegression."""
        X_train, X_test, y_train, y_test = regression_data
        model = LinearRegression(learning_rate=0.01, n_iterations=1000)
        model.fit(X_train, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test)
        assert len(y_pred) == len(y_test)
        assert not np.any(np.isnan(y_pred))
        
        # Test scoring
        score = model.score(X_test, y_test)
        assert isinstance(score, float)
        assert not np.isnan(score)
    
    def test_edge_cases(self):
        """Test edge cases for LinearRegression."""
        # Test with single feature and perfect linear relationship
        X = np.array([[1], [2], [3]])
        y = np.array([1, 2, 3])
        model = LinearRegression(learning_rate=0.001, n_iterations=2000)
        model.fit(X, y)
        y_pred = model.predict([[4]])
        assert abs(y_pred[0] - 4) < 0.1  # Allow for some numerical error
        
        # Test with constant target
        y = np.array([1, 1, 1])
        model = LinearRegression(learning_rate=0.001, n_iterations=2000)
        model.fit(X, y)
        y_pred = model.predict([[4]])
        assert abs(y_pred[0] - 1) < 0.1  # Allow for some numerical error
        
        # Test with zero variance features
        X = np.array([[1, 0], [1, 0], [1, 0]])
        y = np.array([1, 2, 3])
        model = LinearRegression(learning_rate=0.001, n_iterations=2000)
        model.fit(X, y)
        assert not np.any(np.isnan(model.weights))
    
    def test_dask_integration(self, regression_data):
        """Test LinearRegression with Dask DataFrames."""
        X_train, X_test, y_train, y_test = regression_data
        X_train_dd, y_train_dd = create_dask_data(X_train, y_train)
        X_test_dd, y_test_dd = create_dask_data(X_test, y_test)
        
        model = LinearRegression(learning_rate=0.01, n_iterations=1000)
        model.fit(X_train_dd, y_train_dd)
        
        # Test predictions with Dask
        y_pred = model.predict(X_test_dd)
        assert isinstance(y_pred, dd.Series)
        
        # Test scoring with Dask
        score = model.score(X_test_dd, y_test_dd)
        assert isinstance(score, float)
        assert not np.isnan(score)

class TestSVR:
    """Test suite for SVR model."""
    
    def test_basic_functionality(self, regression_data):
        """Test basic functionality of SVR."""
        X_train, X_test, y_train, y_test = regression_data
        model = SVR(kernel='linear')
        model.fit(X_train, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test)
        assert len(y_pred) == len(y_test)
        assert not np.any(np.isnan(y_pred))
        
        # Test scoring
        score = model.score(X_test, y_test)
        assert isinstance(score, float)
        assert not np.isnan(score)
    
    def test_kernels(self, regression_data):
        """Test different kernel types."""
        X_train, X_test, y_train, y_test = regression_data
        
        # Test linear kernel
        model_linear = SVR(kernel='linear')
        model_linear.fit(X_train, y_train)
        y_pred_linear = model_linear.predict(X_test)
        
        # Test RBF kernel
        model_rbf = SVR(kernel='rbf')
        model_rbf.fit(X_train, y_train)
        y_pred_rbf = model_rbf.predict(X_test)
        
        # Predictions should be different
        assert not np.allclose(y_pred_linear, y_pred_rbf)
    
    def test_edge_cases(self):
        """Test edge cases for SVR."""
        model = SVR()
        
        # Test with single sample
        X = np.array([[1, 2, 3]])
        y = np.array([1])
        model.fit(X, y)
        assert not np.any(np.isnan(model.predict([[1, 2, 3]])))
        
        # Test with constant target
        X = np.array([[1, 2, 3], [4, 5, 6]])
        y = np.array([1, 1])
        model.fit(X, y)
        assert not np.any(np.isnan(model.predict([[1, 2, 3]])))

# Classification model tests
class TestLogisticRegression:
    """Test suite for LogisticRegression model."""
    
    def test_basic_functionality(self, classification_data):
        """Test basic functionality of LogisticRegression."""
        X_train, X_test, y_train, y_test = classification_data
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test)
        assert len(y_pred) == len(y_test)
        assert set(y_pred).issubset(set(y_train))
        
        # Test probabilities
        y_proba = model.predict_proba(X_test)
        assert y_proba.shape == (len(y_test), len(np.unique(y_train)))
        assert np.allclose(np.sum(y_proba, axis=1), 1)
        
        # Test scoring
        score = model.score(X_test, y_test)
        assert isinstance(score, float)
        assert 0 <= score <= 1
    
    def test_edge_cases(self):
        """Test edge cases for LogisticRegression."""
        model = LogisticRegression()
        
        # Test with single class
        X = np.array([[1, 2, 3], [4, 5, 6]])
        y = np.array([0, 0])
        model.fit(X, y)
        assert model.predict([[1, 2, 3]])[0] == 0
        
        # Test with imbalanced classes
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        y = np.array([0, 0, 1])
        model.fit(X, y)
        assert set(model.predict(X)).issubset({0, 1})

class TestSVC:
    """Test suite for SVC model."""
    
    def test_basic_functionality(self, classification_data):
        """Test basic functionality of SVC."""
        X_train, X_test, y_train, y_test = classification_data
        model = SVC(kernel='linear')
        model.fit(X_train, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test)
        assert len(y_pred) == len(y_test)
        assert set(y_pred).issubset(set(y_train))
        
        # Test probabilities
        y_proba = model.predict_proba(X_test)
        assert y_proba.shape == (len(y_test), len(np.unique(y_train)))
        assert np.allclose(np.sum(y_proba, axis=1), 1)
        
        # Test scoring
        score = model.score(X_test, y_test)
        assert isinstance(score, float)
        assert 0 <= score <= 1
    
    def test_kernels(self, classification_data):
        """Test different kernel types."""
        X_train, X_test, y_train, y_test = classification_data
        
        # Test linear kernel
        model_linear = SVC(kernel='linear')
        model_linear.fit(X_train, y_train)
        y_pred_linear = model_linear.predict(X_test)
        
        # Test RBF kernel
        model_rbf = SVC(kernel='rbf')
        model_rbf.fit(X_train, y_train)
        y_pred_rbf = model_rbf.predict(X_test)
        
        # Predictions should be different
        assert not np.allclose(y_pred_linear, y_pred_rbf)
    
    def test_edge_cases(self):
        """Test edge cases for SVC."""
        model = SVC()
        
        # Test with single class
        X = np.array([[1, 2, 3], [4, 5, 6]])
        y = np.array([0, 0])
        model.fit(X, y)
        assert model.predict([[1, 2, 3]])[0] == 0
        
        # Test with imbalanced classes
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        y = np.array([0, 0, 1])
        model.fit(X, y)
        assert set(model.predict(X)).issubset({0, 1})

# Clustering model tests
class TestKMeans:
    """Test suite for KMeans model."""
    
    def test_basic_functionality(self, clustering_data):
        """Test basic functionality of KMeans."""
        X = clustering_data
        model = KMeans(n_clusters=3)
        model.fit(X)
        
        # Test predictions
        labels = model.predict(X)
        assert len(labels) == len(X)
        assert set(labels).issubset(set(range(3)))
        
        # Test scoring
        score = model.score(X)
        assert isinstance(score, float)
    
    def test_edge_cases(self):
        """Test edge cases for KMeans."""
        model = KMeans(n_clusters=2)
        
        # Test with single sample
        X = np.array([[1, 2, 3]])
        model.fit(X)
        assert model.predict([[1, 2, 3]])[0] in {0, 1}
        
        # Test with duplicate samples
        X = np.array([[1, 2, 3], [1, 2, 3], [4, 5, 6]])
        model.fit(X)
        assert len(set(model.predict(X))) <= 2

class TestDBSCAN:
    """Test suite for DBSCAN model."""
    
    def test_basic_functionality(self, clustering_data):
        """Test basic functionality of DBSCAN."""
        X = clustering_data
        model = DBSCAN(eps=0.5, min_samples=5)
        model.fit(X)
        
        # Test predictions
        labels = model.predict(X)
        assert len(labels) == len(X)
        assert -1 in labels  # Noise points should be labeled as -1
    
    def test_edge_cases(self):
        """Test edge cases for DBSCAN."""
        model = DBSCAN(eps=0.5, min_samples=2)
        
        # Test with single sample
        X = np.array([[1, 2, 3]])
        model.fit(X)
        assert model.predict([[1, 2, 3]])[0] == -1
        
        # Test with duplicate samples
        X = np.array([[1, 2, 3], [1, 2, 3], [4, 5, 6]])
        model.fit(X)
        labels = model.predict(X)
        assert -1 in labels  # Should have noise points

# Dimensionality reduction tests
class TestPCA:
    """Test suite for PCA model."""
    
    def test_basic_functionality(self, clustering_data):
        """Test basic functionality of PCA."""
        X = clustering_data
        model = PCA(n_components=2)
        model.fit(X)
        
        # Test transformation
        X_transformed = model.transform(X)
        assert X_transformed.shape == (len(X), 2)
        
        # Test inverse transformation
        X_reconstructed = model.inverse_transform(X_transformed)
        assert X_reconstructed.shape == X.shape
    
    def test_edge_cases(self):
        """Test edge cases for PCA."""
        model = PCA(n_components=2)
        
        # Test with single sample
        X = np.array([[1, 2, 3]])
        model.fit(X)
        assert model.transform(X).shape == (1, 2)
        
        # Test with constant features
        X = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        model.fit(X)
        assert not np.any(np.isnan(model.transform(X)))

# Tree-based model tests
class TestDecisionTree:
    """Test suite for DecisionTree model."""
    
    def test_basic_functionality(self, classification_data):
        """Test basic functionality of DecisionTree."""
        X_train, X_test, y_train, y_test = classification_data
        model = DecisionTreeClassifier(max_depth=3)
        model.fit(X_train, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test)
        assert len(y_pred) == len(y_test)
        assert set(y_pred).issubset(set(y_train))
        
        # Test feature importances
        importances = model.feature_importances_
        assert len(importances) == X_train.shape[1]
        assert np.allclose(np.sum(importances), 1)
    
    def test_edge_cases(self):
        """Test edge cases for DecisionTree."""
        model = DecisionTreeClassifier(max_depth=3)
        
        # Test with single class
        X = np.array([[1, 2, 3], [4, 5, 6]])
        y = np.array([0, 0])
        model.fit(X, y)
        assert model.predict([[1, 2, 3]])[0] == 0
        
        # Test with constant features
        X = np.array([[1, 1, 1], [1, 1, 1], [2, 2, 2]])
        y = np.array([0, 0, 1])
        model.fit(X, y)
        assert set(model.predict(X)).issubset({0, 1})

class TestRandomForest:
    """Test suite for RandomForest model."""
    
    def test_basic_functionality(self, classification_data):
        """Test basic functionality of RandomForest."""
        X_train, X_test, y_train, y_test = classification_data
        model = RandomForestClassifier(n_estimators=10, max_depth=3)
        model.fit(X_train, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test)
        assert len(y_pred) == len(y_test)
        assert set(y_pred).issubset(set(y_train))
        
        # Test feature importances
        importances = model.feature_importances_
        assert len(importances) == X_train.shape[1]
        assert np.allclose(np.sum(importances), 1)
    
    def test_edge_cases(self):
        """Test edge cases for RandomForest."""
        model = RandomForestClassifier(n_estimators=10, max_depth=3)
        
        # Test with single class
        X = np.array([[1, 2, 3], [4, 5, 6]])
        y = np.array([0, 0])
        model.fit(X, y)
        assert model.predict([[1, 2, 3]])[0] == 0
        
        # Test with constant features
        X = np.array([[1, 1, 1], [1, 1, 1], [2, 2, 2]])
        y = np.array([0, 0, 1])
        model.fit(X, y)
        assert set(model.predict(X)).issubset({0, 1})

class TestGradientBoosting:
    """Test suite for GradientBoosting model."""
    
    def test_basic_functionality(self, classification_data):
        """Test basic functionality of GradientBoosting."""
        X_train, X_test, y_train, y_test = classification_data
        model = GradientBoosting(n_estimators=10, max_depth=3)
        model.fit(X_train, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test)
        assert len(y_pred) == len(y_test)
        assert set(y_pred).issubset(set(y_train))
        
        # Test feature importances
        importances = model.feature_importances_
        assert len(importances) == X_train.shape[1]
        assert np.allclose(np.sum(importances), 1)
    
    def test_edge_cases(self):
        """Test edge cases for GradientBoosting."""
        model = GradientBoosting(n_estimators=10, max_depth=3)
        
        # Test with single class
        X = np.array([[1, 2, 3], [4, 5, 6]])
        y = np.array([0, 0])
        model.fit(X, y)
        assert model.predict([[1, 2, 3]])[0] == 0
        
        # Test with constant features
        X = np.array([[1, 1, 1], [1, 1, 1], [2, 2, 2]])
        y = np.array([0, 0, 1])
        model.fit(X, y)
        assert set(model.predict(X)).issubset({0, 1})

# Big data handling tests
class TestBigDataHandling:
    """Test suite for big data handling capabilities."""
    
    def test_linear_regression_big_data(self, large_regression_data):
        """Test LinearRegression with large dataset."""
        X, y = large_regression_data
        model = LinearRegression(chunk_size=10000)
        model.fit(X, y)
        
        # Test predictions
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
        assert y_pred.shape == y.shape
        
        # Test scoring
        score = model.score(X, y)
        assert isinstance(score, float)
        assert not np.isnan(score)
    
    def test_logistic_regression_big_data(self, large_classification_data):
        """Test LogisticRegression with large dataset."""
        X, y = large_classification_data
        model = LogisticRegression(chunk_size=10000)
        model.fit(X, y)
        
        # Test predictions
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
        assert y_pred.shape == y.shape
        
        # Test probabilities
        y_proba = model.predict_proba(X)
        assert isinstance(y_proba, da.Array)
        assert y_proba.shape[0] == y.shape[0]
    
    def test_svr_big_data(self, large_regression_data):
        """Test SVR with large dataset."""
        X, y = large_regression_data
        model = SVR(kernel='linear', chunk_size=10000)
        model.fit(X, y)
        
        # Test predictions
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
        assert y_pred.shape == y.shape
    
    def test_svc_big_data(self, large_classification_data):
        """Test SVC with large dataset."""
        X, y = large_classification_data
        model = SVC(kernel='linear', chunk_size=10000)
        model.fit(X, y)
        
        # Test predictions
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
        assert y_pred.shape == y.shape
    
    def test_kmeans_big_data(self, large_classification_data):
        """Test KMeans with large dataset."""
        X, _ = large_classification_data
        model = KMeans(n_clusters=3, chunk_size=10000)
        model.fit(X)
        
        # Test predictions
        labels = model.predict(X)
        assert isinstance(labels, da.Array)
        assert labels.shape[0] == X.shape[0]
    
    def test_dbscan_big_data(self, large_classification_data):
        """Test DBSCAN with large dataset."""
        X, _ = large_classification_data
        model = DBSCAN(eps=0.5, min_samples=5, chunk_size=10000)
        model.fit(X)
        
        # Test predictions
        labels = model.predict(X)
        assert isinstance(labels, da.Array)
        assert labels.shape[0] == X.shape[0]
    
    def test_pca_big_data(self, large_classification_data):
        """Test PCA with large dataset."""
        X, _ = large_classification_data
        model = PCA(n_components=2, chunk_size=10000)
        model.fit(X)
        
        # Test transformation
        X_transformed = model.transform(X)
        assert isinstance(X_transformed, da.Array)
        assert X_transformed.shape == (X.shape[0], 2)
    
    def test_decision_tree_big_data(self, large_classification_data):
        """Test DecisionTree with large dataset."""
        X, y = large_classification_data
        model = DecisionTreeClassifier(max_depth=3, chunk_size=10000)
        model.fit(X, y)
        
        # Test predictions
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
        assert y_pred.shape == y.shape
    
    def test_random_forest_big_data(self, large_classification_data):
        """Test RandomForest with large dataset."""
        X, y = large_classification_data
        model = RandomForestClassifier(n_estimators=10, max_depth=3, chunk_size=10000)
        model.fit(X, y)
        
        # Test predictions
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
        assert y_pred.shape == y.shape
    
    def test_gradient_boosting_big_data(self, large_classification_data):
        """Test GradientBoosting with large dataset."""
        X, y = large_classification_data
        model = GradientBoosting(n_estimators=10, max_depth=3, chunk_size=10000)
        model.fit(X, y)
        
        # Test predictions
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
        assert y_pred.shape == y.shape

# Memory efficiency tests
class TestMemoryEfficiency:
    """Test suite for memory efficiency."""
    
    def test_chunked_processing(self, large_regression_data):
        """Test chunked processing for memory efficiency."""
        X, y = large_regression_data
        chunk_sizes = [1000, 5000, 10000]
        
        for chunk_size in chunk_sizes:
            model = LinearRegression(chunk_size=chunk_size)
            model.fit(X, y)
            y_pred = model.predict(X)
            assert isinstance(y_pred, da.Array)
    
    def test_parallel_processing(self, large_classification_data):
        """Test parallel processing capabilities."""
        X, y = large_classification_data
        model = RandomForestClassifier(n_estimators=10, n_jobs=-1)
        model.fit(X, y)
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array)
    
    def test_incremental_learning(self, large_regression_data):
        """Test incremental learning capabilities."""
        X, y = large_regression_data
        model = LinearRegression()
        
        # Test partial fit
        for i in range(0, X.shape[0], 10000):
            X_chunk = X[i:i+10000]
            y_chunk = y[i:i+10000]
            model.partial_fit(X_chunk, y_chunk)
        
        y_pred = model.predict(X)
        assert isinstance(y_pred, da.Array) 
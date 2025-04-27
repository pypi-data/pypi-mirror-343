"""
Test cases for the model persistence module.

This module contains test cases for saving and loading models
in various formats.
"""

import os
import pytest
import numpy as np
import pandas as pd
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from thinkml.algorithms import LogisticRegression, NeuralNetwork
from thinkml.persistence import save_model, load_model

# ===== Fixtures =====

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def logistic_regression_model():
    """Train a sample logistic regression model."""
    # Generate synthetic data
    X = np.random.randn(100, 5)
    y = (np.random.randn(100) > 0).astype(int)
    
    # Train model
    model = LogisticRegression(learning_rate=0.01, n_iterations=1000)
    model.fit(X, y)
    
    return model

@pytest.fixture
def neural_network_model():
    """Train a sample neural network model."""
    # Generate synthetic data
    X = np.random.randn(100, 5)
    y = (np.random.randn(100) > 0).astype(int)
    
    # Train model
    model = NeuralNetwork(
        input_size=5,
        output_size=1,
        hidden_sizes=[10, 5],
        activation='relu',
        learning_rate=0.01
    )
    model.fit(X, y, n_iterations=100)
    
    return model

@pytest.fixture
def sample_metadata():
    """Create sample metadata for models."""
    return {
        'created_at': '2023-01-01',
        'version': '1.0.0',
        'description': 'Test model',
        'parameters': {
            'learning_rate': 0.01,
            'n_iterations': 1000
        }
    }

# ===== Test Cases =====

def test_save_load_pickle(logistic_regression_model, temp_dir, sample_metadata):
    """Test saving and loading a model using pickle format."""
    # Save model
    filename = os.path.join(temp_dir, 'model.pkl')
    save_model(logistic_regression_model, filename, format='pkl', metadata=sample_metadata)
    
    # Load model
    loaded_data = load_model(filename, format='pkl')
    
    # Check model and metadata
    assert 'model' in loaded_data
    assert 'metadata' in loaded_data
    assert loaded_data['metadata'] == sample_metadata
    
    # Check model functionality
    loaded_model = loaded_data['model']
    X_test = np.random.randn(10, 5)
    original_pred = logistic_regression_model.predict(X_test)
    loaded_pred = loaded_model.predict(X_test)
    
    assert np.array_equal(original_pred, loaded_pred)

def test_save_load_joblib(logistic_regression_model, temp_dir, sample_metadata):
    """Test saving and loading a model using joblib format."""
    # Save model
    filename = os.path.join(temp_dir, 'model.joblib')
    save_model(logistic_regression_model, filename, format='joblib', metadata=sample_metadata)
    
    # Load model
    loaded_data = load_model(filename, format='joblib')
    
    # Check model and metadata
    assert 'model' in loaded_data
    assert 'metadata' in loaded_data
    assert loaded_data['metadata'] == sample_metadata
    
    # Check model functionality
    loaded_model = loaded_data['model']
    X_test = np.random.randn(10, 5)
    original_pred = logistic_regression_model.predict(X_test)
    loaded_pred = loaded_model.predict(X_test)
    
    assert np.array_equal(original_pred, loaded_pred)

@patch('thinkml.persistence.model_saver.ONNX_AVAILABLE', True)
@patch('thinkml.persistence.model_saver.onnx')
@patch('thinkml.persistence.model_saver.convert_sklearn')
def test_save_load_onnx(mock_convert, mock_onnx, logistic_regression_model, temp_dir, sample_metadata):
    """Test saving and loading a model using ONNX format."""
    # Mock ONNX conversion
    mock_onnx_model = MagicMock()
    mock_convert.return_value = mock_onnx_model
    
    # Save model
    filename = os.path.join(temp_dir, 'model.onnx')
    save_model(logistic_regression_model, filename, format='onnx', metadata=sample_metadata)
    
    # Check if ONNX conversion was called
    mock_convert.assert_called_once()
    mock_onnx.save.assert_called_once_with(mock_onnx_model, filename)
    
    # Mock loading ONNX model
    mock_onnx.load.return_value = mock_onnx_model
    
    # Load model
    loaded_data = load_model(filename, format='onnx')
    
    # Check model and metadata
    assert 'model' in loaded_data
    assert 'metadata' in loaded_data
    assert loaded_data['metadata'] == sample_metadata

@patch('thinkml.persistence.model_saver.PMML_AVAILABLE', True)
@patch('thinkml.persistence.model_saver.skl_to_pmml')
def test_save_load_pmml(mock_skl_to_pmml, logistic_regression_model, temp_dir, sample_metadata):
    """Test saving a model using PMML format."""
    # Save model
    filename = os.path.join(temp_dir, 'model.pmml')
    save_model(logistic_regression_model, filename, format='pmml', metadata=sample_metadata)
    
    # Check if PMML conversion was called
    mock_skl_to_pmml.assert_called_once()
    
    # Loading PMML is not implemented
    with pytest.raises(NotImplementedError):
        load_model(filename, format='pmml')

@patch('thinkml.persistence.model_saver.H5_AVAILABLE', True)
@patch('thinkml.persistence.model_saver.h5py')
def test_save_load_h5(mock_h5py, neural_network_model, temp_dir, sample_metadata):
    """Test saving and loading a neural network model using H5 format."""
    # Mock H5 file operations
    mock_file = MagicMock()
    mock_h5py.File.return_value.__enter__.return_value = mock_file
    
    # Mock groups and datasets
    mock_weights_group = MagicMock()
    mock_file.create_group.return_value = mock_weights_group
    
    mock_layer_group = MagicMock()
    mock_weights_group.create_group.return_value = mock_layer_group
    
    mock_config_group = MagicMock()
    mock_file.create_group.return_value = mock_config_group
    
    # Save model
    filename = os.path.join(temp_dir, 'model.h5')
    save_model(neural_network_model, filename, format='h5', metadata=sample_metadata)
    
    # Check if H5 file was created
    mock_h5py.File.assert_called_once()
    
    # Mock loading H5 file
    mock_file.__getitem__.side_effect = lambda key: {
        'config': mock_config_group,
        'weights': mock_weights_group
    }.get(key)
    
    mock_config_group.attrs = {
        'input_size': neural_network_model.input_size,
        'output_size': neural_network_model.output_size,
        'hidden_sizes': neural_network_model.hidden_sizes,
        'activation': neural_network_model.activation,
        'learning_rate': neural_network_model.learning_rate
    }
    
    mock_layer = MagicMock()
    mock_weights_group.__getitem__.return_value = mock_layer
    
    mock_layer.__getitem__.side_effect = lambda key: {
        'weights': np.random.randn(5, 10),
        'biases': np.random.randn(10)
    }.get(key)
    
    # Load model
    loaded_data = load_model(filename, format='h5')
    
    # Check model and metadata
    assert 'model' in loaded_data
    assert 'metadata' in loaded_data
    assert loaded_data['metadata'] == sample_metadata

def test_invalid_format(logistic_regression_model, temp_dir):
    """Test saving a model with an invalid format."""
    # Save model with invalid format
    filename = os.path.join(temp_dir, 'model.invalid')
    with pytest.raises(ValueError, match="Unsupported format"):
        save_model(logistic_regression_model, filename, format='invalid')
    
    # Load model with invalid format
    with pytest.raises(ValueError, match="Unsupported format"):
        load_model(filename, format='invalid')

def test_file_not_found(temp_dir):
    """Test loading a non-existent model file."""
    filename = os.path.join(temp_dir, 'nonexistent.pkl')
    with pytest.raises(FileNotFoundError):
        load_model(filename, format='pkl')

@patch('thinkml.persistence.model_saver.ONNX_AVAILABLE', False)
def test_onnx_not_available(logistic_regression_model, temp_dir):
    """Test saving a model with ONNX format when not available."""
    filename = os.path.join(temp_dir, 'model.onnx')
    with pytest.raises(ValueError, match="ONNX support not available"):
        save_model(logistic_regression_model, filename, format='onnx')

@patch('thinkml.persistence.model_saver.PMML_AVAILABLE', False)
def test_pmml_not_available(logistic_regression_model, temp_dir):
    """Test saving a model with PMML format when not available."""
    filename = os.path.join(temp_dir, 'model.pmml')
    with pytest.raises(ValueError, match="PMML support not available"):
        save_model(logistic_regression_model, filename, format='pmml')

@patch('thinkml.persistence.model_saver.H5_AVAILABLE', False)
def test_h5_not_available(neural_network_model, temp_dir):
    """Test saving a model with H5 format when not available."""
    filename = os.path.join(temp_dir, 'model.h5')
    with pytest.raises(ValueError, match="H5 support not available"):
        save_model(neural_network_model, filename, format='h5')

def test_incompatible_model_for_onnx(temp_dir):
    """Test saving an incompatible model with ONNX format."""
    # Create an incompatible model (no get_params or predict methods)
    class IncompatibleModel:
        pass
    
    model = IncompatibleModel()
    filename = os.path.join(temp_dir, 'model.onnx')
    
    with patch('thinkml.persistence.model_saver.ONNX_AVAILABLE', True):
        with pytest.raises(ValueError, match="not compatible with ONNX conversion"):
            save_model(model, filename, format='onnx')

def test_incompatible_model_for_pmml(temp_dir):
    """Test saving an incompatible model with PMML format."""
    # Create an incompatible model (no get_params or predict methods)
    class IncompatibleModel:
        pass
    
    model = IncompatibleModel()
    filename = os.path.join(temp_dir, 'model.pmml')
    
    with patch('thinkml.persistence.model_saver.PMML_AVAILABLE', True):
        with pytest.raises(ValueError, match="not compatible with PMML conversion"):
            save_model(model, filename, format='pmml')

def test_incompatible_model_for_h5(logistic_regression_model, temp_dir):
    """Test saving a non-neural network model with H5 format."""
    filename = os.path.join(temp_dir, 'model.h5')
    
    with patch('thinkml.persistence.model_saver.H5_AVAILABLE', True):
        with pytest.raises(ValueError, match="only supported for NeuralNetwork models"):
            save_model(logistic_regression_model, filename, format='h5') 
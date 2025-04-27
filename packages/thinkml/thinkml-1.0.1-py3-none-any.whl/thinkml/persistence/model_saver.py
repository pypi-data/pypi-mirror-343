"""
Model persistence utilities for ThinkML.

This module provides functions to save and load machine learning models
in various formats.
"""

import os
import pickle
import joblib
import numpy as np
import pandas as pd
from typing import Any, Union, Dict, Optional
import warnings

# Optional imports for different formats
try:
    import onnx
    import skl2onnx
    from skl2onnx import convert_sklearn
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False

try:
    from nyoka import skl_to_pmml
    PMML_AVAILABLE = True
except ImportError:
    PMML_AVAILABLE = False

try:
    import h5py
    H5_AVAILABLE = True
except ImportError:
    H5_AVAILABLE = False

from thinkml.algorithms import NeuralNetwork

def save_model(
    model: Any,
    filename: str,
    format: str = 'pkl',
    metadata: Optional[Dict] = None
) -> None:
    """
    Save a machine learning model to a file.
    
    Parameters
    ----------
    model : Any
        The model to save
    filename : str
        Path to save the model
    format : str, optional
        Format to save the model in ('pkl', 'joblib', 'onnx', 'pmml', 'h5'), by default 'pkl'
    metadata : Optional[Dict], optional
        Additional metadata to save with the model, by default None
    
    Raises
    ------
    ValueError
        If the format is not supported or the model is incompatible
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    
    # Add metadata if provided
    if metadata is None:
        metadata = {}
    
    # Save based on format
    if format == 'pkl':
        with open(filename, 'wb') as f:
            pickle.dump({'model': model, 'metadata': metadata}, f)
    
    elif format == 'joblib':
        joblib.dump({'model': model, 'metadata': metadata}, filename)
    
    elif format == 'onnx':
        if not ONNX_AVAILABLE:
            raise ValueError("ONNX support not available. Install skl2onnx and onnx packages.")
        
        # Check if model is compatible with ONNX conversion
        if not hasattr(model, 'get_params') or not hasattr(model, 'predict'):
            raise ValueError("Model is not compatible with ONNX conversion")
        
        # Convert to ONNX
        initial_type = [('float_input', skl2onnx.common.data_types.FloatTensorType([None, model.n_features_in_]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)
        
        # Save ONNX model
        onnx.save(onnx_model, filename)
        
        # Save metadata separately
        metadata_file = f"{filename}.metadata.pkl"
        with open(metadata_file, 'wb') as f:
            pickle.dump(metadata, f)
    
    elif format == 'pmml':
        if not PMML_AVAILABLE:
            raise ValueError("PMML support not available. Install nyoka package.")
        
        # Check if model is compatible with PMML conversion
        if not hasattr(model, 'get_params') or not hasattr(model, 'predict'):
            raise ValueError("Model is not compatible with PMML conversion")
        
        # Convert to PMML
        skl_to_pmml(pipeline=model, pmml_f_name=filename)
        
        # Save metadata separately
        metadata_file = f"{filename}.metadata.pkl"
        with open(metadata_file, 'wb') as f:
            pickle.dump(metadata, f)
    
    elif format == 'h5':
        if not H5_AVAILABLE:
            raise ValueError("H5 support not available. Install h5py package.")
        
        # Check if model is a neural network
        if not isinstance(model, NeuralNetwork):
            raise ValueError("H5 format is only supported for NeuralNetwork models")
        
        # Save model weights and architecture
        with h5py.File(filename, 'w') as f:
            # Save model weights
            weights_group = f.create_group('weights')
            for i, layer in enumerate(model.layers):
                layer_group = weights_group.create_group(f'layer_{i}')
                layer_group.create_dataset('weights', data=layer.weights)
                layer_group.create_dataset('biases', data=layer.biases)
            
            # Save model configuration
            config_group = f.create_group('config')
            config_group.attrs['input_size'] = model.input_size
            config_group.attrs['output_size'] = model.output_size
            config_group.attrs['hidden_sizes'] = model.hidden_sizes
            config_group.attrs['activation'] = model.activation
            config_group.attrs['learning_rate'] = model.learning_rate
        
        # Save metadata separately
        metadata_file = f"{filename}.metadata.pkl"
        with open(metadata_file, 'wb') as f:
            pickle.dump(metadata, f)
    
    else:
        raise ValueError(f"Unsupported format: {format}")

def load_model(
    filename: str,
    format: str = 'pkl'
) -> Dict[str, Any]:
    """
    Load a machine learning model from a file.
    
    Parameters
    ----------
    filename : str
        Path to the saved model
    format : str, optional
        Format of the saved model ('pkl', 'joblib', 'onnx', 'pmml', 'h5'), by default 'pkl'
    
    Returns
    -------
    Dict[str, Any]
        Dictionary containing the model and metadata
    
    Raises
    ------
    ValueError
        If the format is not supported or the file cannot be loaded
    FileNotFoundError
        If the file does not exist
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Model file not found: {filename}")
    
    # Load based on format
    if format == 'pkl':
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data
    
    elif format == 'joblib':
        data = joblib.load(filename)
        return data
    
    elif format == 'onnx':
        if not ONNX_AVAILABLE:
            raise ValueError("ONNX support not available. Install skl2onnx and onnx packages.")
        
        # Load ONNX model
        onnx_model = onnx.load(filename)
        
        # Load metadata
        metadata_file = f"{filename}.metadata.pkl"
        if os.path.exists(metadata_file):
            with open(metadata_file, 'rb') as f:
                metadata = pickle.load(f)
        else:
            metadata = {}
        
        return {'model': onnx_model, 'metadata': metadata}
    
    elif format == 'pmml':
        if not PMML_AVAILABLE:
            raise ValueError("PMML support not available. Install nyoka package.")
        
        # PMML models are not directly loadable in Python
        # We would need a PMML interpreter, which is beyond the scope of this implementation
        raise NotImplementedError("Loading PMML models is not implemented")
    
    elif format == 'h5':
        if not H5_AVAILABLE:
            raise ValueError("H5 support not available. Install h5py package.")
        
        # Load model from H5 file
        with h5py.File(filename, 'r') as f:
            # Load model configuration
            config = f['config']
            input_size = config.attrs['input_size']
            output_size = config.attrs['output_size']
            hidden_sizes = config.attrs['hidden_sizes']
            activation = config.attrs['activation']
            learning_rate = config.attrs['learning_rate']
            
            # Create model
            from thinkml.algorithms import NeuralNetwork
            model = NeuralNetwork(
                input_size=input_size,
                output_size=output_size,
                hidden_sizes=hidden_sizes,
                activation=activation,
                learning_rate=learning_rate
            )
            
            # Load weights
            weights_group = f['weights']
            for i, layer in enumerate(model.layers):
                layer_group = weights_group[f'layer_{i}']
                layer.weights = layer_group['weights'][:]
                layer.biases = layer_group['biases'][:]
        
        # Load metadata
        metadata_file = f"{filename}.metadata.pkl"
        if os.path.exists(metadata_file):
            with open(metadata_file, 'rb') as f:
                metadata = pickle.load(f)
        else:
            metadata = {}
        
        return {'model': model, 'metadata': metadata}
    
    else:
        raise ValueError(f"Unsupported format: {format}") 
"""
Base model class for ThinkML algorithms.

This module provides a base class for all machine learning models
in the ThinkML library.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple
import dask.array as da

class BaseModel:
    """
    Base class for all ThinkML models.
    
    This class provides common functionality for all models,
    including data preprocessing, chunk-based processing, and Dask support.
    """
    
    def __init__(self, chunk_size: int = 10000):
        """
        Initialize the base model.
        
        Parameters
        ----------
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        """
        self.chunk_size = chunk_size
        self.is_fitted = False
    
    def fit(self, X, y):
        """
        Fit the model to the data.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Training features
        y : Union[pd.Series, np.ndarray, dd.Series]
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        raise NotImplementedError("Subclasses must implement fit method")
    
    def predict(self, X):
        """
        Make predictions for X.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Samples
            
        Returns
        -------
        Union[np.ndarray, pd.Series, dd.Series]
            Predicted values
        """
        raise NotImplementedError("Subclasses must implement predict method")
    
    def score(self, X, y):
        """
        Return the score of the model on the given test data and labels.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Test samples
        y : Union[pd.Series, np.ndarray, dd.Series]
            True labels for X
            
        Returns
        -------
        float
            Score of the model
        """
        raise NotImplementedError("Subclasses must implement score method")
    
    def _preprocess_data(self, X, y=None):
        """
        Preprocess input data.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Features
        y : Union[pd.Series, np.ndarray, dd.Series, None], default=None
            Target values
            
        Returns
        -------
        Tuple
            Processed X and y (if provided)
        """
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        # Convert pandas DataFrame to numpy array if needed
        if isinstance(X, pd.DataFrame) and not is_dask:
            X = X.values
        
        # Convert pandas Series to numpy array if needed
        if y is not None and isinstance(y, pd.Series) and not isinstance(y, dd.Series):
            y = y.values
        
        # Check for empty dataset
        if isinstance(X, np.ndarray) and (X.shape[0] == 0 or X.shape[1] == 0):
            raise ValueError("Cannot process empty dataset")
        
        return (X, y) if y is not None else X
    
    def _process_in_chunks(self, X, func, **kwargs):
        """
        Process data in chunks for large datasets.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, np.ndarray]
            Data to process
        func : callable
            Function to apply to each chunk
        **kwargs : dict
            Additional arguments to pass to func
            
        Returns
        -------
        Any
            Result of processing
        """
        if isinstance(X, dd.DataFrame):
            # For Dask DataFrames, use Dask's built-in chunking
            return func(X, **kwargs)
        
        # For pandas DataFrames or numpy arrays
        n_samples = len(X)
        results = []
        
        for i in range(0, n_samples, self.chunk_size):
            chunk = X[i:i+self.chunk_size]
            result = func(chunk, **kwargs)
            results.append(result)
        
        # Combine results
        if isinstance(results[0], np.ndarray):
            return np.concatenate(results)
        elif isinstance(results[0], pd.Series):
            return pd.concat(results)
        else:
            return results
    
    def _check_is_fitted(self):
        """
        Check if the model has been fitted.
        
        Raises
        ------
        RuntimeError
            If the model has not been fitted
        """
        if not self.is_fitted:
            raise RuntimeError("Model has not been fitted yet. Call 'fit' before using this model.") 
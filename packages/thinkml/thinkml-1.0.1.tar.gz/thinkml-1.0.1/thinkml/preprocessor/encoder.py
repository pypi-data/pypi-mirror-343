"""
Encoder module for ThinkML.

This module provides functionality for encoding categorical features.
"""

import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any, Union
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from category_encoders import BinaryEncoder, TargetEncoder
import logging
from collections import defaultdict

# Configure logging
logger = logging.getLogger(__name__)

def encode_categorical(
    data: pd.DataFrame,
    method: str = 'onehot',
    columns: Optional[List[str]] = None,
    handle_unknown: str = 'ignore',
    sparse: bool = True,
    chunk_size: int = 10000,
    target: Optional[pd.Series] = None
) -> pd.DataFrame:
    """
    Encode categorical variables in a DataFrame.

    Args:
        data (pd.DataFrame): Input DataFrame.
        method (str): Encoding method. Options: 'onehot', 'label', 'binary', 'target', 'cyclic'.
            Default is 'onehot'.
        columns (Optional[List[str]]): List of columns to encode. If None, all categorical
            columns will be encoded. Default is None.
        handle_unknown (str): How to handle unknown categories. Options: 'error', 'ignore',
            'use_encoded_value'. Default is 'ignore'.
        sparse (bool): Whether to return a sparse matrix. Default is True.
        chunk_size (int): Number of rows to process at a time. Default is 10000.
        target (Optional[pd.Series]): Target variable for target encoding.
            Required when method is 'target'. Default is None.

    Returns:
        pd.DataFrame: DataFrame with encoded categorical variables.

    Raises:
        ValueError: If method is not supported or if input validation fails.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    if data.empty:
        return data.copy()
    
    if method == 'target' and target is None:
        raise ValueError("Target variable is required for target encoding")
    
    # Get columns to encode
    if columns is None:
        columns = data.select_dtypes(include=['object', 'category']).columns.tolist()

    if not columns:
        return data.copy()

    result = data.copy()

    # Process each column in chunks
    for col in columns:
        if col not in result.columns:
            continue

        # Skip if column is not categorical
        if not pd.api.types.is_categorical_dtype(result[col]) and not pd.api.types.is_object_dtype(result[col]):
            continue

        # Handle mixed data types by converting to string
        if result[col].dtype == 'object' and not all(isinstance(x, str) for x in result[col].dropna()):
            logger.info(f"Converting mixed data types in column '{col}' to strings")
            result[col] = result[col].astype(str)

        # Initialize encoder
        if method == 'onehot':
            encoder = OneHotEncoder(sparse_output=sparse, handle_unknown=handle_unknown)
        elif method == 'label':
            encoder = LabelEncoder()
        elif method == 'binary':
            encoder = BinaryEncoder()
        elif method == 'target':
            encoder = TargetEncoder()
        elif method == 'cyclic':
            # Handle cyclic encoding separately
            if pd.api.types.is_numeric_dtype(result[col]):
                # Create sine and cosine features for cyclic data
                result[f"{col}_sin"] = np.sin(2 * np.pi * result[col] / result[col].max())
                result[f"{col}_cos"] = np.cos(2 * np.pi * result[col] / result[col].max())
                # Drop the original column
                result = result.drop(columns=[col])
                continue
            else:
                logger.warning(f"Column '{col}' is not numeric, skipping cyclic encoding")
                continue
        else:
            raise ValueError(f"Unknown encoding method: {method}")
        
        # Process in chunks
        n_chunks = (len(result) + chunk_size - 1) // chunk_size
        encoded_chunks = []

        for i in range(n_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(result))
            chunk = result.iloc[start_idx:end_idx]
            
            if method == 'label':
                # Label encoding doesn't need to be chunked
                encoded = encoder.fit_transform(chunk[[col]])
                result.loc[start_idx:end_idx-1, col] = encoded
            else:
                # For other methods, we need to fit on the entire column first
                if i == 0:
                    if method == 'target':
                        encoder.fit(result[[col]], target)
                    else:
                        encoder.fit(result[[col]])
                
                # Transform the chunk
                if method == 'target':
                    encoded = encoder.transform(chunk[[col]])
                else:
                    encoded = encoder.transform(chunk[[col]])
                
                if method == 'onehot':
                    # Convert sparse matrix to DataFrame
                    if sparse:
                        encoded_df = pd.DataFrame.sparse.from_spmatrix(
                            encoded,
                            columns=[f"{col}_{j}" for j in range(encoded.shape[1])],
                            index=chunk.index
                        )
                    else:
                        encoded_df = pd.DataFrame(
                            encoded,
                            columns=[f"{col}_{j}" for j in range(encoded.shape[1])],
                            index=chunk.index
                        )
                    encoded_chunks.append(encoded_df)
                else:
                    result.loc[start_idx:end_idx-1, col] = encoded

        # Combine one-hot encoded chunks
        if method == 'onehot' and encoded_chunks:
            encoded_df = pd.concat(encoded_chunks)
            result = pd.concat([result.drop(columns=[col]), encoded_df], axis=1)
    
    return result 
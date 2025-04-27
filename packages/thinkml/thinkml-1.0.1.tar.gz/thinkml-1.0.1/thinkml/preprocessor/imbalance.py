"""
Imbalance handler module for ThinkML.

This module provides functionality for handling imbalanced datasets.
"""

import numpy as np
import pandas as pd
from typing import Union, Optional
from sklearn.utils import resample
import logging

# Configure logging
logger = logging.getLogger(__name__)

def handle_imbalance(
    data: pd.DataFrame,
    target_column: str,
    method: str = 'smote',
    sampling_strategy: Union[float, str, dict] = 'auto',
    random_state: Optional[int] = None
) -> pd.DataFrame:
    """
    Handle imbalanced datasets using various resampling techniques.
    
    Parameters
    ----------
    data : pd.DataFrame
        The dataset to process.
    target_column : str
        The name of the target column.
    method : str, optional
        The resampling method to use. Options are:
        - 'smote': Synthetic Minority Over-sampling Technique
        - 'random_oversample': Random oversampling of minority class
        - 'random_undersample': Random undersampling of majority class
        Default is 'smote'.
    sampling_strategy : Union[float, str, dict], optional
        The sampling strategy to use. Can be:
        - float: The ratio of minority to majority class
        - str: 'auto' for automatic balancing
        - dict: Class-wise sampling ratios
        Default is 'auto'.
    random_state : Optional[int], optional
        Random state for reproducibility.
        Default is None.
        
    Returns
    -------
    pd.DataFrame
        The balanced dataset.
    """
    # Validate input
    if data is None or data.empty:
        raise ValueError("Empty dataset provided")
    
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")
    
    # Separate features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Get class counts
    class_counts = y.value_counts()
    
    # Check if dataset is imbalanced
    if len(class_counts) < 2:
        logger.warning("Dataset has only one class")
        return data
    
    # Calculate imbalance ratio
    majority_class = class_counts.index[0]
    minority_class = class_counts.index[1]
    imbalance_ratio = class_counts[majority_class] / class_counts[minority_class]
    
    if imbalance_ratio < 1.5:
        logger.info("Dataset is not significantly imbalanced")
        return data
    
    # Handle imbalance based on method
    if method == 'random_oversample':
        # Random oversampling of minority class
        X_minority = X[y == minority_class]
        y_minority = y[y == minority_class]
        
        # Resample minority class
        X_resampled, y_resampled = resample(
            X_minority,
            y_minority,
            replace=True,
            n_samples=class_counts[majority_class],
            random_state=random_state
        )
        
        # Combine with majority class
        X_balanced = pd.concat([X[y == majority_class], X_resampled])
        y_balanced = pd.concat([y[y == majority_class], y_resampled])
        
    elif method == 'random_undersample':
        # Random undersampling of majority class
        X_majority = X[y == majority_class]
        y_majority = y[y == majority_class]
        
        # Resample majority class
        X_resampled, y_resampled = resample(
            X_majority,
            y_majority,
            replace=False,
            n_samples=class_counts[minority_class],
            random_state=random_state
        )
        
        # Combine with minority class
        X_balanced = pd.concat([X_resampled, X[y == minority_class]])
        y_balanced = pd.concat([y_resampled, y[y == minority_class]])
        
    elif method == 'smote':
        # For now, use random oversampling as a placeholder
        # TODO: Implement SMOTE
        logger.warning("SMOTE not implemented yet, using random oversampling")
        return handle_imbalance(data, target_column, method='random_oversample',
                              sampling_strategy=sampling_strategy,
                              random_state=random_state)
    
    else:
        raise ValueError(f"Unknown resampling method: {method}")
    
    # Create balanced dataset
    balanced_data = pd.concat([X_balanced, y_balanced], axis=1)
    balanced_data.columns = data.columns
    
    # Log results
    logger.info(f"Dataset balanced using {method}")
    logger.info(f"Original class distribution: {class_counts.to_dict()}")
    logger.info(f"Balanced class distribution: {balanced_data[target_column].value_counts().to_dict()}")
    
    return balanced_data 
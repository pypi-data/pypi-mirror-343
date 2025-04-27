"""
Feature selection module for ThinkML.

This module provides functionality for selecting relevant features for model training.
"""

import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any, Union, Tuple
import logging
from sklearn.feature_selection import (
    VarianceThreshold,
    SelectKBest,
    f_classif,
    f_regression,
    mutual_info_classif,
    mutual_info_regression,
    RFE
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
import scipy.sparse
from thinkml.preprocessor.multicollinearity import (
    detect_multicollinearity,
    resolve_multicollinearity,
    MulticollinearityHandler
)
from thinkml.preprocessor.encoder import encode_categorical

# Configure logging
logger = logging.getLogger(__name__)

def select_features(
    data: pd.DataFrame,
    target: Optional[pd.Series] = None,
    method: str = 'variance',
    threshold: float = 0.0,
    k: Optional[int] = None,
    task: str = 'classification',
    handle_multicollinearity: bool = True,
    multicollinearity_threshold: float = 0.8,
    random_state: int = 42,
    encode_categorical_features: bool = True,
    chunk_size: int = 100000
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Select relevant features for model training.

    Args:
        data (pd.DataFrame): Input DataFrame.
        target (Optional[pd.Series]): Target variable for supervised methods.
            Required for 'mutual_info', 'f_score', 'lasso', 'random_forest', 'rfe'.
            Default is None.
        method (str): Feature selection method. Options: 'variance', 'correlation',
            'mutual_info', 'f_score', 'lasso', 'random_forest', 'rfe', 'vif'.
            Default is 'variance'.
        threshold (float): Threshold for feature selection. Used for 'variance',
            'correlation', and 'vif' methods. Default is 0.0.
        k (Optional[int]): Number of features to select. If None, will use threshold.
            Default is None.
        task (str): Task type. Options: 'classification' or 'regression'.
            Default is 'classification'.
        handle_multicollinearity (bool): Whether to handle multicollinearity.
            Default is True.
        multicollinearity_threshold (float): Threshold for multicollinearity.
            Default is 0.8.
        random_state (int): Random state for reproducibility.
            Default is 42.
        encode_categorical_features (bool): Whether to encode categorical features
            before selection. Default is True.
        chunk_size (int): Number of rows to process at a time for large datasets.
            Default is 100000.

    Returns:
        Tuple[pd.DataFrame, List[str]]: Selected features DataFrame and list of
            selected feature names.

    Raises:
        ValueError: If method is not supported or if input validation fails.
    """
    # Input validation
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if data.empty:
        raise ValueError("Empty dataset provided")

    if method not in ['variance', 'correlation', 'mutual_info', 'f_score',
                     'lasso', 'random_forest', 'rfe', 'vif']:
        raise ValueError(
            "Method must be one of: variance, correlation, mutual_info, f_score, "
            "lasso, random_forest, rfe, vif"
        )

    if task not in ['classification', 'regression']:
        raise ValueError("Task must be one of: classification, regression")

    if method in ['mutual_info', 'f_score', 'lasso', 'random_forest', 'rfe'] and target is None:
        raise ValueError(
            f"Target variable is required for method '{method}'"
        )

    # Convert sparse matrix to dense if needed
    if scipy.sparse.issparse(data):
        logger.info("Converting sparse matrix to dense format")
        data = pd.DataFrame(data.toarray(), columns=[f'col_{i}' for i in range(data.shape[1])])

    # Encode categorical features if requested
    if encode_categorical_features:
        logger.info("Encoding categorical features")
        data = encode_categorical(data, method='onehot', sparse=False)

    # Handle multicollinearity if requested
    if handle_multicollinearity:
        logger.info("Handling multicollinearity")
        data = resolve_multicollinearity(
            data,
            threshold=multicollinearity_threshold
        )

    # Get numeric columns
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_columns:
        raise ValueError("No numeric columns found in the dataset")

    # Process large datasets in chunks
    if len(data) > chunk_size:
        logger.info(f"Processing large dataset in chunks of {chunk_size} rows")
        # Scale features in chunks
        scaler = StandardScaler()
        scaled_chunks = []
        
        for i in range(0, len(data), chunk_size):
            chunk = data.iloc[i:i + chunk_size]
            scaled_chunk = pd.DataFrame(
                scaler.fit_transform(chunk[numeric_columns]),
                columns=numeric_columns,
                index=chunk.index
            )
            scaled_chunks.append(scaled_chunk)
        
        scaled_data = pd.concat(scaled_chunks)
    else:
        # Scale features
        scaler = StandardScaler()
        scaled_data = pd.DataFrame(
            scaler.fit_transform(data[numeric_columns]),
            columns=numeric_columns
        )

    # Select features based on method
    if method == 'variance':
        selector = VarianceThreshold(threshold=threshold)
        selector.fit(scaled_data)
        selected_features = [numeric_columns[i] for i, selected in enumerate(selector.get_support()) if selected]

    elif method == 'correlation':
        corr_matrix = scaled_data.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
        selected_features = [col for col in numeric_columns if col not in to_drop]

    elif method == 'mutual_info':
        k_val = k if k is not None else max(1, int(len(numeric_columns) * (1 - threshold)))
        if task == 'classification':
            selector = SelectKBest(mutual_info_classif, k=k_val)
        else:
            selector = SelectKBest(mutual_info_regression, k=k_val)
        selector.fit(scaled_data, target)
        selected_features = [numeric_columns[i] for i, selected in enumerate(selector.get_support()) if selected]

    elif method == 'f_score':
        k_val = k if k is not None else max(1, int(len(numeric_columns) * (1 - threshold)))
        if task == 'classification':
            selector = SelectKBest(f_classif, k=k_val)
        else:
            selector = SelectKBest(f_regression, k=k_val)
        selector.fit(scaled_data, target)
        selected_features = [numeric_columns[i] for i, selected in enumerate(selector.get_support()) if selected]

    elif method == 'lasso':
        if task == 'classification':
            model = LassoCV(random_state=random_state)
        else:
            model = LassoCV(random_state=random_state)
        model.fit(scaled_data, target)
        selected_features = [numeric_columns[i] for i, coef in enumerate(model.coef_) if abs(coef) > threshold]

    elif method == 'random_forest':
        k_val = k if k is not None else max(1, int(len(numeric_columns) * (1 - threshold)))
        if task == 'classification':
            model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        model.fit(scaled_data, target)
        importances = model.feature_importances_
        selected_features = [numeric_columns[i] for i in np.argsort(importances)[-k_val:]]

    elif method == 'rfe':
        k_val = k if k is not None else max(1, int(len(numeric_columns) * (1 - threshold)))
        if task == 'classification':
            model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        selector = RFE(model, n_features_to_select=k_val)
        selector.fit(scaled_data, target)
        selected_features = [numeric_columns[i] for i, selected in enumerate(selector.support_) if selected]

    elif method == 'vif':
        handler = MulticollinearityHandler(threshold=threshold)
        selected_features = handler.select_features(scaled_data)

    # Return selected features
    return data[selected_features], selected_features

def get_feature_importance(
    data: pd.DataFrame,
    target: pd.Series,
    method: str = 'random_forest',
    task: str = 'classification',
    random_state: int = 42,
    encode_categorical_features: bool = True,
    chunk_size: int = 100000
) -> pd.Series:
    """
    Get feature importance scores.

    Args:
        data (pd.DataFrame): Input DataFrame.
        target (pd.Series): Target variable.
        method (str): Method to use for feature importance. Options: 'random_forest',
            'lasso', 'mutual_info', 'f_score'. Default is 'random_forest'.
        task (str): Task type. Options: 'classification' or 'regression'.
            Default is 'classification'.
        random_state (int): Random state for reproducibility.
            Default is 42.
        encode_categorical_features (bool): Whether to encode categorical features
            before selection. Default is True.
        chunk_size (int): Number of rows to process at a time for large datasets.
            Default is 100000.

    Returns:
        pd.Series: Feature importance scores.

    Raises:
        ValueError: If method is not supported or if input validation fails.
    """
    # Input validation
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if data.empty:
        raise ValueError("Empty dataset provided")

    if method not in ['random_forest', 'lasso', 'mutual_info', 'f_score']:
        raise ValueError(
            "Method must be one of: random_forest, lasso, mutual_info, f_score"
        )

    if task not in ['classification', 'regression']:
        raise ValueError("Task must be one of: classification, regression")

    # Convert sparse matrix to dense if needed
    if scipy.sparse.issparse(data):
        logger.info("Converting sparse matrix to dense format")
        data = pd.DataFrame(data.toarray(), columns=[f'col_{i}' for i in range(data.shape[1])])

    # Encode categorical features if requested
    if encode_categorical_features:
        logger.info("Encoding categorical features")
        data = encode_categorical(data, method='onehot', sparse=False)

    # Get numeric columns
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_columns:
        raise ValueError("No numeric columns found in the dataset")

    # Process large datasets in chunks
    if len(data) > chunk_size:
        logger.info(f"Processing large dataset in chunks of {chunk_size} rows")
        # Scale features in chunks
        scaler = StandardScaler()
        scaled_chunks = []
        
        for i in range(0, len(data), chunk_size):
            chunk = data.iloc[i:i + chunk_size]
            scaled_chunk = pd.DataFrame(
                scaler.fit_transform(chunk[numeric_columns]),
                columns=numeric_columns,
                index=chunk.index
            )
            scaled_chunks.append(scaled_chunk)
        
        scaled_data = pd.concat(scaled_chunks)
    else:
        # Scale features
        scaler = StandardScaler()
        scaled_data = pd.DataFrame(
            scaler.fit_transform(data[numeric_columns]),
            columns=numeric_columns
        )

    # Calculate feature importance
    if method == 'random_forest':
        if task == 'classification':
            model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        model.fit(scaled_data, target)
        importance = pd.Series(model.feature_importances_, index=numeric_columns)

    elif method == 'lasso':
        if task == 'classification':
            model = LassoCV(random_state=random_state)
        else:
            model = LassoCV(random_state=random_state)
        model.fit(scaled_data, target)
        importance = pd.Series(np.abs(model.coef_), index=numeric_columns)

    elif method == 'mutual_info':
        if task == 'classification':
            importance = mutual_info_classif(scaled_data, target)
        else:
            importance = mutual_info_regression(scaled_data, target)
        importance = pd.Series(importance, index=numeric_columns)

    elif method == 'f_score':
        if task == 'classification':
            importance = f_classif(scaled_data, target)[0]
        else:
            importance = f_regression(scaled_data, target)[0]
        importance = pd.Series(importance, index=numeric_columns)

    # Sort importance scores
    importance = importance.sort_values(ascending=False)

    return importance 
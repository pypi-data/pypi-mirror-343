"""
Model evaluation functionality for ThinkML.

This module provides functions for evaluating machine learning models
with various metrics for both classification and regression tasks.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Dict, Union, List, Any, Optional, Literal
import dask.array as da
from collections import Counter

def evaluate_model(
    model: Any,
    X_test: Union[pd.DataFrame, dd.DataFrame, np.ndarray],
    y_test: Union[pd.Series, np.ndarray, dd.Series],
    problem_type: str = 'classification',
    metrics: Union[str, List[str]] = 'auto'
) -> Dict[str, float]:
    """
    Evaluate a trained model using various metrics.
    
    Parameters
    ----------
    model : Any
        Trained model object with predict method
    X_test : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
        Test features
    y_test : Union[pd.Series, np.ndarray, dd.Series]
        True labels/values
    problem_type : str, default='classification'
        Type of problem: 'classification' or 'regression'
    metrics : Union[str, List[str]], default='auto'
        Metrics to compute. Options:
        - 'auto': Automatically select appropriate metrics
        - List of specific metrics to compute
        
    Returns
    -------
    Dict[str, float]
        Dictionary of metric name -> metric value
    """
    # Input validation
    if problem_type not in ['classification', 'regression']:
        raise ValueError("problem_type must be 'classification' or 'regression'")
    
    # Check if we're working with Dask DataFrames
    is_dask = isinstance(X_test, dd.DataFrame) or isinstance(y_test, dd.Series)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Auto-select metrics if requested
    if metrics == 'auto':
        if problem_type == 'classification':
            metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        else:  # regression
            metrics = ['r2', 'mse', 'rmse', 'mae']
    
    # Ensure metrics is a list
    if isinstance(metrics, str):
        metrics = [metrics]
    
    # Compute requested metrics
    results = {}
    
    if problem_type == 'classification':
        # Convert to numpy arrays for metric computation if needed
        if is_dask:
            y_test_np = y_test.compute() if isinstance(y_test, dd.Series) else y_test
            y_pred_np = y_pred.compute() if isinstance(y_pred, dd.Series) else y_pred
        else:
            y_test_np = y_test
            y_pred_np = y_pred
        
        # Compute classification metrics
        for metric in metrics:
            if metric == 'accuracy':
                results['accuracy'] = _accuracy_score(y_test_np, y_pred_np)
            elif metric == 'precision':
                results['precision'] = _precision_score(y_test_np, y_pred_np)
            elif metric == 'recall':
                results['recall'] = _recall_score(y_test_np, y_pred_np)
            elif metric == 'f1':
                results['f1'] = _f1_score(y_test_np, y_pred_np)
            elif metric == 'roc_auc':
                results['roc_auc'] = _roc_auc_score(y_test_np, y_pred_np)
            elif metric == 'confusion_matrix':
                results['confusion_matrix'] = _confusion_matrix(y_test_np, y_pred_np)
    else:  # regression
        # Convert to numpy arrays for metric computation if needed
        if is_dask:
            y_test_np = y_test.compute() if isinstance(y_test, dd.Series) else y_test
            y_pred_np = y_pred.compute() if isinstance(y_pred, dd.Series) else y_pred
        else:
            y_test_np = y_test
            y_pred_np = y_pred
        
        # Compute regression metrics
        for metric in metrics:
            if metric == 'r2':
                results['r2'] = _r2_score(y_test_np, y_pred_np)
            elif metric == 'mse':
                results['mse'] = _mean_squared_error(y_test_np, y_pred_np)
            elif metric == 'rmse':
                results['rmse'] = np.sqrt(_mean_squared_error(y_test_np, y_pred_np))
            elif metric == 'mae':
                results['mae'] = _mean_absolute_error(y_test_np, y_pred_np)
    
    return results

# Classification metrics implementations
def _accuracy_score(y_true, y_pred):
    """Compute accuracy score."""
    return np.mean(y_true == y_pred)

def _precision_score(y_true, y_pred):
    """Compute precision score."""
    # Handle binary classification
    if len(np.unique(y_true)) == 2:
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        return tp / (tp + fp) if (tp + fp) > 0 else 0
    
    # Handle multiclass classification
    precision = 0
    classes = np.unique(y_true)
    for c in classes:
        tp = np.sum((y_true == c) & (y_pred == c))
        fp = np.sum((y_true != c) & (y_pred == c))
        precision += tp / (tp + fp) if (tp + fp) > 0 else 0
    
    return precision / len(classes)

def _recall_score(y_true, y_pred):
    """Compute recall score."""
    # Handle binary classification
    if len(np.unique(y_true)) == 2:
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        return tp / (tp + fn) if (tp + fn) > 0 else 0
    
    # Handle multiclass classification
    recall = 0
    classes = np.unique(y_true)
    for c in classes:
        tp = np.sum((y_true == c) & (y_pred == c))
        fn = np.sum((y_true == c) & (y_pred != c))
        recall += tp / (tp + fn) if (tp + fn) > 0 else 0
    
    return recall / len(classes)

def _f1_score(y_true, y_pred):
    """Compute F1 score."""
    precision = _precision_score(y_true, y_pred)
    recall = _recall_score(y_true, y_pred)
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

def _roc_auc_score(y_true, y_pred):
    """
    Compute ROC AUC score.
    
    Note: This is a simplified implementation that assumes binary classification
    and that the model outputs probabilities for the positive class.
    """
    # For binary classification only
    if len(np.unique(y_true)) != 2:
        raise ValueError("ROC AUC is only defined for binary classification")
    
    # Sort by prediction probability
    sorted_indices = np.argsort(y_pred)[::-1]
    y_true_sorted = y_true[sorted_indices]
    
    # Calculate TPR and FPR at each threshold
    n_pos = np.sum(y_true == 1)
    n_neg = np.sum(y_true == 0)
    
    tpr = np.zeros_like(y_true, dtype=float)
    fpr = np.zeros_like(y_true, dtype=float)
    
    tp = 0
    fp = 0
    
    for i in range(len(y_true_sorted)):
        if y_true_sorted[i] == 1:
            tp += 1
        else:
            fp += 1
        
        tpr[i] = tp / n_pos if n_pos > 0 else 0
        fpr[i] = fp / n_neg if n_neg > 0 else 0
    
    # Calculate AUC using trapezoidal rule
    auc = 0
    for i in range(1, len(tpr)):
        auc += (fpr[i] - fpr[i-1]) * (tpr[i] + tpr[i-1]) / 2
    
    return auc

def _confusion_matrix(y_true, y_pred):
    """Compute confusion matrix."""
    classes = np.unique(y_true)
    n_classes = len(classes)
    cm = np.zeros((n_classes, n_classes), dtype=int)
    
    for i, true_class in enumerate(classes):
        for j, pred_class in enumerate(classes):
            cm[i, j] = np.sum((y_true == true_class) & (y_pred == pred_class))
    
    return cm

# Regression metrics implementations
def _r2_score(y_true, y_pred):
    """Compute R² score."""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

def _mean_squared_error(y_true, y_pred):
    """Compute mean squared error."""
    return np.mean((y_true - y_pred) ** 2)

def _mean_absolute_error(y_true, y_pred):
    """Compute mean absolute error."""
    return np.mean(np.abs(y_true - y_pred))

def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute confusion matrix.
    
    Parameters
    ----------
    y_true : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels
        
    Returns
    -------
    np.ndarray
        2x2 confusion matrix
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    # Get unique classes
    classes = np.unique(np.concatenate([y_true, y_pred]))
    n_classes = len(classes)
    
    # Initialize confusion matrix
    cm = np.zeros((n_classes, n_classes), dtype=int)
    
    # Fill confusion matrix
    for i in range(n_classes):
        for j in range(n_classes):
            cm[i, j] = np.sum((y_true == classes[i]) & (y_pred == classes[j]))
            
    return cm

def roc_auc_score(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """
    Compute ROC-AUC score.
    
    Parameters
    ----------
    y_true : np.ndarray
        True labels
    y_score : np.ndarray
        Target scores/probabilities
        
    Returns
    -------
    float
        ROC-AUC score
    """
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    
    # Sort scores and corresponding true labels
    sorted_indices = np.argsort(y_score)[::-1]
    y_true_sorted = y_true[sorted_indices]
    
    # Calculate true positive and false positive rates
    tp = np.cumsum(y_true_sorted == 1)
    fp = np.cumsum(y_true_sorted == 0)
    
    # Calculate total positives and negatives
    n_pos = np.sum(y_true == 1)
    n_neg = np.sum(y_true == 0)
    
    # Calculate TPR and FPR
    tpr = tp / n_pos if n_pos > 0 else np.zeros_like(tp)
    fpr = fp / n_neg if n_neg > 0 else np.zeros_like(fp)
    
    # Calculate AUC using trapezoidal rule
    auc = np.trapz(tpr, fpr)
    
    return auc

def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute mean squared error.
    
    Parameters
    ----------
    y_true : np.ndarray
        True values
    y_pred : np.ndarray
        Predicted values
        
    Returns
    -------
    float
        Mean squared error
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    return np.mean((y_true - y_pred) ** 2)

def root_mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute root mean squared error.
    
    Parameters
    ----------
    y_true : np.ndarray
        True values
    y_pred : np.ndarray
        Predicted values
        
    Returns
    -------
    float
        Root mean squared error
    """
    return np.sqrt(mean_squared_error(y_true, y_pred))

def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute mean absolute error.
    
    Parameters
    ----------
    y_true : np.ndarray
        True values
    y_pred : np.ndarray
        Predicted values
        
    Returns
    -------
    float
        Mean absolute error
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    return np.mean(np.abs(y_true - y_pred))

def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute R² score.
    
    Parameters
    ----------
    y_true : np.ndarray
        True values
    y_pred : np.ndarray
        Predicted values
        
    Returns
    -------
    float
        R² score
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    # Calculate total sum of squares
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    
    # Calculate residual sum of squares
    ss_res = np.sum((y_true - y_pred) ** 2)
    
    # Calculate R²
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    return r2

def evaluate_regression(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Evaluate regression model performance.
    
    Parameters
    ----------
    y_true : np.ndarray
        True values
    y_pred : np.ndarray
        Predicted values
        
    Returns
    -------
    Dict[str, float]
        Dictionary containing regression metrics
    """
    return {
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': root_mean_squared_error(y_true, y_pred),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred)
    }

def evaluate_classification(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: Optional[np.ndarray] = None
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Evaluate classification model performance.
    
    Parameters
    ----------
    y_true : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels
    y_score : Optional[np.ndarray], optional
        Target scores/probabilities for ROC-AUC
        
    Returns
    -------
    Dict[str, Union[float, np.ndarray]]
        Dictionary containing classification metrics
    """
    metrics = {
        'confusion_matrix': confusion_matrix(y_true, y_pred)
    }
    
    if y_score is not None:
        metrics['roc_auc'] = roc_auc_score(y_true, y_score)
        
    return metrics 
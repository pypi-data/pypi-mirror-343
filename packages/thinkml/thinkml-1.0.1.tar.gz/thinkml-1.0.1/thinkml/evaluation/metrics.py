"""
Evaluation metrics for ThinkML.

This module provides implementations of common evaluation metrics
for machine learning models.
"""

import numpy as np
from typing import Union, List, Optional, Tuple


def accuracy_score(y_true: Union[np.ndarray, List], y_pred: Union[np.ndarray, List]) -> float:
    """
    Calculate the accuracy score for classification.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        
    Returns:
        Accuracy score between 0 and 1
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    
    return np.mean(y_true == y_pred)


def f1_score(y_true: Union[np.ndarray, List], y_pred: Union[np.ndarray, List], 
            average: str = 'weighted') -> float:
    """
    Calculate the F1 score for classification.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        average: Averaging strategy ('binary', 'micro', 'macro', 'weighted')
        
    Returns:
        F1 score between 0 and 1
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    
    # Get unique classes
    classes = np.unique(np.concatenate([y_true, y_pred]))
    
    if len(classes) == 2 and average == 'binary':
        # Binary classification
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    elif average == 'micro':
        # Micro-averaging
        tp = np.sum(y_true == y_pred)
        fp = np.sum(y_true != y_pred)
        fn = fp  # For micro-averaging, FP = FN
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    elif average == 'macro':
        # Macro-averaging
        f1_scores = []
        
        for c in classes:
            y_true_binary = (y_true == c).astype(int)
            y_pred_binary = (y_pred == c).astype(int)
            
            tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
            fp = np.sum((y_true_binary == 0) & (y_pred_binary == 1))
            fn = np.sum((y_true_binary == 1) & (y_pred_binary == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            f1_scores.append(f1)
        
        return np.mean(f1_scores)
    
    elif average == 'weighted':
        # Weighted-averaging
        f1_scores = []
        weights = []
        
        for c in classes:
            y_true_binary = (y_true == c).astype(int)
            y_pred_binary = (y_pred == c).astype(int)
            
            tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
            fp = np.sum((y_true_binary == 0) & (y_pred_binary == 1))
            fn = np.sum((y_true_binary == 1) & (y_pred_binary == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            f1_scores.append(f1)
            
            # Weight by the number of samples in this class
            weight = np.sum(y_true == c)
            weights.append(weight)
        
        weights = np.array(weights) / np.sum(weights)
        return np.sum(f1_scores * weights)
    
    else:
        raise ValueError(f"Unsupported average: {average}")


def mean_squared_error(y_true: Union[np.ndarray, List], y_pred: Union[np.ndarray, List]) -> float:
    """
    Calculate the mean squared error for regression.
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
        
    Returns:
        Mean squared error
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    
    return np.mean((y_true - y_pred) ** 2)


def r2_score(y_true: Union[np.ndarray, List], y_pred: Union[np.ndarray, List]) -> float:
    """
    Calculate the R² score for regression.
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
        
    Returns:
        R² score (can be negative for poorly performing models)
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    
    return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0


def precision_score(y_true: Union[np.ndarray, List], y_pred: Union[np.ndarray, List], 
                  average: str = 'weighted') -> float:
    """
    Calculate the precision score for classification.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        average: Averaging strategy ('binary', 'micro', 'macro', 'weighted')
        
    Returns:
        Precision score between 0 and 1
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    
    # Get unique classes
    classes = np.unique(np.concatenate([y_true, y_pred]))
    
    if len(classes) == 2 and average == 'binary':
        # Binary classification
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        
        return tp / (tp + fp) if (tp + fp) > 0 else 0
    
    elif average == 'micro':
        # Micro-averaging
        tp = np.sum(y_true == y_pred)
        fp = np.sum(y_true != y_pred)
        
        return tp / (tp + fp) if (tp + fp) > 0 else 0
    
    elif average == 'macro':
        # Macro-averaging
        precision_scores = []
        
        for c in classes:
            y_true_binary = (y_true == c).astype(int)
            y_pred_binary = (y_pred == c).astype(int)
            
            tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
            fp = np.sum((y_true_binary == 0) & (y_pred_binary == 1))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            precision_scores.append(precision)
        
        return np.mean(precision_scores)
    
    elif average == 'weighted':
        # Weighted-averaging
        precision_scores = []
        weights = []
        
        for c in classes:
            y_true_binary = (y_true == c).astype(int)
            y_pred_binary = (y_pred == c).astype(int)
            
            tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
            fp = np.sum((y_true_binary == 0) & (y_pred_binary == 1))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            precision_scores.append(precision)
            
            # Weight by the number of samples in this class
            weight = np.sum(y_true == c)
            weights.append(weight)
        
        weights = np.array(weights) / np.sum(weights)
        return np.sum(precision_scores * weights)
    
    else:
        raise ValueError(f"Unsupported average: {average}")


def recall_score(y_true: Union[np.ndarray, List], y_pred: Union[np.ndarray, List], 
               average: str = 'weighted') -> float:
    """
    Calculate the recall score for classification.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        average: Averaging strategy ('binary', 'micro', 'macro', 'weighted')
        
    Returns:
        Recall score between 0 and 1
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    
    # Get unique classes
    classes = np.unique(np.concatenate([y_true, y_pred]))
    
    if len(classes) == 2 and average == 'binary':
        # Binary classification
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        
        return tp / (tp + fn) if (tp + fn) > 0 else 0
    
    elif average == 'micro':
        # Micro-averaging
        tp = np.sum(y_true == y_pred)
        fn = np.sum(y_true != y_pred)
        
        return tp / (tp + fn) if (tp + fn) > 0 else 0
    
    elif average == 'macro':
        # Macro-averaging
        recall_scores = []
        
        for c in classes:
            y_true_binary = (y_true == c).astype(int)
            y_pred_binary = (y_pred == c).astype(int)
            
            tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
            fn = np.sum((y_true_binary == 1) & (y_pred_binary == 0))
            
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            recall_scores.append(recall)
        
        return np.mean(recall_scores)
    
    elif average == 'weighted':
        # Weighted-averaging
        recall_scores = []
        weights = []
        
        for c in classes:
            y_true_binary = (y_true == c).astype(int)
            y_pred_binary = (y_pred == c).astype(int)
            
            tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
            fn = np.sum((y_true_binary == 1) & (y_pred_binary == 0))
            
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            recall_scores.append(recall)
            
            # Weight by the number of samples in this class
            weight = np.sum(y_true == c)
            weights.append(weight)
        
        weights = np.array(weights) / np.sum(weights)
        return np.sum(recall_scores * weights)
    
    else:
        raise ValueError(f"Unsupported average: {average}")


def confusion_matrix(y_true: Union[np.ndarray, List], y_pred: Union[np.ndarray, List]) -> np.ndarray:
    """
    Calculate the confusion matrix for classification.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        
    Returns:
        Confusion matrix as a 2D numpy array
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    
    # Get unique classes
    classes = np.unique(np.concatenate([y_true, y_pred]))
    n_classes = len(classes)
    
    # Initialize confusion matrix
    cm = np.zeros((n_classes, n_classes), dtype=int)
    
    # Fill confusion matrix
    for i, true_class in enumerate(classes):
        for j, pred_class in enumerate(classes):
            cm[i, j] = np.sum((y_true == true_class) & (y_pred == pred_class))
    
    return cm 
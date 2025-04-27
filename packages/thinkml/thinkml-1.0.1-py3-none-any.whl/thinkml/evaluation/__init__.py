"""
Model evaluation module for ThinkML.

This module provides functionality for evaluating machine learning models
with various metrics for both classification and regression tasks.
"""

from .evaluator import evaluate_model
from .metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_squared_error,
    r2_score,
    confusion_matrix
)

__all__ = [
    'evaluate_model',
    'accuracy_score',
    'precision_score',
    'recall_score',
    'f1_score',
    'mean_squared_error',
    'r2_score',
    'confusion_matrix'
] 
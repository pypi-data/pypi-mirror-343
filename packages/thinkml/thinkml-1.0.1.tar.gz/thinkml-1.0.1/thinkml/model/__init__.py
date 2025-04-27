"""
Model training and prediction module for ThinkML.

This module provides functionality for training multiple models,
evaluating their performance, and making predictions.
"""

from .trainer import train_multiple_models, predict_with_model

__all__ = ['train_multiple_models', 'predict_with_model'] 
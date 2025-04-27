"""
Preprocessor module for ThinkML.

This module provides functionality for preprocessing data before model training.
"""

from thinkml.preprocessor.missing_values import handle_missing_values
from thinkml.preprocessor.encoder import encode_categorical
from thinkml.preprocessor.scaler import scale_features
from thinkml.preprocessor.multicollinearity import (
    detect_multicollinearity,
    resolve_multicollinearity,
    MulticollinearityHandler
)
from thinkml.preprocessor.imbalance import handle_imbalance

__all__ = [
    'handle_missing_values',
    'encode_categorical',
    'scale_features',
    'detect_multicollinearity',
    'resolve_multicollinearity',
    'MulticollinearityHandler',
    'handle_imbalance'
] 
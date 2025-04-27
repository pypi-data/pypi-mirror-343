"""
Feature selection module for ThinkML.

This module provides functionality for selecting relevant features for model training.
"""

from .selector import select_features, get_feature_importance

__all__ = [
    'select_features',
    'get_feature_importance'
]

__version__ = "0.1.0" 
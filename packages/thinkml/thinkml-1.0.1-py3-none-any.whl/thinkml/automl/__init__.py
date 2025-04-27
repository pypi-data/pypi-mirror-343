"""
AutoML module for ThinkML library.

This module provides automated machine learning capabilities including
data preprocessing, model selection, and hyperparameter tuning.
"""

from .pipeline import automl_pipeline

__version__ = '0.1.0'

__all__ = ['automl_pipeline'] 
"""
Model persistence module for ThinkML.

This module provides utilities for saving and loading machine learning models
in various formats.
"""

from .model_saver import save_model, load_model

__version__ = '0.1.0'

__all__ = ['save_model', 'load_model'] 
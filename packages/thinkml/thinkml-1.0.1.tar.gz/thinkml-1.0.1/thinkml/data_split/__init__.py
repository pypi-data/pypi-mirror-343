"""
Data splitting module for ThinkML.

This module provides functionality for standardizing and splitting datasets
into training and testing sets with various scaling options.
"""

from .splitter import standardize_and_split, train_test_split

__all__ = ['standardize_and_split', 'train_test_split'] 
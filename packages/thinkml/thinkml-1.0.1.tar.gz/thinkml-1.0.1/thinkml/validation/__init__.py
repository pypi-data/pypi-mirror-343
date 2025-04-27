"""
Validation module for ThinkML.

This module provides cross-validation functionality for machine learning models.
"""

from .cross_validator import cross_validate
from .cross_validation import NestedCrossValidator
from .time_series import TimeSeriesValidator
from .stratified_group import StratifiedGroupValidator
from .bootstrap import BootstrapValidator

__version__ = "0.1.0"
__all__ = [
    'NestedCrossValidator',
    'TimeSeriesValidator',
    'StratifiedGroupValidator',
    'BootstrapValidator'
] 
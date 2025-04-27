"""
Calibration Module for ThinkML.

This module provides functions for probability calibration and evaluation.
"""

from .probability_calibration import calibrate_probabilities, plot_reliability_diagram

__all__ = ['calibrate_probabilities', 'plot_reliability_diagram']
__version__ = "0.1.0" 
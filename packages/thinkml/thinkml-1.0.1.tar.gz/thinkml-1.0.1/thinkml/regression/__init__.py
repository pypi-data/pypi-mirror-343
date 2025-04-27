"""
Advanced regression models for ThinkML.
"""

from thinkml.regression.quantile_regression import QuantileRegressor
from thinkml.regression.robust_regression import RobustRegressor
from thinkml.regression.censored_regression import CensoredRegressor

__version__ = "1.0.0"
__all__ = [
    "QuantileRegressor",
    "RobustRegressor",
    "CensoredRegressor"
] 
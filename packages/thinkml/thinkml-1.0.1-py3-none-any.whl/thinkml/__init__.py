"""
ThinkML - A comprehensive machine learning library that extends scikit-learn
with advanced functionality for model development, validation, optimization, and interpretation.
"""

from thinkml.helpers.user_interface import ThinkML
from thinkml.validation import (
    NestedCrossValidator,
    TimeSeriesValidator,
    StratifiedGroupValidator,
    BootstrapValidator
)
from thinkml.optimization import (
    EarlyStopping,
    GPUAccelerator,
    ParallelProcessor
)
from thinkml.selection import (
    BayesianOptimizer,
    MultiObjectiveOptimizer
)
from thinkml.feature_engineering import (
    create_features,
    select_features
)
from thinkml.interpretability import (
    explain_model,
    get_feature_importance
)
from thinkml.regression import (
    QuantileRegressor,
    RobustRegressor,
    CensoredRegressor
)
from thinkml.classification import (
    MultiLabelClassifier,
    CostSensitiveClassifier,
    OrdinalClassifier
)
from thinkml.calibration import (
    calibrate_probabilities,
    plot_reliability_diagram
)
from thinkml.utils import (
    preprocess_data,
    evaluate_model
)

__version__ = "1.0.0"
__all__ = [
    "ThinkML",
    "NestedCrossValidator",
    "TimeSeriesValidator",
    "StratifiedGroupValidator",
    "BootstrapValidator",
    "EarlyStopping",
    "GPUAccelerator",
    "ParallelProcessor",
    "BayesianOptimizer",
    "MultiObjectiveOptimizer",
    "create_features",
    "select_features",
    "explain_model",
    "get_feature_importance",
    "QuantileRegressor",
    "RobustRegressor",
    "CensoredRegressor",
    "MultiLabelClassifier",
    "CostSensitiveClassifier",
    "OrdinalClassifier",
    "calibrate_probabilities",
    "plot_reliability_diagram",
    "preprocess_data",
    "evaluate_model"
] 
"""
Advanced classification models for ThinkML.
"""

from thinkml.classification.multi_label import MultiLabelClassifier
from thinkml.classification.cost_sensitive import CostSensitiveClassifier
from thinkml.classification.ordinal_classification import OrdinalClassifier

__version__ = "1.0.0"
__all__ = [
    "MultiLabelClassifier",
    "CostSensitiveClassifier",
    "OrdinalClassifier"
] 
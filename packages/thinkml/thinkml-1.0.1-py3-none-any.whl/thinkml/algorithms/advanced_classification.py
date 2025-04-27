"""
Advanced classification algorithms for ThinkML.
Implements multi-label classification, cost-sensitive learning, and class imbalance handling.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek

class MultiLabelClassifier(BaseEstimator, ClassifierMixin):
    """Multi-label classification implementation."""
    
    def __init__(
        this,
        base_estimator: BaseEstimator,
        threshold: float = 0.5
    ):
        this.base_estimator = base_estimator
        this.threshold = threshold
        this.classifiers = None
        this.classes_ = None
    
    def fit(this, X: pd.DataFrame, y: pd.DataFrame) -> "MultiLabelClassifier":
        """Fit the multi-label classifier."""
        this.classes_ = y.columns
        this.classifiers = {}
        
        for label in this.classes_:
            classifier = OneVsRestClassifier(this.base_estimator)
            classifier.fit(X, y[label])
            this.classifiers[label] = classifier
        
        return this
    
    def predict(this, X: pd.DataFrame) -> pd.DataFrame:
        """Make predictions."""
        predictions = {}
        
        for label, classifier in this.classifiers.items():
            proba = classifier.predict_proba(X)[:, 1]
            predictions[label] = (proba >= this.threshold).astype(int)
        
        return pd.DataFrame(predictions)
    
    def predict_proba(this, X: pd.DataFrame) -> pd.DataFrame:
        """Predict class probabilities."""
        probabilities = {}
        
        for label, classifier in this.classifiers.items():
            probabilities[label] = classifier.predict_proba(X)[:, 1]
        
        return pd.DataFrame(probabilities)

class CostSensitiveClassifier(BaseEstimator, ClassifierMixin):
    """Cost-sensitive classification implementation."""
    
    def __init__(
        this,
        base_estimator: BaseEstimator,
        cost_matrix: Optional[np.ndarray] = None
    ):
        this.base_estimator = base_estimator
        this.cost_matrix = cost_matrix
        this.model = None
        this.classes_ = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "CostSensitiveClassifier":
        """Fit the cost-sensitive classifier."""
        this.classes_ = np.unique(y)
        
        if this.cost_matrix is None:
            # Default cost matrix: higher cost for false negatives
            this.cost_matrix = np.array([
                [0, 1],
                [2, 0]
            ])
        
        # Adjust sample weights based on cost matrix
        sample_weights = np.zeros(len(y))
        for i, label in enumerate(y):
            for j, pred in enumerate(this.classes_):
                sample_weights[i] += this.cost_matrix[label, j]
        
        this.model = this.base_estimator
        this.model.fit(X, y, sample_weight=sample_weights)
        return this
    
    def predict(this, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        return this.model.predict(X)
    
    def predict_proba(this, X: pd.DataFrame) -> np.ndarray:
        """Predict class probabilities."""
        if hasattr(this.model, "predict_proba"):
            return this.model.predict_proba(X)
        else:
            raise ValueError("Base estimator does not support probability predictions")

class ImbalancedClassifier(BaseEstimator, ClassifierMixin):
    """Class imbalance handling implementation."""
    
    def __init__(
        this,
        base_estimator: BaseEstimator,
        sampling_strategy: str = "auto",
        sampling_method: str = "smote"
    ):
        this.base_estimator = base_estimator
        this.sampling_strategy = sampling_strategy
        this.sampling_method = sampling_method
        this.pipeline = None
        this.classes_ = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "ImbalancedClassifier":
        """Fit the imbalanced classifier."""
        this.classes_ = np.unique(y)
        
        if this.sampling_method == "smote":
            sampler = SMOTE(sampling_strategy=this.sampling_strategy)
        elif this.sampling_method == "undersampling":
            sampler = RandomUnderSampler(sampling_strategy=this.sampling_strategy)
        elif this.sampling_method == "combined":
            sampler = SMOTETomek(sampling_strategy=this.sampling_strategy)
        else:
            raise ValueError(f"Unknown sampling method: {this.sampling_method}")
        
        this.pipeline = Pipeline([
            ("sampler", sampler),
            ("classifier", this.base_estimator)
        ])
        
        this.pipeline.fit(X, y)
        return this
    
    def predict(this, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        return this.pipeline.predict(X)
    
    def predict_proba(this, X: pd.DataFrame) -> np.ndarray:
        """Predict class probabilities."""
        return this.pipeline.predict_proba(X)

class ProbabilityCalibrator:
    """Probability calibration implementation."""
    
    def __init__(
        this,
        base_estimator: BaseEstimator,
        method: str = "sigmoid",
        cv: int = 5
    ):
        this.base_estimator = base_estimator
        this.method = method
        this.cv = cv
        this.calibrated_model = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "ProbabilityCalibrator":
        """Fit the probability calibrator."""
        this.calibrated_model = CalibratedClassifierCV(
            base_estimator=this.base_estimator,
            method=this.method,
            cv=this.cv
        )
        this.calibrated_model.fit(X, y)
        return this
    
    def predict(this, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        return this.calibrated_model.predict(X)
    
    def predict_proba(this, X: pd.DataFrame) -> np.ndarray:
        """Predict calibrated probabilities."""
        return this.calibrated_model.predict_proba(X)

def plot_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
    title: str = "Classification Results"
) -> None:
    """Plot classification metrics and ROC curve."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax1)
    ax1.set_title("Confusion Matrix")
    ax1.set_xlabel("Predicted")
    ax1.set_ylabel("True")
    
    # ROC Curve (if probabilities are provided)
    if y_prob is not None:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = roc_auc_score(y_true, y_prob)
        ax2.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
        ax2.plot([0, 1], [0, 1], "k--")
        ax2.set_xlim([0.0, 1.0])
        ax2.set_ylim([0.0, 1.05])
        ax2.set_xlabel("False Positive Rate")
        ax2.set_ylabel("True Positive Rate")
        ax2.set_title("ROC Curve")
        ax2.legend(loc="lower right")
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()
    
    # Print metrics
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall: {recall_score(y_true, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_true, y_pred):.4f}")

def plot_class_distribution(
    y: pd.Series,
    title: str = "Class Distribution"
) -> None:
    """Plot class distribution."""
    plt.figure(figsize=(10, 6))
    y.value_counts().plot(kind="bar")
    plt.title(title)
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_decision_boundary(
    model: BaseEstimator,
    X: pd.DataFrame,
    y: pd.Series,
    resolution: int = 100
) -> None:
    """Plot decision boundary for binary classification."""
    if len(X.columns) != 2:
        raise ValueError("Decision boundary plot requires exactly 2 features")
    
    if not hasattr(model, "predict_proba"):
        raise ValueError("Model must support probability predictions")
    
    x_min, x_max = X[X.columns[0]].min() - 1, X[X.columns[0]].max() + 1
    y_min, y_max = X[X.columns[1]].min() - 1, X[X.columns[1]].max() + 1
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, resolution),
        np.linspace(y_min, y_max, resolution)
    )
    
    Z = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(
        X[X.columns[0]],
        X[X.columns[1]],
        c=y,
        alpha=0.8
    )
    plt.title("Decision Boundary")
    plt.xlabel(X.columns[0])
    plt.ylabel(X.columns[1])
    plt.colorbar()
    plt.tight_layout()
    plt.show() 
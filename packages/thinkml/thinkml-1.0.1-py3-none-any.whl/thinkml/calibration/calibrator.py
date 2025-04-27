"""
Model calibration utilities for ThinkML.
Implements Platt scaling, isotonic regression, and temperature scaling.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.calibration import CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import brier_score_loss, log_loss
import matplotlib.pyplot as plt
import seaborn as sns

class ModelCalibrator:
    """Advanced model calibration utilities."""
    
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
        this.calibration_curve = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "ModelCalibrator":
        """Fit the calibrated model."""
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

class TemperatureScaler:
    """Temperature scaling implementation."""
    
    def __init__(this, temperature: float = 1.0):
        this.temperature = temperature
        this.optimal_temperature = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "TemperatureScaler":
        """Find optimal temperature parameter."""
        def objective(t):
            scaled_probs = this._scale_probs(X, t)
            return log_loss(y, scaled_probs)
        
        # Simple grid search for optimal temperature
        temperatures = np.linspace(0.1, 5.0, 50)
        losses = [objective(t) for t in temperatures]
        this.optimal_temperature = temperatures[np.argmin(losses)]
        return this
    
    def _scale_probs(this, X: pd.DataFrame, temperature: float) -> np.ndarray:
        """Scale probabilities using temperature."""
        logits = np.log(X / (1 - X))
        scaled_logits = logits / temperature
        return 1 / (1 + np.exp(-scaled_logits))
    
    def transform(this, X: pd.DataFrame) -> np.ndarray:
        """Transform probabilities using optimal temperature."""
        if this.optimal_temperature is None:
            raise ValueError("Model has not been fitted yet")
        return this._scale_probs(X, this.optimal_temperature)

class IsotonicCalibrator:
    """Isotonic regression calibration implementation."""
    
    def __init__(this):
        this.calibrator = None
        this.calibration_curve = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "IsotonicCalibrator":
        """Fit the isotonic calibrator."""
        this.calibrator = IsotonicRegression(out_of_bounds="clip")
        this.calibrator.fit(X, y)
        return this
    
    def transform(this, X: pd.DataFrame) -> np.ndarray:
        """Transform probabilities using isotonic regression."""
        if this.calibrator is None:
            raise ValueError("Model has not been fitted yet")
        return this.calibrator.transform(X)

def plot_calibration_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
    title: str = "Calibration Curve"
) -> None:
    """Plot calibration curve."""
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins)
    
    plt.figure(figsize=(10, 6))
    plt.plot([0, 1], [0, 1], "k--", label="Perfectly Calibrated")
    plt.plot(prob_pred, prob_true, "s-", label="Model")
    plt.xlabel("Mean Predicted Probability")
    plt.ylabel("True Probability")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Print calibration metrics
    brier = brier_score_loss(y_true, y_prob)
    print(f"Brier Score: {brier:.4f}")

def plot_reliability_diagram(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
    title: str = "Reliability Diagram"
) -> None:
    """Plot reliability diagram."""
    bin_edges = np.linspace(0, 1, n_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    bin_counts = np.histogram(y_prob, bins=bin_edges)[0]
    bin_sums = np.histogram(y_prob, bins=bin_edges, weights=y_true)[0]
    bin_means = np.zeros_like(bin_centers)
    
    for i in range(len(bin_centers)):
        if bin_counts[i] > 0:
            bin_means[i] = bin_sums[i] / bin_counts[i]
    
    plt.figure(figsize=(10, 6))
    plt.bar(bin_centers, bin_means, width=1/n_bins, alpha=0.5, label="Model")
    plt.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
    plt.xlabel("Predicted Probability")
    plt.ylabel("True Probability")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def evaluate_calibration(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10
) -> Dict[str, float]:
    """Evaluate calibration metrics."""
    metrics = {}
    
    # Brier score
    metrics["brier_score"] = brier_score_loss(y_true, y_prob)
    
    # Log loss
    metrics["log_loss"] = log_loss(y_true, y_prob)
    
    # Calibration error
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins)
    metrics["calibration_error"] = np.mean(np.abs(prob_true - prob_pred))
    
    return metrics

def plot_calibration_histogram(
    y_prob: np.ndarray,
    n_bins: int = 20,
    title: str = "Probability Distribution"
) -> None:
    """Plot probability distribution histogram."""
    plt.figure(figsize=(10, 6))
    plt.hist(y_prob, bins=n_bins, alpha=0.5)
    plt.xlabel("Predicted Probability")
    plt.ylabel("Count")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compare_calibration_methods(
    y_true: np.ndarray,
    y_prob_original: np.ndarray,
    y_prob_platt: np.ndarray,
    y_prob_isotonic: np.ndarray,
    y_prob_temp: np.ndarray,
    title: str = "Calibration Methods Comparison"
) -> None:
    """Compare different calibration methods."""
    plt.figure(figsize=(12, 8))
    
    # Plot calibration curves
    plt.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
    
    for y_prob, label in [
        (y_prob_original, "Original"),
        (y_prob_platt, "Platt Scaling"),
        (y_prob_isotonic, "Isotonic"),
        (y_prob_temp, "Temperature Scaling")
    ]:
        prob_true, prob_pred = calibration_curve(y_true, y_prob)
        plt.plot(prob_pred, prob_true, "s-", label=label)
    
    plt.xlabel("Mean Predicted Probability")
    plt.ylabel("True Probability")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Print metrics for each method
    methods = {
        "Original": y_prob_original,
        "Platt Scaling": y_prob_platt,
        "Isotonic": y_prob_isotonic,
        "Temperature Scaling": y_prob_temp
    }
    
    print("\nCalibration Metrics:")
    print("-" * 50)
    for method, y_prob in methods.items():
        metrics = evaluate_calibration(y_true, y_prob)
        print(f"\n{method}:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}") 
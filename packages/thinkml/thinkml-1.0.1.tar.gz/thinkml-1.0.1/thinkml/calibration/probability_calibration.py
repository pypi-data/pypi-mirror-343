"""
Probability Calibration Module for ThinkML.

This module provides functions for calibrating probability estimates and
evaluating calibration performance.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import LabelBinarizer
from typing import Optional, Union, Dict, Any, Tuple, List
import pandas as pd

def calibrate_probabilities(
    estimator: BaseEstimator,
    X: np.ndarray,
    y: np.ndarray,
    method: str = 'sigmoid',
    cv: int = 5,
    n_jobs: Optional[int] = None
) -> Tuple[BaseEstimator, Dict[str, Any]]:
    """
    Calibrate probability estimates of a classifier.
    
    Parameters
    ----------
    estimator : estimator object
        The classifier whose probabilities need calibration.
    X : array-like of shape (n_samples, n_features)
        Training data.
    y : array-like of shape (n_samples,)
        Target values.
    method : str, default='sigmoid'
        The method to use for calibration.
        Supported values are ['sigmoid', 'isotonic'].
    cv : int, default=5
        Number of folds for cross-validation.
    n_jobs : int, optional
        Number of jobs to run in parallel.
        
    Returns
    -------
    tuple
        - Calibrated classifier
        - Dictionary containing calibration metrics
    """
    # Input validation
    X = np.asarray(X)
    y = np.asarray(y)
    
    # Create and fit calibrated classifier
    calibrated_clf = CalibratedClassifierCV(
        estimator,
        method=method,
        cv=cv,
        n_jobs=n_jobs
    )
    calibrated_clf.fit(X, y)
    
    # Get calibration metrics
    prob_true, prob_pred = calibration_curve(
        y,
        calibrated_clf.predict_proba(X)[:, 1],
        n_bins=10
    )
    
    # Calculate calibration error
    calibration_error = np.mean(np.abs(prob_true - prob_pred))
    
    # Calculate Brier score
    y_prob = calibrated_clf.predict_proba(X)
    lb = LabelBinarizer()
    y_true_bin = lb.fit_transform(y)
    if len(y_prob.shape) == 2:
        y_prob = y_prob[:, 1]
    brier_score = np.mean((y_true_bin - y_prob) ** 2)
    
    metrics = {
        'calibration_error': calibration_error,
        'brier_score': brier_score,
        'prob_true': prob_true,
        'prob_pred': prob_pred
    }
    
    return calibrated_clf, metrics

def plot_reliability_diagram(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
    title: str = 'Reliability Diagram',
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Plot reliability diagram (calibration curve).
    
    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True binary labels.
    y_prob : array-like of shape (n_samples,) or (n_samples, 2)
        Probability estimates. If shape is (n_samples, 2), the second column
        is used as the positive class probabilities.
    n_bins : int, default=10
        Number of bins for the calibration curve.
    title : str, default='Reliability Diagram'
        Title of the plot.
    figsize : tuple of int, default=(10, 6)
        Figure size.
        
    Returns
    -------
    matplotlib.figure.Figure
        The figure containing the reliability diagram.
    """
    # Convert inputs to numpy arrays
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    
    # If probabilities are given for both classes, take the positive class
    if len(y_prob.shape) == 2:
        y_prob = y_prob[:, 1]
    
    # Calculate calibration curve
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins)
    
    # Create figure
    fig = plt.figure(figsize=figsize)
    
    # Plot calibration curve
    plt.plot(prob_pred, prob_true, 's-', label='Calibration curve')
    
    # Plot diagonal (perfect calibration)
    plt.plot([0, 1], [0, 1], '--', color='gray', label='Perfect calibration')
    
    # Customize plot
    plt.xlabel('Mean predicted probability')
    plt.ylabel('Fraction of positives')
    plt.title(title)
    plt.legend(loc='lower right')
    plt.grid(True)
    
    # Add calibration error to the plot
    calibration_error = np.mean(np.abs(prob_true - prob_pred))
    plt.text(
        0.05, 0.95,
        f'Calibration error: {calibration_error:.3f}',
        transform=plt.gca().transAxes,
        verticalalignment='top'
    )
    
    return fig 
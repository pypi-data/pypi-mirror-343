"""
Evaluation Utilities Module for ThinkML.

This module provides functions for model evaluation and performance metrics.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score
)
from sklearn.model_selection import cross_val_score
from typing import Optional, Union, Dict, Any, List
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(
    model: Any,
    X: Union[np.ndarray, pd.DataFrame],
    y: Union[np.ndarray, pd.Series],
    X_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
    y_test: Optional[Union[np.ndarray, pd.Series]] = None,
    task: str = 'auto',
    cv: Optional[int] = 5,
    metrics: Optional[List[str]] = None,
    plot_results: bool = True
) -> Dict[str, Any]:
    """
    Evaluate a model's performance using various metrics and optionally plot results.
    
    Parameters
    ----------
    model : estimator object
        The trained model to evaluate.
    X : array-like of shape (n_samples, n_features)
        Training data.
    y : array-like of shape (n_samples,)
        Training target values.
    X_test : array-like of shape (n_samples, n_features), optional
        Test data. If not provided, cross-validation will be used.
    y_test : array-like of shape (n_samples,), optional
        Test target values.
    task : str, default='auto'
        The type of task. Options: ['auto', 'classification', 'regression']
        If 'auto', will try to determine from the model and data.
    cv : int, optional
        Number of cross-validation folds. Only used if X_test is None.
    metrics : list of str, optional
        List of metrics to compute. If None, uses default metrics for the task.
    plot_results : bool, default=True
        Whether to create and return visualization plots.
        
    Returns
    -------
    dict
        Dictionary containing evaluation metrics and optionally plots.
    """
    # Convert inputs to numpy arrays
    X = np.asarray(X)
    y = np.asarray(y)
    if X_test is not None:
        X_test = np.asarray(X_test)
        y_test = np.asarray(y_test)
    
    # Determine task type if auto
    if task == 'auto':
        if hasattr(model, '_estimator_type'):
            task = model._estimator_type
        else:
            # Try to infer from target values
            if np.issubdtype(y.dtype, np.number) and len(np.unique(y)) > 10:
                task = 'regression'
            else:
                task = 'classification'
    
    # Set default metrics based on task
    if metrics is None:
        if task == 'classification':
            metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        else:  # regression
            metrics = ['mse', 'mae', 'r2', 'explained_variance']
    
    results = {}
    
    # Evaluate on test set if provided
    if X_test is not None and y_test is not None:
        results['test_metrics'] = _compute_metrics(
            model, X_test, y_test, task, metrics
        )
        if plot_results:
            results['plots'] = _create_plots(
                model, X_test, y_test, task
            )
    
    # Perform cross-validation if no test set provided
    if cv is not None:
        cv_results = {}
        for metric in metrics:
            if task == 'classification':
                if metric == 'roc_auc':
                    scoring = 'roc_auc'
                else:
                    scoring = metric
            else:  # regression
                if metric == 'mse':
                    scoring = 'neg_mean_squared_error'
                elif metric == 'mae':
                    scoring = 'neg_mean_absolute_error'
                elif metric == 'r2':
                    scoring = 'r2'
                elif metric == 'explained_variance':
                    scoring = 'explained_variance'
                    
            scores = cross_val_score(
                model, X, y,
                cv=cv,
                scoring=scoring
            )
            
            # Convert negative scores back to positive
            if metric in ['mse', 'mae']:
                scores = -scores
                
            cv_results[metric] = {
                'mean': np.mean(scores),
                'std': np.std(scores),
                'scores': scores
            }
            
        results['cv_results'] = cv_results
        
        if plot_results:
            results['cv_plots'] = _create_cv_plots(cv_results)
    
    return results

def _compute_metrics(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    task: str,
    metrics: List[str]
) -> Dict[str, float]:
    """Compute specified metrics for the model."""
    results = {}
    
    # Get predictions
    y_pred = model.predict(X)
    if task == 'classification' and hasattr(model, 'predict_proba'):
        y_prob = model.predict_proba(X)
        if y_prob.shape[1] == 2:  # Binary classification
            y_prob = y_prob[:, 1]
    
    # Compute metrics
    for metric in metrics:
        if task == 'classification':
            if metric == 'accuracy':
                results[metric] = accuracy_score(y, y_pred)
            elif metric == 'precision':
                results[metric] = precision_score(y, y_pred, average='weighted')
            elif metric == 'recall':
                results[metric] = recall_score(y, y_pred, average='weighted')
            elif metric == 'f1':
                results[metric] = f1_score(y, y_pred, average='weighted')
            elif metric == 'roc_auc' and 'y_prob' in locals():
                if len(np.unique(y)) == 2:  # Binary classification
                    results[metric] = roc_auc_score(y, y_prob)
                else:  # Multi-class
                    results[metric] = roc_auc_score(y, y_prob, multi_class='ovr')
                    
            results['confusion_matrix'] = confusion_matrix(y, y_pred)
            results['classification_report'] = classification_report(y, y_pred)
            
        else:  # regression
            if metric == 'mse':
                results[metric] = mean_squared_error(y, y_pred)
            elif metric == 'mae':
                results[metric] = mean_absolute_error(y, y_pred)
            elif metric == 'r2':
                results[metric] = r2_score(y, y_pred)
            elif metric == 'explained_variance':
                results[metric] = explained_variance_score(y, y_pred)
    
    return results

def _create_plots(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    task: str
) -> Dict[str, plt.Figure]:
    """Create visualization plots based on the task type."""
    plots = {}
    
    if task == 'classification':
        # Confusion matrix heatmap
        cm = confusion_matrix(y, model.predict(X))
        fig = plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues'
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plots['confusion_matrix'] = fig
        
        # ROC curve for binary classification
        if len(np.unique(y)) == 2 and hasattr(model, 'predict_proba'):
            from sklearn.metrics import roc_curve
            y_prob = model.predict_proba(X)[:, 1]
            fpr, tpr, _ = roc_curve(y, y_prob)
            
            fig = plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr)
            plt.plot([0, 1], [0, 1], '--')
            plt.title('ROC Curve')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plots['roc_curve'] = fig
            
    else:  # regression
        # Predicted vs Actual values
        y_pred = model.predict(X)
        fig = plt.figure(figsize=(8, 6))
        plt.scatter(y, y_pred, alpha=0.5)
        plt.plot([y.min(), y.max()], [y.min(), y.max()], '--r')
        plt.title('Predicted vs Actual Values')
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plots['pred_vs_actual'] = fig
        
        # Residuals plot
        residuals = y - y_pred
        fig = plt.figure(figsize=(8, 6))
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.title('Residuals Plot')
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plots['residuals'] = fig
    
    return plots

def _create_cv_plots(
    cv_results: Dict[str, Dict[str, Union[float, np.ndarray]]]
) -> Dict[str, plt.Figure]:
    """Create plots for cross-validation results."""
    plots = {}
    
    # Distribution of CV scores
    fig = plt.figure(figsize=(10, 6))
    metrics = list(cv_results.keys())
    n_metrics = len(metrics)
    
    for i, metric in enumerate(metrics, 1):
        plt.subplot(1, n_metrics, i)
        scores = cv_results[metric]['scores']
        plt.hist(scores, bins='auto')
        plt.title(f'{metric.upper()} Distribution')
        plt.xlabel('Score')
        plt.ylabel('Count')
    
    plt.tight_layout()
    plots['cv_distributions'] = fig
    
    # Box plot of CV scores
    fig = plt.figure(figsize=(10, 6))
    scores_data = [cv_results[metric]['scores'] for metric in metrics]
    plt.boxplot(scores_data, labels=metrics)
    plt.title('Cross-validation Scores')
    plt.ylabel('Score')
    plt.xticks(rotation=45)
    plots['cv_boxplot'] = fig
    
    return plots 
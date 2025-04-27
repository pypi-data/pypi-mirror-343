"""
Cost-sensitive classification models for handling different misclassification costs.
"""

from typing import Optional, Union, Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array
from sklearn.linear_model import LogisticRegression

class CostSensitiveClassifier(BaseEstimator, ClassifierMixin):
    """
    A classifier that takes into account different misclassification costs.
    
    This classifier modifies the prediction threshold based on the cost matrix
    to minimize the total misclassification cost.
    
    Parameters
    ----------
    base_estimator : estimator object, default=None
        The base estimator to use for classification.
        If None, LogisticRegression is used.
    cost_matrix : array-like of shape (n_classes, n_classes), default=None
        The cost matrix where cost_matrix[i, j] is the cost of
        predicting class j when the true class is i.
        If None, uniform costs are assumed.
    """
    
    def __init__(
        self,
        base_estimator: Optional[BaseEstimator] = None,
        cost_matrix: Optional[np.ndarray] = None
    ):
        self.base_estimator = base_estimator or LogisticRegression()
        self.cost_matrix = cost_matrix
        self.classes_ = None
        self.n_classes_ = 0
        self.thresholds_ = None
    
    def _compute_thresholds(self) -> None:
        """Compute optimal decision thresholds based on the cost matrix."""
        if self.cost_matrix is None:
            self.thresholds_ = np.ones(self.n_classes_) / self.n_classes_
            return
            
        # Normalize cost matrix
        costs = self.cost_matrix / np.sum(self.cost_matrix)
        
        # Compute thresholds for each class
        self.thresholds_ = np.zeros(self.n_classes_)
        for i in range(self.n_classes_):
            # Threshold is ratio of cost of false positive to total cost
            false_positive_cost = np.sum(costs[:, i])
            total_cost = false_positive_cost + costs[i, i]
            self.thresholds_[i] = false_positive_cost / total_cost if total_cost > 0 else 0.5
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> 'CostSensitiveClassifier':
        """
        Fit the cost-sensitive classification model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
            
        Returns
        -------
        self : object
            Returns self.
        """
        X, y = check_X_y(X, y)
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        
        if self.cost_matrix is not None:
            if self.cost_matrix.shape != (self.n_classes_, self.n_classes_):
                raise ValueError(
                    f"Cost matrix shape {self.cost_matrix.shape} does not match "
                    f"number of classes {self.n_classes_}"
                )
        
        self._compute_thresholds()
        self.base_estimator.fit(X, y)
        return self
    
    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Predict class probabilities for X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.
            
        Returns
        -------
        P : array-like of shape (n_samples, n_classes)
            The class probabilities of the input samples.
        """
        X = check_array(X)
        return self.base_estimator.predict_proba(X)
    
    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Predict class labels for X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.
            
        Returns
        -------
        y : array-like of shape (n_samples,)
            The predicted class labels.
        """
        probs = self.predict_proba(X)
        
        # Apply cost-sensitive thresholds
        adjusted_probs = probs / self.thresholds_
        return self.classes_[np.argmax(adjusted_probs, axis=1)]
    
    def score(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> float:
        """
        Return the negative total cost on the given test data and labels.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.
        y : array-like of shape (n_samples,)
            True labels for X.
            
        Returns
        -------
        score : float
            Negative total cost of predictions.
        """
        y_pred = self.predict(X)
        
        if self.cost_matrix is None:
            from sklearn.metrics import accuracy_score
            return accuracy_score(y, y_pred)
        
        # Compute total cost
        total_cost = 0
        for i, true_class in enumerate(self.classes_):
            for j, pred_class in enumerate(self.classes_):
                mask = (y == true_class) & (y_pred == pred_class)
                total_cost += np.sum(mask) * self.cost_matrix[i, j]
        
        return -total_cost  # Return negative cost as score (higher is better) 
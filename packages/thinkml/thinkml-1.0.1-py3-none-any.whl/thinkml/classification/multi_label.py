"""
Multi-label classification models for handling multiple target labels.
"""

from typing import Optional, Union, Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array
from sklearn.linear_model import LogisticRegression

class MultiLabelClassifier(BaseEstimator, ClassifierMixin):
    """
    A classifier for handling multi-label classification problems.
    
    This classifier implements the binary relevance approach by training
    one binary classifier per label.
    
    Parameters
    ----------
    base_estimator : estimator object, default=None
        The base estimator to use for binary classification.
        If None, LogisticRegression is used.
    threshold : float, default=0.5
        The decision threshold for predicting labels.
    """
    
    def __init__(
        self,
        base_estimator: Optional[BaseEstimator] = None,
        threshold: float = 0.5
    ):
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")
            
        self.base_estimator = base_estimator or LogisticRegression()
        self.threshold = threshold
        self.classifiers_ = []
        self.n_labels_ = 0
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.DataFrame]) -> 'MultiLabelClassifier':
        """
        Fit the multi-label classification model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples, n_labels)
            Target values.
            
        Returns
        -------
        self : object
            Returns self.
        """
        X, y = check_X_y(X, y, multi_output=True)
        self.n_labels_ = y.shape[1]
        
        # Train one classifier per label
        for i in range(self.n_labels_):
            # Clone and fit the base estimator
            from sklearn.base import clone
            clf = clone(self.base_estimator)
            clf.fit(X, y[:, i])
            self.classifiers_.append(clf)
        
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
        P : array-like of shape (n_samples, n_labels)
            The class probabilities of the input samples.
        """
        X = check_array(X)
        
        # Get probabilities for each label
        probs = np.zeros((X.shape[0], self.n_labels_))
        for i, clf in enumerate(self.classifiers_):
            probs[:, i] = clf.predict_proba(X)[:, 1]
        
        return probs
    
    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Predict class labels for X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.
            
        Returns
        -------
        y : array-like of shape (n_samples, n_labels)
            The predicted class labels.
        """
        probs = self.predict_proba(X)
        return (probs >= self.threshold).astype(int)
    
    def score(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.DataFrame]) -> float:
        """
        Return the accuracy score on the given test data and labels.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.
        y : array-like of shape (n_samples, n_labels)
            True labels for X.
            
        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) wrt. y.
        """
        from sklearn.metrics import accuracy_score
        y_pred = self.predict(X)
        return np.mean([accuracy_score(y[:, i], y_pred[:, i]) for i in range(self.n_labels_)]) 
"""
Ordinal classification models for handling ordered categorical targets.
"""

from typing import Optional, Union, Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array
from sklearn.linear_model import LogisticRegression

class OrdinalClassifier(BaseEstimator, ClassifierMixin):
    """
    A classifier for handling ordinal categorical targets.
    
    This classifier implements the ordinal classification approach by training
    multiple binary classifiers to predict cumulative probabilities.
    
    Parameters
    ----------
    base_estimator : estimator object, default=None
        The base estimator to use for binary classification.
        If None, LogisticRegression is used.
    """
    
    def __init__(self, base_estimator: Optional[BaseEstimator] = None):
        self.base_estimator = base_estimator or LogisticRegression()
        self.classifiers_ = []
        self.classes_ = None
        self.n_classes_ = 0
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> 'OrdinalClassifier':
        """
        Fit the ordinal classification model.
        
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
        
        if self.n_classes_ < 2:
            raise ValueError("The number of classes must be greater than one")
        
        # Train binary classifiers for each threshold
        for i in range(self.n_classes_ - 1):
            # Create binary targets
            y_bin = (y > self.classes_[i]).astype(int)
            
            # Clone and fit the base estimator
            from sklearn.base import clone
            clf = clone(self.base_estimator)
            clf.fit(X, y_bin)
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
        P : array-like of shape (n_samples, n_classes)
            The class probabilities of the input samples.
        """
        X = check_array(X)
        
        # Get cumulative probabilities
        cum_probs = np.zeros((X.shape[0], self.n_classes_ - 1))
        for i, clf in enumerate(self.classifiers_):
            cum_probs[:, i] = clf.predict_proba(X)[:, 1]
        
        # Convert cumulative probabilities to class probabilities
        probs = np.zeros((X.shape[0], self.n_classes_))
        probs[:, 0] = 1 - cum_probs[:, 0]
        for i in range(1, self.n_classes_ - 1):
            probs[:, i] = cum_probs[:, i-1] - cum_probs[:, i]
        probs[:, -1] = cum_probs[:, -1]
        
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
        y : array-like of shape (n_samples,)
            The predicted class labels.
        """
        probs = self.predict_proba(X)
        return self.classes_[np.argmax(probs, axis=1)]
    
    def score(self, X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series]) -> float:
        """
        Return the mean accuracy on the given test data and labels.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.
        y : array-like of shape (n_samples,)
            True labels for X.
            
        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) wrt. y.
        """
        from sklearn.metrics import accuracy_score
        return accuracy_score(y, self.predict(X)) 
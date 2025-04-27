"""
Advanced Classification Module for ThinkML.

This module provides advanced classification functionality including:
- Logistic regression with regularization
- Support vector classification
- Neural network classification
- Ensemble classification methods
- Multi-label classification
- Cost-sensitive classification
"""

import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any, Optional
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_val_score
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelBinarizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import clone
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

class AdvancedClassification:
    """
    A class for advanced classification techniques.
    
    This class provides methods for:
    - Logistic regression with various regularization techniques
    - Support vector classification
    - Neural network classification
    - Ensemble classification methods
    - Multi-label classification
    - Cost-sensitive classification
    """
    
    def __init__(self):
        """Initialize the AdvancedClassification class."""
        self.models = {}
        self.best_model = None
        self.best_score = float('-inf')
        
    def create_logistic_model(self, 
                            regularization: str = 'l2',
                            C: float = 1.0,
                            class_weights: Optional[Dict[int, float]] = None) -> LogisticRegression:
        """
        Create a logistic regression model with optional regularization.
        
        Parameters
        ----------
        regularization : str, default='l2'
            Type of regularization ('l1', 'l2', 'elasticnet')
        C : float, default=1.0
            Inverse of regularization strength
        class_weights : dict, optional
            Dictionary mapping classes to weights
            
        Returns
        -------
        LogisticRegression
            The configured logistic regression model
        """
        return LogisticRegression(
            penalty=regularization,
            C=C,
            class_weight=class_weights,
            solver='liblinear' if regularization != 'elasticnet' else 'saga'
        )
    
    def create_svc_model(self, 
                        kernel: str = 'rbf',
                        C: float = 1.0,
                        class_weights: Optional[Dict[int, float]] = None) -> SVC:
        """
        Create a support vector classification model.
        
        Parameters
        ----------
        kernel : str, default='rbf'
            Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
        C : float, default=1.0
            Regularization parameter
        class_weights : dict, optional
            Dictionary mapping classes to weights
            
        Returns
        -------
        SVC
            The configured SVC model
        """
        return SVC(kernel=kernel, C=C, class_weight=class_weights, probability=True)
    
    def create_neural_network(self, 
                            input_size: int,
                            hidden_sizes: List[int] = [64, 32],
                            output_size: int = 1) -> nn.Module:
        """
        Create a neural network for classification.
        
        Parameters
        ----------
        input_size : int
            Number of input features
        hidden_sizes : List[int], default=[64, 32]
            List of hidden layer sizes
        output_size : int, default=1
            Number of output classes
            
        Returns
        -------
        nn.Module
            The configured neural network
        """
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_size),
                nn.Dropout(0.2)
            ])
            prev_size = hidden_size
            
        layers.append(nn.Linear(prev_size, output_size))
        if output_size == 1:
            layers.append(nn.Sigmoid())
        else:
            layers.append(nn.Softmax(dim=1))
            
        return nn.Sequential(*layers)
    
    def create_ensemble_model(self, 
                            method: str = 'random_forest',
                            n_estimators: int = 100,
                            class_weights: Optional[Dict[int, float]] = None,
                            **kwargs) -> BaseEstimator:
        """
        Create an ensemble classification model.
        
        Parameters
        ----------
        method : str, default='random_forest'
            Ensemble method ('random_forest' or 'gradient_boosting')
        n_estimators : int, default=100
            Number of estimators
        class_weights : dict, optional
            Dictionary mapping classes to weights
        **kwargs : dict
            Additional parameters for the ensemble model
            
        Returns
        -------
        BaseEstimator
            The configured ensemble model
        """
        if method == 'random_forest':
            return RandomForestClassifier(
                n_estimators=n_estimators,
                class_weight=class_weights,
                **kwargs
            )
        elif method == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=n_estimators,
                **kwargs
            )
        else:
            raise ValueError(f"Unknown ensemble method: {method}")
    
    def create_multilabel_model(self, 
                              base_model: BaseEstimator) -> OneVsRestClassifier:
        """
        Create a multi-label classification model.
        
        Parameters
        ----------
        base_model : BaseEstimator
            Base classifier to use for multi-label classification
            
        Returns
        -------
        OneVsRestClassifier
            The configured multi-label classifier
        """
        return OneVsRestClassifier(base_model)
    
    def evaluate_model(self, 
                      model: BaseEstimator,
                      X: Union[np.ndarray, pd.DataFrame],
                      y: Union[np.ndarray, pd.Series],
                      cv: int = 5) -> Dict[str, float]:
        """
        Evaluate a classification model using cross-validation.
        
        Parameters
        ----------
        model : BaseEstimator
            The model to evaluate
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        cv : int, default=5
            Number of cross-validation folds
            
        Returns
        -------
        dict
            Dictionary containing evaluation metrics
        """
        accuracy_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        precision_scores = cross_val_score(model, X, y, cv=cv, scoring='precision_weighted')
        recall_scores = cross_val_score(model, X, y, cv=cv, scoring='recall_weighted')
        f1_scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted')
        
        return {
            'accuracy': accuracy_scores.mean(),
            'precision': precision_scores.mean(),
            'recall': recall_scores.mean(),
            'f1': f1_scores.mean(),
            'cv_scores': {
                'accuracy': accuracy_scores,
                'precision': precision_scores,
                'recall': recall_scores,
                'f1': f1_scores
            }
        }
    
    def find_best_model(self, 
                       X: Union[np.ndarray, pd.DataFrame],
                       y: Union[np.ndarray, pd.Series],
                       models: Dict[str, BaseEstimator]) -> Dict[str, Any]:
        """
        Find the best performing model from a set of models.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        models : dict
            Dictionary of models to evaluate
            
        Returns
        -------
        dict
            Dictionary containing the best model and its performance
        """
        best_model_name = None
        best_score = float('-inf')
        results = {}
        
        for name, model in models.items():
            scores = self.evaluate_model(model, X, y)
            results[name] = scores
            
            if scores['f1'] > best_score:
                best_score = scores['f1']
                best_model_name = name
                self.best_model = model
                self.best_score = best_score
        
        return {
            'best_model_name': best_model_name,
            'best_model': self.best_model,
            'best_score': self.best_score,
            'all_results': results
        }

class MultiLabelClassifier(BaseEstimator, ClassifierMixin):
    """
    Multi-Label Classification estimator.
    
    This class implements multi-label classification, which handles tasks where each
    instance can be associated with multiple labels simultaneously.
    
    Parameters
    ----------
    base_estimator : estimator object, default=None
        The base estimator to use for multi-label classification.
        If None, uses RandomForestClassifier.
    threshold : float, default=0.5
        The threshold for converting probability estimates to binary predictions.
    n_jobs : int, default=None
        Number of jobs to run in parallel.
    """
    
    def __init__(
        self,
        base_estimator: Optional[BaseEstimator] = None,
        threshold: float = 0.5,
        n_jobs: Optional[int] = None
    ):
        self.base_estimator = base_estimator
        self.threshold = threshold
        self.n_jobs = n_jobs
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MultiLabelClassifier':
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
        # Input validation
        X, y = check_X_y(X, y, multi_output=True)
        
        # Initialize base estimator if not provided
        if self.base_estimator is None:
            self.base_estimator_ = RandomForestClassifier(n_jobs=self.n_jobs)
        else:
            self.base_estimator_ = self.base_estimator
            
        # Initialize and fit the multi-output classifier
        self.model_ = MultiOutputClassifier(
            self.base_estimator_,
            n_jobs=self.n_jobs
        )
        
        self.model_.fit(X, y)
        
        # Store training data characteristics
        self.n_features_in_ = X.shape[1]
        self.n_labels_ = y.shape[1]
        self.classes_ = [np.unique(y[:, i]) for i in range(y.shape[1])]
        
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict using the multi-label classification model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        y : array-like of shape (n_samples, n_labels)
            Returns predicted values.
        """
        check_is_fitted(self)
        X = check_array(X)
        
        return self.model_.predict(X)
        
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities for X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        p : array-like of shape (n_samples, n_labels, n_classes)
            Returns probabilities of the samples for each label.
        """
        check_is_fitted(self)
        X = check_array(X)
        
        return np.array([est.predict_proba(X) for est in self.model_.estimators_])
        
    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """Get parameters for this estimator."""
        return {
            'base_estimator': self.base_estimator,
            'threshold': self.threshold,
            'n_jobs': self.n_jobs
        }
        
    def set_params(self, **parameters: Any) -> 'MultiLabelClassifier':
        """Set the parameters of this estimator."""
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

class CostSensitiveClassifier(BaseEstimator, ClassifierMixin):
    """
    Cost-Sensitive Classification estimator.
    
    This class implements cost-sensitive classification, which takes into account
    different misclassification costs for different classes.
    
    Parameters
    ----------
    base_estimator : estimator object, default=None
        The base estimator to use for classification.
        If None, uses RandomForestClassifier.
    cost_matrix : array-like of shape (n_classes, n_classes), default=None
        The cost matrix where cost_matrix[i, j] is the cost of predicting
        class i when the true class is j.
    class_weight : dict or 'balanced', default=None
        Weights associated with classes.
    n_jobs : int, default=None
        Number of jobs to run in parallel.
    """
    
    def __init__(
        self,
        base_estimator: Optional[BaseEstimator] = None,
        cost_matrix: Optional[np.ndarray] = None,
        class_weight: Optional[Union[Dict, str]] = None,
        n_jobs: Optional[int] = None
    ):
        self.base_estimator = base_estimator
        self.cost_matrix = cost_matrix
        self.class_weight = class_weight
        self.n_jobs = n_jobs
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'CostSensitiveClassifier':
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
        # Input validation
        X, y = check_X_y(X, y)
        
        # Initialize base estimator if not provided
        if self.base_estimator is None:
            self.base_estimator_ = RandomForestClassifier(
                class_weight=self.class_weight,
                n_jobs=self.n_jobs
            )
        else:
            self.base_estimator_ = self.base_estimator
            
        # Store class information
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        
        # Initialize cost matrix if not provided
        if self.cost_matrix is None:
            self.cost_matrix_ = np.ones((self.n_classes_, self.n_classes_))
            np.fill_diagonal(self.cost_matrix_, 0)
        else:
            self.cost_matrix_ = np.asarray(self.cost_matrix)
            if self.cost_matrix_.shape != (self.n_classes_, self.n_classes_):
                raise ValueError("Cost matrix shape does not match number of classes")
                
        # Compute sample weights based on cost matrix
        sample_weights = np.zeros(len(y))
        for i, yi in enumerate(y):
            sample_weights[i] = np.sum(self.cost_matrix_[yi])
            
        # Normalize sample weights
        sample_weights = sample_weights / np.sum(sample_weights)
        
        # Fit the model with sample weights
        self.model_ = self.base_estimator_
        self.model_.fit(X, y, sample_weight=sample_weights)
        
        # Store training data characteristics
        self.n_features_in_ = X.shape[1]
        
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict using the cost-sensitive classification model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        y : array-like of shape (n_samples,)
            Returns predicted values.
        """
        check_is_fitted(self)
        X = check_array(X)
        
        if hasattr(self.model_, 'predict_proba'):
            # Use cost-sensitive prediction if probabilities are available
            proba = self.model_.predict_proba(X)
            return self.classes_[np.argmin(np.dot(proba, self.cost_matrix_), axis=1)]
        else:
            return self.model_.predict(X)
        
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities for X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.
            
        Returns
        -------
        p : array-like of shape (n_samples, n_classes)
            Returns probabilities of the samples for each class.
        """
        check_is_fitted(self)
        X = check_array(X)
        
        if hasattr(self.model_, 'predict_proba'):
            return self.model_.predict_proba(X)
        else:
            raise AttributeError("Base estimator does not have predict_proba method")
        
    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """Get parameters for this estimator."""
        return {
            'base_estimator': self.base_estimator,
            'cost_matrix': self.cost_matrix,
            'class_weight': self.class_weight,
            'n_jobs': self.n_jobs
        }
        
    def set_params(self, **parameters: Any) -> 'CostSensitiveClassifier':
        """Set the parameters of this estimator."""
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

class ImbalancedClassifier(BaseEstimator, ClassifierMixin):
    """Classifier for handling imbalanced datasets."""
    
    def __init__(self, base_estimator=None, sampling_strategy='auto', method='smote'):
        """
        Initialize imbalanced classifier.
        
        Parameters:
        -----------
        base_estimator : estimator object, default=None
            Base estimator to use for classification
        sampling_strategy : str or dict, default='auto'
            Sampling strategy to use
        method : str, default='smote'
            Resampling method to use: 'smote', 'adasyn', 'random'
        """
        self.base_estimator = base_estimator if base_estimator is not None else RandomForestClassifier()
        self.sampling_strategy = sampling_strategy
        self.method = method
        self.sampler = None
        
    def fit(self, X, y):
        """
        Fit the imbalanced classifier.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Create sampler based on method
        if self.method == 'smote':
            from imblearn.over_sampling import SMOTE
            self.sampler = SMOTE(sampling_strategy=self.sampling_strategy)
        elif self.method == 'adasyn':
            from imblearn.over_sampling import ADASYN
            self.sampler = ADASYN(sampling_strategy=self.sampling_strategy)
        elif self.method == 'random':
            from imblearn.over_sampling import RandomOverSampler
            self.sampler = RandomOverSampler(sampling_strategy=self.sampling_strategy)
            
        # Resample data
        X_resampled, y_resampled = self.sampler.fit_resample(X, y)
        
        # Fit base estimator on resampled data
        self.base_estimator.fit(X_resampled, y_resampled)
        
        return self
        
    def predict(self, X):
        """
        Predict using the imbalanced classifier.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Samples
        """
        X = np.asarray(X)
        return self.base_estimator.predict(X)
        
    def predict_proba(self, X):
        """
        Predict class probabilities for X.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Samples
        """
        X = np.asarray(X)
        return self.base_estimator.predict_proba(X)

class OrdinalClassifier(BaseEstimator, ClassifierMixin):
    """Ordinal classification model for handling ordered categorical targets."""
    
    def __init__(self, base_estimator=None):
        """
        Initialize ordinal classifier.
        
        Parameters:
        -----------
        base_estimator : estimator object, default=None
            Base estimator to use for classification
        """
        self.base_estimator = base_estimator if base_estimator is not None else RandomForestClassifier()
        self.classes_ = None
        self.classifiers = []
        
    def fit(self, X, y):
        """
        Fit the ordinal classifier.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Get unique classes and sort them
        self.classes_ = np.unique(y)
        self.classes_.sort()
        
        # Train binary classifiers for each threshold
        for i in range(len(self.classes_) - 1):
            # Create binary labels
            binary_y = (y > self.classes_[i]).astype(int)
            
            # Create and train classifier
            classifier = clone(self.base_estimator)
            classifier.fit(X, binary_y)
            self.classifiers.append(classifier)
        
        return self
        
    def predict(self, X):
        """
        Predict using the ordinal classifier.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Samples
        """
        X = np.asarray(X)
        
        # Get probabilities for each threshold
        probas = self.predict_proba(X)
        
        # Convert probabilities to class predictions
        predictions = np.zeros(len(X))
        for i in range(len(self.classes_)):
            mask = probas[:, i] >= 0.5
            predictions[mask] = self.classes_[i]
            
        return predictions
        
    def predict_proba(self, X):
        """
        Predict class probabilities for X.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Samples
        """
        X = np.asarray(X)
        
        # Get probabilities from each classifier
        probas = np.zeros((len(X), len(self.classes_)))
        for i, classifier in enumerate(self.classifiers):
            probas[:, i + 1:] += classifier.predict_proba(X)[:, 1].reshape(-1, 1)
            
        # Normalize probabilities
        probas /= (np.sum(probas, axis=1).reshape(-1, 1) + 1e-8)
        
        return probas 
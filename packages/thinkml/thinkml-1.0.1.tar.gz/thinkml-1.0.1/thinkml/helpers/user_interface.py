"""
User Interface Module for ThinkML

This module provides a simplified interface for using ThinkML functionality,
making it easier for users to access all features without remembering complex
class names or parameters.
"""

import inspect
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import KFold, StratifiedKFold

# Import ThinkML modules
from thinkml.validation.advanced_validation import (
    NestedCrossValidator,
    TimeSeriesValidator,
    StratifiedGroupValidator,
    BootstrapValidator
)
from thinkml.optimization.performance_optimizer import (
    EarlyStopping,
    GPUAccelerator,
    ParallelProcessor,
    optimize_batch_size,
    optimize_learning_rate
)
from thinkml.selection.advanced_selection import (
    BayesianOptimizer,
    MultiObjectiveOptimizer
)
from thinkml.feature_engineering.feature_creator import FeatureCreator
from thinkml.feature_engineering.feature_transformer import FeatureTransformer
from thinkml.interpretability.model_interpreter import ModelInterpreter
from thinkml.regression.advanced_regression import (
    QuantileRegressor,
    CensoredRegressor
)
from thinkml.classification.advanced_classification import (
    MultiLabelClassifier,
    OrdinalClassifier
)
from thinkml.calibration.probability_calibration import (
    calibrate_probabilities,
    plot_reliability_diagram
)


class ThinkML:
    """
    Simplified interface for ThinkML functionality.
    
    This class provides easy access to all ThinkML features through a simple,
    intuitive API. It handles the complexity of class instantiation and
    parameter management, allowing users to focus on their machine learning tasks.
    """
    
    def __init__(self):
        """Initialize the ThinkML interface."""
        # Initialize commonly used objects
        self._feature_creator = FeatureCreator()
        self._feature_transformer = FeatureTransformer()
        self._model_interpreter = ModelInterpreter()
    
    # ===== VALIDATION METHODS =====
    
    def nested_cv(self, 
                 estimator: BaseEstimator, 
                 X: Union[np.ndarray, pd.DataFrame], 
                 y: Union[np.ndarray, pd.Series],
                 param_grid: Dict[str, List[Any]] = None,
                 inner_cv: int = 5,
                 outer_cv: int = 5,
                 scoring: str = None,
                 n_jobs: int = -1) -> Dict[str, Any]:
        """
        Perform nested cross-validation with hyperparameter tuning.
        
        Parameters
        ----------
        estimator : BaseEstimator
            The estimator to use
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        param_grid : dict, optional
            Parameter grid for hyperparameter tuning
        inner_cv : int, default=5
            Number of inner CV folds
        outer_cv : int, default=5
            Number of outer CV folds
        scoring : str, optional
            Scoring metric
        n_jobs : int, default=-1
            Number of jobs to run in parallel
        
        Returns
        -------
        dict
            Dictionary containing cross-validation results
        """
        validator = NestedCrossValidator(
            estimator=estimator,
            param_grid=param_grid,
            inner_cv=inner_cv,
            outer_cv=outer_cv,
            scoring=scoring,
            n_jobs=n_jobs
        )
        return validator.fit_predict(X, y)
    
    def time_series_cv(self, 
                      estimator: BaseEstimator, 
                      X: Union[np.ndarray, pd.DataFrame], 
                      y: Union[np.ndarray, pd.Series],
                      n_splits: int = 5,
                      test_size: float = 0.2,
                      gap: int = 0,
                      scoring: str = None) -> Dict[str, Any]:
        """
        Perform time series cross-validation.
        
        Parameters
        ----------
        estimator : BaseEstimator
            The estimator to use
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        n_splits : int, default=5
            Number of splits
        test_size : float, default=0.2
            Size of test set
        gap : int, default=0
            Gap between train and test sets
        scoring : str, optional
            Scoring metric
        
        Returns
        -------
        dict
            Dictionary containing cross-validation results
        """
        validator = TimeSeriesValidator(
            n_splits=n_splits,
            test_size=test_size,
            gap=gap,
            scoring=scoring
        )
        return validator.fit_predict(X, y, estimator)
    
    def stratified_group_cv(self, 
                          estimator: BaseEstimator, 
                          X: Union[np.ndarray, pd.DataFrame], 
                          y: Union[np.ndarray, pd.Series],
                          groups: Union[np.ndarray, pd.Series],
                          n_splits: int = 5,
                          scoring: str = None) -> Dict[str, Any]:
        """
        Perform stratified group cross-validation.
        
        Parameters
        ----------
        estimator : BaseEstimator
            The estimator to use
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        groups : array-like of shape (n_samples,)
            Group labels
        n_splits : int, default=5
            Number of splits
        scoring : str, optional
            Scoring metric
        
        Returns
        -------
        dict
            Dictionary containing cross-validation results
        """
        validator = StratifiedGroupValidator(
            n_splits=n_splits,
            scoring=scoring
        )
        return validator.fit_predict(X, y, estimator, groups)
    
    def bootstrap_cv(self, 
                    estimator: BaseEstimator, 
                    X: Union[np.ndarray, pd.DataFrame], 
                    y: Union[np.ndarray, pd.Series],
                    n_iterations: int = 100,
                    sample_size: float = 0.8,
                    scoring: str = None) -> Dict[str, Any]:
        """
        Perform bootstrap cross-validation.
        
        Parameters
        ----------
        estimator : BaseEstimator
            The estimator to use
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        n_iterations : int, default=100
            Number of bootstrap iterations
        sample_size : float, default=0.8
            Size of bootstrap samples
        scoring : str, optional
            Scoring metric
        
        Returns
        -------
        dict
            Dictionary containing cross-validation results
        """
        validator = BootstrapValidator(
            n_iterations=n_iterations,
            sample_size=sample_size,
            scoring=scoring
        )
        return validator.fit_predict(X, y, estimator)
    
    # ===== OPTIMIZATION METHODS =====
    
    def early_stopping(self, 
                      patience: int = 10, 
                      min_delta: float = 0.001,
                      restore_best_weights: bool = True) -> EarlyStopping:
        """
        Create an early stopping callback.
        
        Parameters
        ----------
        patience : int, default=10
            Number of epochs to wait before stopping
        min_delta : float, default=0.001
            Minimum change to qualify as an improvement
        restore_best_weights : bool, default=True
            Whether to restore model weights from the epoch with the best value
        
        Returns
        -------
        EarlyStopping
            Early stopping callback
        """
        return EarlyStopping(
            patience=patience,
            min_delta=min_delta,
            restore_best_weights=restore_best_weights
        )
    
    def gpu_accelerator(self, 
                       model: Any = None,
                       device: str = None) -> GPUAccelerator:
        """
        Create a GPU accelerator.
        
        Parameters
        ----------
        model : Any, optional
            Model to accelerate
        device : str, optional
            Device to use ('cuda' or 'cpu')
        
        Returns
        -------
        GPUAccelerator
            GPU accelerator
        """
        return GPUAccelerator(model=model, device=device)
    
    def parallel_processor(self, 
                         n_jobs: int = -1,
                         backend: str = 'threading') -> ParallelProcessor:
        """
        Create a parallel processor.
        
        Parameters
        ----------
        n_jobs : int, default=-1
            Number of jobs to run in parallel
        backend : str, default='threading'
            Backend to use for parallel processing
        
        Returns
        -------
        ParallelProcessor
            Parallel processor
        """
        return ParallelProcessor(n_jobs=n_jobs, backend=backend)
    
    def find_optimal_batch_size(self, 
                              model: Any,
                              X: Union[np.ndarray, pd.DataFrame],
                              y: Union[np.ndarray, pd.Series],
                              batch_sizes: List[int] = None,
                              max_batch_size: int = 1024) -> int:
        """
        Find the optimal batch size for a model.
        
        Parameters
        ----------
        model : Any
            Model to optimize
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        batch_sizes : list, optional
            Batch sizes to try
        max_batch_size : int, default=1024
            Maximum batch size to try
        
        Returns
        -------
        int
            Optimal batch size
        """
        return optimize_batch_size(
            model=model,
            X=X,
            y=y,
            batch_sizes=batch_sizes,
            max_batch_size=max_batch_size
        )
    
    def find_optimal_learning_rate(self, 
                                 model: Any,
                                 X: Union[np.ndarray, pd.DataFrame],
                                 y: Union[np.ndarray, pd.Series],
                                 batch_size: int = 32,
                                 num_iterations: int = 100) -> float:
        """
        Find the optimal learning rate for a model.
        
        Parameters
        ----------
        model : Any
            Model to optimize
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        batch_size : int, default=32
            Batch size to use
        num_iterations : int, default=100
            Number of iterations to run
        
        Returns
        -------
        float
            Optimal learning rate
        """
        return optimize_learning_rate(
            model=model,
            X=X,
            y=y,
            batch_size=batch_size,
            num_iterations=num_iterations
        )
    
    # ===== SELECTION METHODS =====
    
    def bayesian_optimization(self, 
                            estimator: BaseEstimator,
                            X: Union[np.ndarray, pd.DataFrame],
                            y: Union[np.ndarray, pd.Series],
                            param_space: Dict[str, Tuple[Any, Any]],
                            n_iter: int = 50,
                            cv: int = 5,
                            scoring: str = None,
                            n_jobs: int = -1) -> Dict[str, Any]:
        """
        Perform Bayesian optimization for hyperparameter tuning.
        
        Parameters
        ----------
        estimator : BaseEstimator
            The estimator to use
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        param_space : dict
            Parameter space for optimization
        n_iter : int, default=50
            Number of iterations
        cv : int, default=5
            Number of cross-validation folds
        scoring : str, optional
            Scoring metric
        n_jobs : int, default=-1
            Number of jobs to run in parallel
        
        Returns
        -------
        dict
            Dictionary containing optimization results
        """
        optimizer = BayesianOptimizer(
            estimator=estimator,
            param_space=param_space,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs
        )
        return optimizer.optimize(X, y)
    
    def multi_objective_optimization(self, 
                                   estimator: BaseEstimator,
                                   X: Union[np.ndarray, pd.DataFrame],
                                   y: Union[np.ndarray, pd.Series],
                                   param_space: Dict[str, Tuple[Any, Any]],
                                   objectives: List[str],
                                   n_trials: int = 100,
                                   cv: int = 5) -> Dict[str, Any]:
        """
        Perform multi-objective optimization for hyperparameter tuning.
        
        Parameters
        ----------
        estimator : BaseEstimator
            The estimator to use
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        param_space : dict
            Parameter space for optimization
        objectives : list
            List of objective functions to optimize
        n_trials : int, default=100
            Number of trials
        cv : int, default=5
            Number of cross-validation folds
        
        Returns
        -------
        dict
            Dictionary containing optimization results
        """
        optimizer = MultiObjectiveOptimizer(
            estimator=estimator,
            param_space=param_space,
            objectives=objectives,
            n_trials=n_trials,
            cv=cv
        )
        return optimizer.optimize(X, y)
    
    # ===== FEATURE ENGINEERING METHODS =====
    
    def create_features(self, 
                       X: Union[np.ndarray, pd.DataFrame],
                       feature_types: List[str] = None) -> pd.DataFrame:
        """
        Create new features from existing data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data
        feature_types : list, optional
            Types of features to create
        
        Returns
        -------
        pd.DataFrame
            DataFrame with new features
        """
        return self._feature_creator.create_features(X, feature_types)
    
    def create_polynomial_features(self, 
                                 X: Union[np.ndarray, pd.DataFrame],
                                 degree: int = 2,
                                 interaction_only: bool = False) -> pd.DataFrame:
        """
        Create polynomial features.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data
        degree : int, default=2
            Degree of polynomial
        interaction_only : bool, default=False
            Whether to include only interaction features
        
        Returns
        -------
        pd.DataFrame
            DataFrame with polynomial features
        """
        return self._feature_creator.create_polynomial_features(
            X, degree, interaction_only
        )
    
    def create_interaction_features(self, 
                                  X: Union[np.ndarray, pd.DataFrame],
                                  columns: List[str] = None) -> pd.DataFrame:
        """
        Create interaction features.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data
        columns : list, optional
            Columns to create interactions for
        
        Returns
        -------
        pd.DataFrame
            DataFrame with interaction features
        """
        return self._feature_creator.create_interaction_features(X, columns)
    
    def transform_features(self, 
                         X: Union[np.ndarray, pd.DataFrame],
                         transformations: List[str] = None) -> pd.DataFrame:
        """
        Transform features.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data
        transformations : list, optional
            Transformations to apply
        
        Returns
        -------
        pd.DataFrame
            DataFrame with transformed features
        """
        return self._feature_transformer.transform_features(X, transformations)
    
    def scale_features(self, 
                      X: Union[np.ndarray, pd.DataFrame],
                      method: str = 'standard') -> pd.DataFrame:
        """
        Scale features.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data
        method : str, default='standard'
            Scaling method to use
        
        Returns
        -------
        pd.DataFrame
            DataFrame with scaled features
        """
        return self._feature_transformer.scale_features(X, method)
    
    def encode_categorical_features(self, 
                                  X: Union[np.ndarray, pd.DataFrame],
                                  columns: List[str] = None,
                                  method: str = 'onehot') -> pd.DataFrame:
        """
        Encode categorical features.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data
        columns : list, optional
            Columns to encode
        method : str, default='onehot'
            Encoding method to use
        
        Returns
        -------
        pd.DataFrame
            DataFrame with encoded features
        """
        return self._feature_transformer.encode_categorical_features(
            X, columns, method
        )
    
    # ===== INTERPRETABILITY METHODS =====
    
    def explain_model(self, 
                     model: BaseEstimator,
                     X: Union[np.ndarray, pd.DataFrame],
                     method: str = 'shap') -> Dict[str, Any]:
        """
        Explain model predictions.
        
        Parameters
        ----------
        model : BaseEstimator
            Trained model
        X : array-like of shape (n_samples, n_features)
            Input data
        method : str, default='shap'
            Explanation method to use
        
        Returns
        -------
        dict
            Dictionary containing explanation results
        """
        return self._model_interpreter.explain_model(model, X, method)
    
    def plot_feature_importance(self, 
                              model: BaseEstimator,
                              X: Union[np.ndarray, pd.DataFrame],
                              top_n: int = 10) -> None:
        """
        Plot feature importance.
        
        Parameters
        ----------
        model : BaseEstimator
            Trained model
        X : array-like of shape (n_samples, n_features)
            Input data
        top_n : int, default=10
            Number of top features to show
        """
        self._model_interpreter.plot_feature_importance(model, X, top_n)
    
    def plot_shap_summary(self, 
                         model: BaseEstimator,
                         X: Union[np.ndarray, pd.DataFrame],
                         top_n: int = 10) -> None:
        """
        Plot SHAP summary.
        
        Parameters
        ----------
        model : BaseEstimator
            Trained model
        X : array-like of shape (n_samples, n_features)
            Input data
        top_n : int, default=10
            Number of top features to show
        """
        self._model_interpreter.plot_shap_summary(model, X, top_n)
    
    def plot_lime_explanation(self, 
                            model: BaseEstimator,
                            X: Union[np.ndarray, pd.DataFrame],
                            instance_idx: int = 0,
                            num_features: int = 10) -> None:
        """
        Plot LIME explanation.
        
        Parameters
        ----------
        model : BaseEstimator
            Trained model
        X : array-like of shape (n_samples, n_features)
            Input data
        instance_idx : int, default=0
            Index of instance to explain
        num_features : int, default=10
            Number of features to show
        """
        self._model_interpreter.plot_lime_explanation(
            model, X, instance_idx, num_features
        )
    
    # ===== REGRESSION METHODS =====
    
    def quantile_regression(self, 
                          X: Union[np.ndarray, pd.DataFrame],
                          y: Union[np.ndarray, pd.Series],
                          quantile: float = 0.5,
                          alpha: float = 0.0) -> QuantileRegressor:
        """
        Create a quantile regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        quantile : float, default=0.5
            Quantile to estimate
        alpha : float, default=0.0
            Regularization parameter
        
        Returns
        -------
        QuantileRegressor
            Fitted quantile regression model
        """
        model = QuantileRegressor(quantile=quantile, alpha=alpha)
        model.fit(X, y)
        return model
    
    def censored_regression(self, 
                          X: Union[np.ndarray, pd.DataFrame],
                          y: Union[np.ndarray, pd.Series],
                          censoring: Union[np.ndarray, pd.Series]) -> CensoredRegressor:
        """
        Create a censored regression model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        censoring : array-like of shape (n_samples,)
            Censoring indicators
        
        Returns
        -------
        CensoredRegressor
            Fitted censored regression model
        """
        model = CensoredRegressor()
        model.fit(X, y, censoring)
        return model
    
    # ===== CLASSIFICATION METHODS =====
    
    def multi_label_classification(self, 
                                 X: Union[np.ndarray, pd.DataFrame],
                                 y: Union[np.ndarray, pd.DataFrame],
                                 base_estimator: BaseEstimator = None) -> MultiLabelClassifier:
        """
        Create a multi-label classification model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples, n_labels)
            Target values
        base_estimator : BaseEstimator, optional
            Base estimator to use
        
        Returns
        -------
        MultiLabelClassifier
            Fitted multi-label classification model
        """
        model = MultiLabelClassifier(base_estimator=base_estimator)
        model.fit(X, y)
        return model
    
    def ordinal_classification(self, 
                             X: Union[np.ndarray, pd.DataFrame],
                             y: Union[np.ndarray, pd.Series],
                             base_estimator: BaseEstimator = None) -> OrdinalClassifier:
        """
        Create an ordinal classification model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        base_estimator : BaseEstimator, optional
            Base estimator to use
        
        Returns
        -------
        OrdinalClassifier
            Fitted ordinal classification model
        """
        model = OrdinalClassifier(base_estimator=base_estimator)
        model.fit(X, y)
        return model
    
    # ===== CALIBRATION METHODS =====
    
    def calibrate_probabilities(self, 
                              model: BaseEstimator,
                              X: Union[np.ndarray, pd.DataFrame],
                              y: Union[np.ndarray, pd.Series],
                              method: str = 'platt') -> BaseEstimator:
        """
        Calibrate probability estimates.
        
        Parameters
        ----------
        model : BaseEstimator
            Trained model
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        method : str, default='platt'
            Calibration method to use
        
        Returns
        -------
        BaseEstimator
            Calibrated model
        """
        if method == 'platt':
            calibrator = PlattScaler()
        elif method == 'isotonic':
            calibrator = IsotonicRegressor()
        else:
            raise ValueError(f"Unknown calibration method: {method}")
        
        return calibrator.fit_transform(model, X, y)
    
    # ===== UTILITY METHODS =====
    
    def get_available_methods(self) -> Dict[str, List[str]]:
        """
        Get a list of available methods.
        
        Returns
        -------
        dict
            Dictionary mapping categories to lists of method names
        """
        methods = {}
        for name, method in inspect.getmembers(self):
            if inspect.ismethod(method) and not name.startswith('_'):
                category = name.split('_')[0]
                if category not in methods:
                    methods[category] = []
                methods[category].append(name)
        return methods
    
    def get_method_help(self, method_name: str) -> str:
        """
        Get help information for a method.
        
        Parameters
        ----------
        method_name : str
            Name of the method
        
        Returns
        -------
        str
            Help information
        """
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return inspect.getdoc(method)
        else:
            return f"Method '{method_name}' not found."


# Create a global instance for easy access
thinkml = ThinkML() 
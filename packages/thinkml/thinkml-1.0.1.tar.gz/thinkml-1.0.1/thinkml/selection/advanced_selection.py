"""
Advanced model selection utilities for ThinkML.
Implements Bayesian optimization, multi-objective optimization, and model stacking.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_score
from skopt import BayesSearchCV
from skopt.space import Real, Integer, Categorical
import optuna
from sklearn.ensemble import StackingClassifier, StackingRegressor
import matplotlib.pyplot as plt
import seaborn as sns

class BayesianOptimizer:
    """Bayesian optimization for hyperparameter tuning."""
    
    def __init__(
        self,
        estimator: BaseEstimator,
        param_space: Dict[str, Any],
        n_iter: int = 50,
        cv: int = 5,
        scoring: str = "neg_mean_squared_error",
        n_jobs: int = -1
    ):
        self.estimator = estimator
        self.param_space = self._convert_param_space(param_space)
        self.n_iter = n_iter
        self.cv = cv
        self.scoring = scoring
        self.n_jobs = n_jobs
        self.optimizer = None
        
    def _convert_param_space(self, param_space: Dict[str, Any]) -> Dict[str, Any]:
        """Convert dictionary parameter space to skopt space objects."""
        converted_space = {}
        for param, space in param_space.items():
            if isinstance(space, tuple):
                if len(space) == 2:
                    converted_space[param] = Real(space[0], space[1])
                elif len(space) == 3:
                    converted_space[param] = Real(space[0], space[1], prior=space[2])
            elif isinstance(space, list):
                converted_space[param] = Categorical(space)
            elif isinstance(space, int):
                converted_space[param] = Integer(space)
        return converted_space
    
    def optimize(self, X: pd.DataFrame, y: pd.Series) -> Tuple[Dict[str, Any], float]:
        """Perform Bayesian optimization."""
        self.optimizer = BayesSearchCV(
            estimator=self.estimator,
            search_spaces=self.param_space,
            n_iter=self.n_iter,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=self.n_jobs
        )
        self.optimizer.fit(X, y)
        return self.optimizer.best_params_, self.optimizer.best_score_
    
    def plot_optimization_history(self):
        """Plot the optimization history."""
        if self.optimizer is None:
            raise ValueError("Optimizer has not been run yet.")
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.optimizer.cv_results_['mean_test_score'])
        plt.title('Optimization History')
        plt.xlabel('Iteration')
        plt.ylabel('Mean CV Score')
        plt.grid(True)
        plt.show()

class MultiObjectiveOptimizer:
    """Multi-objective optimization for model selection."""
    
    def __init__(
        self,
        objectives: List[callable],
        param_space: Dict[str, Any],
        n_trials: int = 100
    ):
        self.objectives = objectives
        self.param_space = param_space
        self.n_trials = n_trials
        self.study = None
        
    def optimize(self) -> List[Dict[str, Any]]:
        """Perform multi-objective optimization using Optuna."""
        def objective(trial):
            params = {}
            for param, space in self.param_space.items():
                if isinstance(space, tuple):
                    params[param] = trial.suggest_float(param, space[0], space[1])
                elif isinstance(space, list):
                    params[param] = trial.suggest_categorical(param, space)
                elif isinstance(space, int):
                    params[param] = trial.suggest_int(param, 0, space)
            
            return [obj(params) for obj in self.objectives]
        
        self.study = optuna.create_study(directions=["minimize"] * len(self.objectives))
        self.study.optimize(objective, n_trials=self.n_trials)
        return self.study.best_trials

class ModelStacker:
    """Model stacking and blending implementation."""
    
    def __init__(
        self,
        base_models: List[BaseEstimator],
        meta_model: BaseEstimator,
        cv: int = 5,
        n_jobs: int = -1
    ):
        self.base_models = base_models
        self.meta_model = meta_model
        self.cv = cv
        self.n_jobs = n_jobs
        self.stacker = None
        
    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        task: str = "classification"
    ) -> "ModelStacker":
        """Fit the stacked model."""
        if task == "classification":
            self.stacker = StackingClassifier(
                estimators=[(f"model_{i}", model) for i, model in enumerate(self.base_models)],
                final_estimator=self.meta_model,
                cv=self.cv,
                n_jobs=self.n_jobs
            )
        else:
            self.stacker = StackingRegressor(
                estimators=[(f"model_{i}", model) for i, model in enumerate(self.base_models)],
                final_estimator=self.meta_model,
                cv=self.cv,
                n_jobs=self.n_jobs
            )
        
        self.stacker.fit(X, y)
        return this
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using the stacked model."""
        if self.stacker is None:
            raise ValueError("Model has not been fitted yet.")
        return this.stacker.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Make probability predictions using the stacked model."""
        if self.stacker is None:
            raise ValueError("Model has not been fitted yet.")
        if not hasattr(self.stacker, "predict_proba"):
            raise ValueError("Model does not support probability predictions.")
        return this.stacker.predict_proba(X)

def plot_learning_curves(
    estimator: BaseEstimator,
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5,
    n_jobs: int = -1,
    train_sizes: Optional[List[float]] = None
) -> None:
    """Plot learning curves for model evaluation."""
    from sklearn.model_selection import learning_curve
    
    if train_sizes is None:
        train_sizes = np.linspace(0.1, 1.0, 10)
    
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs,
        train_sizes=train_sizes, return_times=False
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, label='Training score')
    plt.fill_between(
        train_sizes, train_mean - train_std, train_mean + train_std,
        alpha=0.1
    )
    plt.plot(train_sizes, val_mean, label='Cross-validation score')
    plt.fill_between(
        train_sizes, val_mean - val_std, val_mean + val_std,
        alpha=0.1
    )
    plt.title('Learning Curves')
    plt.xlabel('Training Examples')
    plt.ylabel('Score')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

def plot_validation_curves(
    estimator: BaseEstimator,
    X: pd.DataFrame,
    y: pd.Series,
    param_name: str,
    param_range: List[Any],
    cv: int = 5,
    scoring: str = "neg_mean_squared_error"
) -> None:
    """Plot validation curves for hyperparameter tuning."""
    from sklearn.model_selection import validation_curve
    
    train_scores, val_scores = validation_curve(
        estimator, X, y, param_name=param_name,
        param_range=param_range, cv=cv, scoring=scoring
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(param_range, train_mean, label='Training score')
    plt.fill_between(
        param_range, train_mean - train_std, train_mean + train_std,
        alpha=0.1
    )
    plt.plot(param_range, val_mean, label='Cross-validation score')
    plt.fill_between(
        param_range, val_mean - val_std, val_mean + val_std,
        alpha=0.1
    )
    plt.title('Validation Curves')
    plt.xlabel(param_name)
    plt.ylabel('Score')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show() 
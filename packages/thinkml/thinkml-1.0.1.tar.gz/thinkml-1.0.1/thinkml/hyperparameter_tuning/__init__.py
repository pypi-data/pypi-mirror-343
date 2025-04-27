"""
Hyperparameter tuning module for ThinkML.
Implements various hyperparameter optimization strategies including grid search,
random search, Bayesian optimization, population-based methods, and successive halving.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import ParameterGrid, ParameterSampler
from sklearn.metrics import make_scorer
import optuna
from optuna.samplers import TPESampler, RandomSampler, CmaEsSampler
from optuna.pruners import MedianPruner, SuccessiveHalvingPruner
from optuna.visualization import plot_optimization_history, plot_param_importances
import joblib
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import uniform, randint, norm
import warnings

class GridSearchOptimizer:
    """Grid search hyperparameter optimization."""
    
    def __init__(
        self,
        estimator: BaseEstimator,
        param_grid: Dict[str, List[Any]],
        scoring: Union[str, Callable] = "neg_mean_squared_error",
        cv: int = 5,
        n_jobs: int = -1,
        verbose: int = 0
    ):
        self.estimator = estimator
        self.param_grid = param_grid
        self.scoring = scoring
        self.cv = cv
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.best_params_ = None
        self.best_score_ = None
        self.cv_results_ = None
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "GridSearchOptimizer":
        """Perform grid search to find the best hyperparameters."""
        param_grid = ParameterGrid(self.param_grid)
        n_combinations = len(param_grid)
        
        if self.verbose > 0:
            print(f"Grid search with {n_combinations} parameter combinations")
        
        cv_results = {
            "params": [],
            "mean_test_score": [],
            "std_test_score": [],
            "mean_train_score": [],
            "std_train_score": [],
            "mean_fit_time": [],
            "std_fit_time": []
        }
        
        best_score = float("-inf")
        best_params = None
        
        for params in tqdm(param_grid, disable=self.verbose == 0):
            estimator = self.estimator.set_params(**params)
            
            # Perform cross-validation
            scores = cross_validate(
                estimator, X, y,
                cv=self.cv,
                scoring=self.scoring,
                return_train_score=True,
                return_estimator=True,
                n_jobs=self.n_jobs
            )
            
            # Store results
            cv_results["params"].append(params)
            cv_results["mean_test_score"].append(scores["test_score"].mean())
            cv_results["std_test_score"].append(scores["test_score"].std())
            cv_results["mean_train_score"].append(scores["train_score"].mean())
            cv_results["std_train_score"].append(scores["train_score"].std())
            cv_results["mean_fit_time"].append(scores["fit_time"].mean())
            cv_results["std_fit_time"].append(scores["fit_time"].std())
            
            # Update best parameters if necessary
            if scores["test_score"].mean() > best_score:
                best_score = scores["test_score"].mean()
                best_params = params
        
        self.best_params_ = best_params
        self.best_score_ = best_score
        self.cv_results_ = cv_results
        
        return self
    
    def get_results(self) -> Dict[str, Any]:
        """Get the results of the grid search."""
        if self.best_params_ is None:
            raise ValueError("Grid search has not been performed yet.")
        
        return {
            "best_params": self.best_params_,
            "best_score": self.best_score_,
            "cv_results": self.cv_results_
        }
    
    def plot_results(self, param_name: Optional[str] = None) -> None:
        """Plot the results of the grid search."""
        if self.cv_results_ is None:
            raise ValueError("Grid search has not been performed yet.")
        
        if param_name is not None and param_name not in self.param_grid:
            raise ValueError(f"Parameter {param_name} not found in param_grid.")
        
        if param_name is not None:
            # Plot results for a single parameter
            param_values = [params[param_name] for params in self.cv_results_["params"]]
            scores = self.cv_results_["mean_test_score"]
            errors = self.cv_results_["std_test_score"]
            
            plt.figure(figsize=(10, 6))
            plt.errorbar(param_values, scores, yerr=errors, fmt='o-')
            plt.xlabel(param_name)
            plt.ylabel("Mean CV Score")
            plt.title(f"Grid Search Results for {param_name}")
            plt.grid(True)
            plt.show()
        else:
            # Plot results for all parameters
            n_params = len(self.param_grid)
            fig, axes = plt.subplots(1, n_params, figsize=(5*n_params, 5))
            
            if n_params == 1:
                axes = [axes]
            
            for i, (param_name, param_values) in enumerate(self.param_grid.items()):
                param_scores = {}
                param_errors = {}
                
                for j, params in enumerate(self.cv_results_["params"]):
                    if params[param_name] not in param_scores:
                        param_scores[params[param_name]] = []
                        param_errors[params[param_name]] = []
                    
                    param_scores[params[param_name]].append(self.cv_results_["mean_test_score"][j])
                    param_errors[params[param_name]].append(self.cv_results_["std_test_score"][j])
                
                x = list(param_scores.keys())
                y = [np.mean(scores) for scores in param_scores.values()]
                yerr = [np.mean(errors) for errors in param_errors.values()]
                
                axes[i].errorbar(x, y, yerr=yerr, fmt='o-')
                axes[i].set_xlabel(param_name)
                axes[i].set_ylabel("Mean CV Score")
                axes[i].set_title(f"Results for {param_name}")
                axes[i].grid(True)
            
            plt.tight_layout()
            plt.show()

class RandomSearchOptimizer:
    """Random search hyperparameter optimization."""
    
    def __init__(
        self,
        estimator: BaseEstimator,
        param_distributions: Dict[str, Any],
        n_iter: int = 100,
        scoring: Union[str, Callable] = "neg_mean_squared_error",
        cv: int = 5,
        n_jobs: int = -1,
        verbose: int = 0,
        random_state: Optional[int] = None
    ):
        self.estimator = estimator
        self.param_distributions = param_distributions
        self.n_iter = n_iter
        self.scoring = scoring
        self.cv = cv
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.random_state = random_state
        self.best_params_ = None
        self.best_score_ = None
        self.cv_results_ = None
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "RandomSearchOptimizer":
        """Perform random search to find the best hyperparameters."""
        param_sampler = ParameterSampler(
            self.param_distributions,
            n_iter=self.n_iter,
            random_state=self.random_state
        )
        
        if self.verbose > 0:
            print(f"Random search with {self.n_iter} iterations")
        
        cv_results = {
            "params": [],
            "mean_test_score": [],
            "std_test_score": [],
            "mean_train_score": [],
            "std_train_score": [],
            "mean_fit_time": [],
            "std_fit_time": []
        }
        
        best_score = float("-inf")
        best_params = None
        
        for params in tqdm(param_sampler, disable=self.verbose == 0):
            estimator = self.estimator.set_params(**params)
            
            # Perform cross-validation
            scores = cross_validate(
                estimator, X, y,
                cv=self.cv,
                scoring=self.scoring,
                return_train_score=True,
                return_estimator=True,
                n_jobs=self.n_jobs
            )
            
            # Store results
            cv_results["params"].append(params)
            cv_results["mean_test_score"].append(scores["test_score"].mean())
            cv_results["std_test_score"].append(scores["test_score"].std())
            cv_results["mean_train_score"].append(scores["train_score"].mean())
            cv_results["std_train_score"].append(scores["train_score"].std())
            cv_results["mean_fit_time"].append(scores["fit_time"].mean())
            cv_results["std_fit_time"].append(scores["fit_time"].std())
            
            # Update best parameters if necessary
            if scores["test_score"].mean() > best_score:
                best_score = scores["test_score"].mean()
                best_params = params
        
        self.best_params_ = best_params
        self.best_score_ = best_score
        self.cv_results_ = cv_results
        
        return self
    
    def get_results(self) -> Dict[str, Any]:
        """Get the results of the random search."""
        if self.best_params_ is None:
            raise ValueError("Random search has not been performed yet.")
        
        return {
            "best_params": self.best_params_,
            "best_score": self.best_score_,
            "cv_results": self.cv_results_
        }
    
    def plot_results(self, param_name: Optional[str] = None) -> None:
        """Plot the results of the random search."""
        if self.cv_results_ is None:
            raise ValueError("Random search has not been performed yet.")
        
        if param_name is not None and param_name not in self.param_distributions:
            raise ValueError(f"Parameter {param_name} not found in param_distributions.")
        
        if param_name is not None:
            # Plot results for a single parameter
            param_values = [params[param_name] for params in self.cv_results_["params"]]
            scores = self.cv_results_["mean_test_score"]
            
            plt.figure(figsize=(10, 6))
            plt.scatter(param_values, scores, alpha=0.5)
            plt.xlabel(param_name)
            plt.ylabel("Mean CV Score")
            plt.title(f"Random Search Results for {param_name}")
            plt.grid(True)
            plt.show()
        else:
            # Plot results for all parameters
            n_params = len(self.param_distributions)
            fig, axes = plt.subplots(1, n_params, figsize=(5*n_params, 5))
            
            if n_params == 1:
                axes = [axes]
            
            for i, (param_name, _) in enumerate(self.param_distributions.items()):
                param_values = [params[param_name] for params in self.cv_results_["params"]]
                scores = self.cv_results_["mean_test_score"]
                
                axes[i].scatter(param_values, scores, alpha=0.5)
                axes[i].set_xlabel(param_name)
                axes[i].set_ylabel("Mean CV Score")
                axes[i].set_title(f"Results for {param_name}")
                axes[i].grid(True)
            
            plt.tight_layout()
            plt.show()

class BayesianOptimizer:
    """Bayesian optimization for hyperparameter tuning."""
    
    def __init__(
        self,
        estimator: BaseEstimator,
        param_space: Dict[str, Any],
        n_iter: int = 50,
        scoring: Union[str, Callable] = "neg_mean_squared_error",
        cv: int = 5,
        n_jobs: int = -1,
        verbose: int = 0,
        random_state: Optional[int] = None,
        sampler: str = "tpe"
    ):
        self.estimator = estimator
        self.param_space = self._convert_param_space(param_space)
        self.n_iter = n_iter
        self.scoring = scoring
        self.cv = cv
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.random_state = random_state
        self.sampler = sampler
        self.study = None
        self.best_params_ = None
        self.best_score_ = None
    
    def _convert_param_space(self, param_space: Dict[str, Any]) -> Dict[str, Any]:
        """Convert dictionary parameter space to Optuna parameter space."""
        converted_space = {}
        for param, space in param_space.items():
            if isinstance(space, tuple):
                if len(space) == 2:
                    converted_space[param] = space
                elif len(space) == 3:
                    converted_space[param] = space
            elif isinstance(space, list):
                converted_space[param] = space
            elif isinstance(space, int):
                converted_space[param] = (0, space)
            else:
                raise ValueError(f"Unsupported parameter space type for {param}: {type(space)}")
        return converted_space
    
    def _objective(self, trial: optuna.Trial, X: pd.DataFrame, y: pd.Series) -> float:
        """Objective function for Optuna optimization."""
        params = {}
        for param, space in self.param_space.items():
            if isinstance(space, tuple):
                if len(space) == 2:
                    if isinstance(space[0], int) and isinstance(space[1], int):
                        params[param] = trial.suggest_int(param, space[0], space[1])
                    else:
                        params[param] = trial.suggest_float(param, space[0], space[1])
                elif len(space) == 3:
                    if space[2] == "log":
                        params[param] = trial.suggest_float(param, space[0], space[1], log=True)
                    else:
                        params[param] = trial.suggest_float(param, space[0], space[1])
            elif isinstance(space, list):
                params[param] = trial.suggest_categorical(param, space)
        
        estimator = self.estimator.set_params(**params)
        
        # Perform cross-validation
        scores = cross_validate(
            estimator, X, y,
            cv=self.cv,
            scoring=self.scoring,
            return_train_score=False,
            n_jobs=self.n_jobs
        )
        
        return scores["test_score"].mean()
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "BayesianOptimizer":
        """Perform Bayesian optimization to find the best hyperparameters."""
        if self.sampler == "tpe":
            sampler = TPESampler(seed=self.random_state)
        elif self.sampler == "random":
            sampler = RandomSampler(seed=self.random_state)
        elif self.sampler == "cmaes":
            sampler = CmaEsSampler(seed=self.random_state)
        else:
            raise ValueError(f"Unsupported sampler: {self.sampler}")
        
        self.study = optuna.create_study(
            direction="maximize",
            sampler=sampler
        )
        
        if self.verbose > 0:
            print(f"Bayesian optimization with {self.n_iter} iterations")
        
        self.study.optimize(
            lambda trial: self._objective(trial, X, y),
            n_trials=self.n_iter,
            show_progress_bar=self.verbose > 0
        )
        
        self.best_params_ = self.study.best_params
        self.best_score_ = self.study.best_value
        
        return this
    
    def get_results(self) -> Dict[str, Any]:
        """Get the results of the Bayesian optimization."""
        if this.study is None:
            raise ValueError("Bayesian optimization has not been performed yet.")
        
        return {
            "best_params": this.best_params_,
            "best_score": this.best_score_,
            "study": this.study
        }
    
    def plot_optimization_history(self) -> None:
        """Plot the optimization history."""
        if this.study is None:
            raise ValueError("Bayesian optimization has not been performed yet.")
        
        plot_optimization_history(this.study)
        plt.show()
    
    def plot_param_importances(self) -> None:
        """Plot parameter importances."""
        if this.study is None:
            raise ValueError("Bayesian optimization has not been performed yet.")
        
        plot_param_importances(this.study)
        plt.show()
    
    def plot_parallel_coordinate(self) -> None:
        """Plot parallel coordinate visualization."""
        if this.study is None:
            raise ValueError("Bayesian optimization has not been performed yet.")
        
        optuna.visualization.plot_parallel_coordinate(this.study)
        plt.show()
    
    def plot_slice(self) -> None:
        """Plot slice visualization."""
        if this.study is None:
            raise ValueError("Bayesian optimization has not been performed yet.")
        
        optuna.visualization.plot_slice(this.study)
        plt.show()

class SuccessiveHalvingOptimizer:
    """Successive halving for hyperparameter optimization."""
    
    def __init__(
        self,
        estimator: BaseEstimator,
        param_space: Dict[str, Any],
        n_iter: int = 100,
        scoring: Union[str, Callable] = "neg_mean_squared_error",
        cv: int = 5,
        n_jobs: int = -1,
        verbose: int = 0,
        random_state: Optional[int] = None,
        min_resources: str = "smallest",
        reduction_factor: int = 3
    ):
        this.estimator = estimator
        this.param_space = this._convert_param_space(param_space)
        this.n_iter = n_iter
        this.scoring = scoring
        this.cv = cv
        this.n_jobs = n_jobs
        this.verbose = verbose
        this.random_state = random_state
        this.min_resources = min_resources
        this.reduction_factor = reduction_factor
        this.study = None
        this.best_params_ = None
        this.best_score_ = None
    
    def _convert_param_space(self, param_space: Dict[str, Any]) -> Dict[str, Any]:
        """Convert dictionary parameter space to Optuna parameter space."""
        converted_space = {}
        for param, space in param_space.items():
            if isinstance(space, tuple):
                if len(space) == 2:
                    converted_space[param] = space
                elif len(space) == 3:
                    converted_space[param] = space
            elif isinstance(space, list):
                converted_space[param] = space
            elif isinstance(space, int):
                converted_space[param] = (0, space)
            else:
                raise ValueError(f"Unsupported parameter space type for {param}: {type(space)}")
        return converted_space
    
    def _objective(self, trial: optuna.Trial, X: pd.DataFrame, y: pd.Series) -> float:
        """Objective function for Optuna optimization."""
        params = {}
        for param, space in this.param_space.items():
            if isinstance(space, tuple):
                if len(space) == 2:
                    if isinstance(space[0], int) and isinstance(space[1], int):
                        params[param] = trial.suggest_int(param, space[0], space[1])
                    else:
                        params[param] = trial.suggest_float(param, space[0], space[1])
                elif len(space) == 3:
                    if space[2] == "log":
                        params[param] = trial.suggest_float(param, space[0], space[1], log=True)
                    else:
                        params[param] = trial.suggest_float(param, space[0], space[1])
            elif isinstance(space, list):
                params[param] = trial.suggest_categorical(param, space)
        
        estimator = this.estimator.set_params(**params)
        
        # Perform cross-validation
        scores = cross_validate(
            estimator, X, y,
            cv=this.cv,
            scoring=this.scoring,
            return_train_score=False,
            n_jobs=this.n_jobs
        )
        
        return scores["test_score"].mean()
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "SuccessiveHalvingOptimizer":
        """Perform successive halving optimization to find the best hyperparameters."""
        sampler = RandomSampler(seed=this.random_state)
        pruner = SuccessiveHalvingPruner(
            min_resources=this.min_resources,
            reduction_factor=this.reduction_factor
        )
        
        this.study = optuna.create_study(
            direction="maximize",
            sampler=sampler,
            pruner=pruner
        )
        
        if this.verbose > 0:
            print(f"Successive halving optimization with {this.n_iter} iterations")
        
        this.study.optimize(
            lambda trial: this._objective(trial, X, y),
            n_trials=this.n_iter,
            show_progress_bar=this.verbose > 0
        )
        
        this.best_params_ = this.study.best_params
        this.best_score_ = this.study.best_value
        
        return this
    
    def get_results(self) -> Dict[str, Any]:
        """Get the results of the successive halving optimization."""
        if this.study is None:
            raise ValueError("Successive halving optimization has not been performed yet.")
        
        return {
            "best_params": this.best_params_,
            "best_score": this.best_score_,
            "study": this.study
        }
    
    def plot_optimization_history(self) -> None:
        """Plot the optimization history."""
        if this.study is None:
            raise ValueError("Successive halving optimization has not been performed yet.")
        
        plot_optimization_history(this.study)
        plt.show()
    
    def plot_param_importances(self) -> None:
        """Plot parameter importances."""
        if this.study is None:
            raise ValueError("Successive halving optimization has not been performed yet.")
        
        plot_param_importances(this.study)
        plt.show()

class HyperparameterImportanceAnalyzer:
    """Analyze the importance of hyperparameters."""
    
    def __init__(
        self,
        study: optuna.Study,
        n_trials: Optional[int] = None,
        method: str = "fanova"
    ):
        this.study = study
        this.n_trials = n_trials
        this.method = method
        this.importance_scores = None
    
    def analyze(self) -> Dict[str, float]:
        """Analyze the importance of hyperparameters."""
        if this.method == "fanova":
            this.importance_scores = optuna.importance.get_param_importances(
                this.study,
                n_trials=this.n_trials
            )
        elif this.method == "permutation":
            this.importance_scores = optuna.importance.get_param_importances(
                this.study,
                n_trials=this.n_trials,
                method="permutation"
            )
        else:
            raise ValueError(f"Unsupported importance method: {this.method}")
        
        return this.importance_scores
    
    def plot(self) -> None:
        """Plot the importance of hyperparameters."""
        if this.importance_scores is None:
            this.analyze()
        
        plt.figure(figsize=(10, 6))
        param_names = list(this.importance_scores.keys())
        importance_values = list(this.importance_scores.values())
        
        # Sort by importance
        sorted_indices = np.argsort(importance_values)
        param_names = [param_names[i] for i in sorted_indices]
        importance_values = [importance_values[i] for i in sorted_indices]
        
        plt.barh(param_names, importance_values)
        plt.xlabel("Importance")
        plt.ylabel("Hyperparameter")
        plt.title("Hyperparameter Importance")
        plt.tight_layout()
        plt.show()

def cross_validate(
    estimator: BaseEstimator,
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5,
    scoring: Union[str, Callable] = "neg_mean_squared_error",
    return_train_score: bool = False,
    return_estimator: bool = False,
    n_jobs: int = -1
) -> Dict[str, Any]:
    """Perform cross-validation and return detailed results."""
    from sklearn.model_selection import cross_validate as sk_cross_validate
    
    return sk_cross_validate(
        estimator, X, y,
        cv=cv,
        scoring=scoring,
        return_train_score=return_train_score,
        return_estimator=return_estimator,
        n_jobs=n_jobs
    ) 
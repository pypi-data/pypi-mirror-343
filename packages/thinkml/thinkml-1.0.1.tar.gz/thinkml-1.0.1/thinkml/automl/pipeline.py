"""
AutoML pipeline implementation for ThinkML.

This module implements an automated machine learning pipeline that handles
data preprocessing, model selection, and evaluation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional, Tuple, Any
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from thinkml.data_analysis import describe_data
from thinkml.preprocessor import handle_extreme_values, handle_duplicates, handle_missing_values
from thinkml.preprocessor import encode_categorical_features, scale_numerical_features
from thinkml.feature_selection import select_features
from thinkml.algorithms import (
    LogisticRegression, RandomForestClassifier, GradientBoostingClassifier,
    SVM, NeuralNetwork, LinearRegression, RandomForestRegressor,
    GradientBoostingRegressor
)

def _is_dask_dataframe(df: Any) -> bool:
    """Check if the input is a Dask DataFrame."""
    return isinstance(df, dd.DataFrame)

def _convert_to_pandas(df: Union[pd.DataFrame, dd.DataFrame]) -> pd.DataFrame:
    """Convert Dask DataFrame to pandas DataFrame if necessary."""
    if _is_dask_dataframe(df):
        with ProgressBar():
            return df.compute()
    return df

def _validate_input(X: Union[pd.DataFrame, dd.DataFrame], y: Optional[pd.Series] = None) -> None:
    """Validate input data."""
    if X.empty:
        raise ValueError("Input DataFrame X cannot be empty")
    
    if y is not None:
        if len(X) != len(y):
            raise ValueError("Length of X and y must be equal")
        
        if _is_dask_dataframe(X) and not _is_dask_dataframe(y):
            raise ValueError("If X is a Dask DataFrame, y must also be a Dask Series")
        
        if not _is_dask_dataframe(X) and _is_dask_dataframe(y):
            raise ValueError("If X is a pandas DataFrame, y must also be a pandas Series")

def _get_models(problem_type: str) -> List[Any]:
    """Get list of models based on problem type."""
    if problem_type == 'classification':
        return [
            LogisticRegression(),
            RandomForestClassifier(n_estimators=100, random_state=42),
            GradientBoostingClassifier(n_estimators=100, random_state=42),
            SVM(kernel='rbf', random_state=42),
            NeuralNetwork(hidden_layer_sizes=(100,), random_state=42)
        ]
    else:  # regression
        return [
            LinearRegression(),
            RandomForestRegressor(n_estimators=100, random_state=42),
            GradientBoostingRegressor(n_estimators=100, random_state=42)
        ]

def cross_val_score(estimator, X, y, cv=5, scoring=None):
    """
    Evaluate a score by cross-validation.
    
    Parameters
    ----------
    estimator : object
        The object to use to fit the data.
    X : array-like of shape (n_samples, n_features)
        Training data.
    y : array-like of shape (n_samples,)
        Target values.
    cv : int, default=5
        Number of folds for cross-validation.
    scoring : str or callable, default=None
        Strategy to evaluate the performance of the cross-validated model on
        the test set.
        
    Returns
    -------
    scores : array of float, shape=(len(cv),)
        Array of scores of the estimator for each run of the cross validation.
    """
    X = np.asarray(X)
    y = np.asarray(y)
    
    n_samples = len(X)
    fold_size = n_samples // cv
    scores = []
    
    for i in range(cv):
        # Calculate indices for this fold
        start_idx = i * fold_size
        end_idx = start_idx + fold_size if i < cv - 1 else n_samples
        
        # Create train and test indices
        test_indices = np.arange(start_idx, end_idx)
        train_indices = np.concatenate([np.arange(0, start_idx), np.arange(end_idx, n_samples)])
        
        # Split data
        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]
        
        # Fit and predict
        estimator.fit(X_train, y_train)
        y_pred = estimator.predict(X_test)
        
        # Calculate score
        if scoring == 'accuracy':
            score = accuracy_score(y_test, y_pred)
        elif scoring == 'r2':
            score = r2_score(y_test, y_pred)
        elif scoring == 'mse':
            score = mean_squared_error(y_test, y_pred)
        else:
            raise ValueError(f"Unknown scoring metric: {scoring}")
        
        scores.append(score)
    
    return np.array(scores)

def accuracy_score(y_true, y_pred):
    """
    Accuracy classification score.
    
    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth (correct) labels.
    y_pred : array-like of shape (n_samples,)
        Predicted labels.
        
    Returns
    -------
    score : float
        The accuracy score.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    return np.mean(y_true == y_pred)

def r2_score(y_true, y_pred):
    """
    R^2 (coefficient of determination) regression score.
    
    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth (correct) target values.
    y_pred : array-like of shape (n_samples,)
        Estimated target values.
        
    Returns
    -------
    score : float
        The R^2 score.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    
    if ss_tot == 0:
        return 0.0
    
    return 1 - (ss_res / ss_tot)

def mean_squared_error(y_true, y_pred):
    """
    Mean squared error regression loss.
    
    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth (correct) target values.
    y_pred : array-like of shape (n_samples,)
        Estimated target values.
        
    Returns
    -------
    score : float
        The mean squared error.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    return np.mean((y_true - y_pred) ** 2)

def automl_pipeline(
    X: Union[pd.DataFrame, dd.DataFrame],
    y: Optional[pd.Series] = None,
    problem_type: Optional[str] = None,
    target_column: Optional[str] = None,
    test_size: float = 0.2,
    random_state: int = 42,
    verbose: bool = True
) -> Dict:
    """
    Run the AutoML pipeline.
    
    Parameters
    ----------
    X : Union[pd.DataFrame, dd.DataFrame]
        Input features DataFrame.
    y : Optional[pd.Series], default=None
        Target variable. If None, target_column must be provided.
    problem_type : Optional[str], default=None
        Type of problem: 'classification' or 'regression'.
        If None, it will be inferred from the target variable.
    target_column : Optional[str], default=None
        Name of the target column in X. Used only if y is None.
    test_size : float, default=0.2
        Proportion of the dataset to include in the test split.
    random_state : int, default=42
        Random state for reproducibility.
    verbose : bool, default=True
        Whether to print progress information.
        
    Returns
    -------
    Dict
        Dictionary containing:
        - 'best_model': The best performing model
        - 'best_score': The score of the best model
        - 'evaluation_report': Dictionary with evaluation metrics for all models
        - 'preprocessing_steps': List of preprocessing steps applied
        - 'feature_importance': Dictionary of feature importance scores
    """
    # Validate input
    _validate_input(X, y)
    
    # Handle target variable
    if y is None:
        if target_column is None:
            raise ValueError("Either y or target_column must be provided")
        if target_column not in X.columns:
            raise ValueError(f"Target column '{target_column}' not found in X")
        y = X[target_column]
        X = X.drop(columns=[target_column])
    
    # Determine problem type if not provided
    if problem_type is None:
        if len(np.unique(y)) < 10:  # Assuming classification if less than 10 unique values
            problem_type = 'classification'
        else:
            problem_type = 'regression'
    
    if problem_type not in ['classification', 'regression']:
        raise ValueError("problem_type must be either 'classification' or 'regression'")
    
    # Convert to pandas if necessary
    X = _convert_to_pandas(X)
    y = _convert_to_pandas(y) if _is_dask_dataframe(y) else y
    
    # Describe data
    if verbose:
        print("Analyzing data...")
    data_summary = describe_data(X, y)
    
    # Preprocess data
    if verbose:
        print("Preprocessing data...")
    
    # Handle extreme values
    X = handle_extreme_values(X, method='iqr')
    
    # Handle duplicates
    X = handle_duplicates(X)
    
    # Handle missing values
    X = handle_missing_values(X, method='mean')
    
    # Encode categorical features
    X = encode_categorical_features(X, method='onehot')
    
    # Scale numerical features
    X = scale_numerical_features(X, method='standard')
    
    # Select features
    if verbose:
        print("Selecting features...")
    feature_selection = select_features(X, y, method='mutual_info')
    X = X[feature_selection['selected_features']]
    
    # Get models
    models = _get_models(problem_type)
    
    # Train and evaluate models
    if verbose:
        print("Training and evaluating models...")
    
    evaluation_report = {}
    best_score = float('-inf')
    best_model = None
    
    for model in models:
        # Determine scoring metric
        if problem_type == 'classification':
            scoring = 'accuracy'
        else:
            scoring = 'r2'
        
        # Cross validate
        scores = cross_val_score(model, X, y, cv=5, scoring=scoring)
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        
        # Update best model
        if mean_score > best_score:
            best_score = mean_score
            best_model = model
        
        # Store results
        evaluation_report[model.__class__.__name__] = {
            'mean_score': mean_score,
            'std_score': std_score,
            'scores': scores
        }
    
    # Display results
    if verbose:
        print("\nEvaluation Results:")
        for model_name, results in evaluation_report.items():
            print(f"{model_name}:")
            print(f"  Mean Score: {results['mean_score']:.4f} (±{results['std_score']:.4f})")
        
        print(f"\nBest Model: {best_model.__class__.__name__}")
        print(f"Best Score: {best_score:.4f}")
    
    return {
        'best_model': best_model,
        'best_score': best_score,
        'evaluation_report': evaluation_report,
        'preprocessing_steps': [
            'handle_extreme_values',
            'handle_duplicates',
            'handle_missing_values',
            'encode_categorical_features',
            'scale_numerical_features',
            'select_features'
        ],
        'feature_importance': feature_selection['scores']
    } 
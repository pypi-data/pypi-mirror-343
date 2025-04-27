"""
Model training and prediction functionality for ThinkML.

This module provides functions for training multiple models,
evaluating their performance, and making predictions.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Dict, Union, List, Tuple, Any, Optional
import dask_ml.linear_model as dask_linear
import dask_ml.ensemble as dask_ensemble
import dask_ml.neighbors as dask_neighbors
import dask_ml.metrics as dask_metrics

# Import our own model implementations
from thinkml.algorithms import (
    LogisticRegression,
    LinearRegression,
    RidgeRegression,
    DecisionTreeClassifier,
    DecisionTreeRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
    KNeighborsClassifier
)

# Import our own metrics implementations
from thinkml.evaluation.metrics import (
    accuracy_score,
    f1_score,
    mean_squared_error,
    r2_score
)

def train_multiple_models(
    X_train: Union[pd.DataFrame, dd.DataFrame],
    y_train: Union[pd.Series, np.ndarray, dd.Series],
    X_test: Union[pd.DataFrame, dd.DataFrame],
    y_test: Union[pd.Series, np.ndarray, dd.Series],
    problem_type: str = 'classification'
) -> Tuple[Dict[str, Any], Dict[str, Dict[str, float]]]:
    """
    Train multiple models and evaluate their performance.
    
    Parameters
    ----------
    X_train : Union[pd.DataFrame, dd.DataFrame]
        Training features
    y_train : Union[pd.Series, np.ndarray, dd.Series]
        Training target
    X_test : Union[pd.DataFrame, dd.DataFrame]
        Test features
    y_test : Union[pd.Series, np.ndarray, dd.Series]
        Test target
    problem_type : str, default='classification'
        Type of problem: 'classification' or 'regression'
        
    Returns
    -------
    Tuple[Dict[str, Any], Dict[str, Dict[str, float]]]
        A tuple containing:
        - Dictionary of model name -> trained model object
        - Dictionary of model name -> evaluation metrics
    """
    # Input validation
    if problem_type not in ['classification', 'regression']:
        raise ValueError("problem_type must be 'classification' or 'regression'")
    
    # Check if we're working with Dask DataFrames
    is_dask = isinstance(X_train, dd.DataFrame)
    
    # Determine if we should use Dask models based on dataset size
    use_dask_models = is_dask or (isinstance(X_train, pd.DataFrame) and len(X_train) > 1_000_000)
    
    # Initialize models based on problem type and data size
    if problem_type == 'classification':
        if use_dask_models:
            models = {
                'Logistic Regression': dask_linear.LogisticRegression(),
                'Decision Tree': dask_ensemble.DecisionTreeClassifier(),
                'Random Forest': dask_ensemble.RandomForestClassifier(),
                'KNN': dask_neighbors.KNeighborsClassifier()
            }
        else:
            models = {
                'Logistic Regression': LogisticRegression(),
                'Decision Tree': DecisionTreeClassifier(),
                'Random Forest': RandomForestClassifier(),
                'KNN': KNeighborsClassifier()
            }
    else:  # regression
        if use_dask_models:
            models = {
                'Linear Regression': dask_linear.LinearRegression(),
                'Ridge Regression': dask_linear.Ridge(),
                'Decision Tree': dask_ensemble.DecisionTreeRegressor(),
                'Random Forest': dask_ensemble.RandomForestRegressor()
            }
        else:
            models = {
                'Linear Regression': LinearRegression(),
                'Ridge Regression': RidgeRegression(),
                'Decision Tree': DecisionTreeRegressor(),
                'Random Forest': RandomForestRegressor()
            }
    
    # Train models and evaluate performance
    trained_models = {}
    evaluation_scores = {}
    
    for name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Evaluate performance
        if problem_type == 'classification':
            scores = {
                'accuracy': accuracy_score(y_test, y_pred),
                'f1': f1_score(y_test, y_pred)
            }
        else:  # regression
            scores = {
                'mse': mean_squared_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred)
            }
        
        # Store results
        trained_models[name] = model
        evaluation_scores[name] = scores
    
    # Display evaluation report
    _display_evaluation_report(evaluation_scores, problem_type)
    
    return trained_models, evaluation_scores


def predict_with_model(
    model: Any,
    X_new: Union[pd.DataFrame, dd.DataFrame]
) -> Union[np.ndarray, pd.Series, dd.Series]:
    """
    Make predictions using a trained model.
    
    Parameters
    ----------
    model : Any
        Trained model object
    X_new : Union[pd.DataFrame, dd.DataFrame]
        New data to make predictions for
        
    Returns
    -------
    Union[np.ndarray, pd.Series, dd.Series]
        Predictions for the new data
    """
    # Input validation
    if not hasattr(model, 'predict'):
        raise ValueError("Model must have a 'predict' method")
    
    # Make predictions
    return model.predict(X_new)


def _display_evaluation_report(
    evaluation_scores: Dict[str, Dict[str, float]],
    problem_type: str
) -> None:
    """
    Display a summary of model evaluation scores.
    
    Parameters
    ----------
    evaluation_scores : Dict[str, Dict[str, float]]
        Dictionary of model name -> evaluation metrics
    problem_type : str
        Type of problem: 'classification' or 'regression'
    """
    print("\n===== MODEL EVALUATION REPORT =====")
    
    if problem_type == 'classification':
        print(f"{'Model':<20} {'Accuracy':<10} {'F1 Score':<10}")
        print("-" * 40)
        for model_name, scores in evaluation_scores.items():
            print(f"{model_name:<20} {scores['accuracy']:<10.4f} {scores['f1']:<10.4f}")
    else:  # regression
        print(f"{'Model':<20} {'MSE':<10} {'R²':<10}")
        print("-" * 40)
        for model_name, scores in evaluation_scores.items():
            print(f"{model_name:<20} {scores['mse']:<10.4f} {scores['r2']:<10.4f}")
    
    print("=====================================\n") 
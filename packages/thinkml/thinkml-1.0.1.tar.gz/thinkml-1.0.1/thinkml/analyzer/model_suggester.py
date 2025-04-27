"""
Model suggestion functionality for ThinkML.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.metrics import make_scorer, accuracy_score, r2_score, mean_squared_error

class ModelSuggester:
    """
    Class for suggesting the best model based on data characteristics.
    """
    
    def __init__(
        self,
        task: str = 'classification',
        cv: int = 5,
        scoring: Optional[str] = None,
        random_state: Optional[int] = None
    ):
        """
        Initialize the ModelSuggester.

        Args:
            task: Type of task ('classification' or 'regression')
            cv: Number of cross-validation folds
            scoring: Scoring metric
            random_state: Random state for reproducibility
        """
        self.task = task
        self.cv = cv
        self.random_state = random_state
        
        # Set default scoring based on task
        if scoring is None:
            self.scoring = 'accuracy' if task == 'classification' else 'r2'
        else:
            self.scoring = scoring
        
        # Initialize model candidates
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize candidate models based on task type."""
        if self.task == 'classification':
            self.models = {
                'random_forest': RandomForestClassifier(
                    random_state=self.random_state
                ),
                'logistic_regression': LogisticRegression(
                    random_state=self.random_state
                ),
                'svm': SVC(
                    probability=True,
                    random_state=self.random_state
                ),
                'knn': KNeighborsClassifier(),
                'decision_tree': DecisionTreeClassifier(
                    random_state=self.random_state
                ),
                'neural_network': MLPClassifier(
                    random_state=self.random_state
                )
            }
        else:  # regression
            self.models = {
                'random_forest': RandomForestRegressor(
                    random_state=self.random_state
                ),
                'linear_regression': LinearRegression(),
                'svm': SVR(),
                'knn': KNeighborsRegressor(),
                'decision_tree': DecisionTreeRegressor(
                    random_state=self.random_state
                ),
                'neural_network': MLPRegressor(
                    random_state=self.random_state
                )
            }
    
    def _analyze_data(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> Dict[str, float]:
        """
        Analyze data characteristics to help with model selection.

        Args:
            X: Input features
            y: Target variable

        Returns:
            Dictionary of data characteristics
        """
        characteristics = {}
        
        # Basic characteristics
        characteristics['n_samples'] = len(X)
        characteristics['n_features'] = X.shape[1]
        characteristics['feature_types'] = {
            'numeric': X.select_dtypes(include=[np.number]).shape[1],
            'categorical': X.select_dtypes(exclude=[np.number]).shape[1]
        }
        
        # Class balance (for classification)
        if self.task == 'classification':
            class_counts = y.value_counts()
            characteristics['n_classes'] = len(class_counts)
            characteristics['class_balance'] = class_counts.min() / class_counts.max()
        
        # Missing values
        characteristics['missing_ratio'] = X.isnull().sum().sum() / (X.shape[0] * X.shape[1])
        
        # Feature correlation
        numeric_X = X.select_dtypes(include=[np.number])
        if not numeric_X.empty:
            correlations = numeric_X.corr().abs()
            characteristics['max_correlation'] = correlations.where(
                ~np.eye(correlations.shape[0], dtype=bool)
            ).max().max()
        
        return characteristics
    
    def suggest_model(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        return_scores: bool = False
    ) -> Union[str, Tuple[str, Dict[str, float]]]:
        """
        Suggest the best model based on data characteristics and cross-validation.

        Args:
            X: Input features
            y: Target variable
            return_scores: Whether to return scores for all models

        Returns:
            Best model name or tuple of (best model name, all scores)
        """
        # Analyze data
        characteristics = self._analyze_data(X, y)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Evaluate models
        scores = {}
        for name, model in self.models.items():
            try:
                cv_scores = cross_val_score(
                    model,
                    X_scaled,
                    y,
                    cv=self.cv,
                    scoring=self.scoring
                )
                scores[name] = cv_scores.mean()
            except Exception as e:
                print(f"Warning: {name} failed with error: {str(e)}")
                scores[name] = float('-inf')
        
        # Get best model
        best_model = max(scores.items(), key=lambda x: x[1])[0]
        
        if return_scores:
            return best_model, scores
        return best_model
    
    def get_model_recommendations(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> Dict[str, Dict[str, Union[float, str]]]:
        """
        Get detailed recommendations for each model.

        Args:
            X: Input features
            y: Target variable

        Returns:
            Dictionary with model recommendations and explanations
        """
        # Get model scores
        best_model, scores = self.suggest_model(X, y, return_scores=True)
        characteristics = self._analyze_data(X, y)
        
        recommendations = {}
        for model_name in self.models:
            recommendation = {
                'score': scores[model_name],
                'rank': sorted(
                    scores.items(),
                    key=lambda x: x[1],
                    reverse=True
                ).index((model_name, scores[model_name])) + 1,
                'recommendation': self._get_model_recommendation(
                    model_name,
                    characteristics,
                    scores[model_name]
                )
            }
            recommendations[model_name] = recommendation
        
        return recommendations
    
    def _get_model_recommendation(
        self,
        model_name: str,
        characteristics: Dict[str, float],
        score: float
    ) -> str:
        """Generate a recommendation for a specific model."""
        recommendation = []
        
        # General performance
        if score == float('-inf'):
            recommendation.append("Failed to evaluate.")
            return " ".join(recommendation)
        
        # Model-specific recommendations
        if model_name == 'random_forest':
            if characteristics['n_samples'] < 1000:
                recommendation.append(
                    "May overfit due to small sample size."
                )
            else:
                recommendation.append(
                    "Good choice for complex relationships."
                )
        
        elif model_name in ['logistic_regression', 'linear_regression']:
            if characteristics.get('max_correlation', 0) > 0.9:
                recommendation.append(
                    "High feature correlation may affect performance."
                )
            if characteristics['n_features'] > 1000:
                recommendation.append(
                    "Large number of features may cause issues."
                )
        
        elif model_name == 'svm':
            if characteristics['n_samples'] > 10000:
                recommendation.append(
                    "May be slow due to large sample size."
                )
            if characteristics['n_features'] > 1000:
                recommendation.append(
                    "Consider dimensionality reduction."
                )
        
        elif model_name == 'knn':
            if characteristics['n_samples'] > 100000:
                recommendation.append(
                    "May be slow for predictions."
                )
            if characteristics['missing_ratio'] > 0.1:
                recommendation.append(
                    "Sensitive to missing values."
                )
        
        elif model_name == 'neural_network':
            if characteristics['n_samples'] < 1000:
                recommendation.append(
                    "May need more data for good performance."
                )
            if characteristics['n_features'] < 10:
                recommendation.append(
                    "Simple architecture may suffice."
                )
        
        # Add performance-based recommendation
        if score > 0.9:
            recommendation.append("Excellent performance.")
        elif score > 0.7:
            recommendation.append("Good performance.")
        elif score > 0.5:
            recommendation.append("Moderate performance.")
        else:
            recommendation.append("Poor performance.")
        
        return " ".join(recommendation)

def suggest_model(
    X: pd.DataFrame,
    y: pd.Series,
    task: str = 'classification',
    cv: int = 5,
    scoring: Optional[str] = None,
    random_state: Optional[int] = None,
    return_scores: bool = False
) -> Union[str, Tuple[str, Dict[str, float]]]:
    """
    Suggest the best model for the given data.

    Args:
        X: Input features
        y: Target variable
        task: Type of task ('classification' or 'regression')
        cv: Number of cross-validation folds
        scoring: Scoring metric
        random_state: Random state for reproducibility
        return_scores: Whether to return scores for all models

    Returns:
        Best model name or tuple of (best model name, all scores)
    """
    suggester = ModelSuggester(
        task=task,
        cv=cv,
        scoring=scoring,
        random_state=random_state
    )
    return suggester.suggest_model(X, y, return_scores=return_scores) 
"""
Advanced feature engineering utilities for ThinkML.
Implements polynomial features, feature interactions, and time-based feature extraction.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

class FeatureEngineer:
    """Advanced feature engineering utilities."""
    
    def __init__(
        self,
        polynomial_degree: int = 2,
        interaction_only: bool = False,
        include_bias: bool = False
    ):
        self.polynomial_degree = polynomial_degree
        self.interaction_only = interaction_only
        self.include_bias = include_bias
        self.poly_features = None
        self.feature_names = None
        
    def create_polynomial_features(
        self,
        X: pd.DataFrame,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Create polynomial features for specified columns."""
        if columns is None:
            columns = X.columns.tolist()
        
        X_subset = X[columns]
        self.poly_features = PolynomialFeatures(
            degree=self.polynomial_degree,
            interaction_only=self.interaction_only,
            include_bias=self.include_bias
        )
        
        poly_features = self.poly_features.fit_transform(X_subset)
        self.feature_names = self.poly_features.get_feature_names_out(columns)
        
        return pd.DataFrame(
            poly_features,
            columns=self.feature_names,
            index=X.index
        )
    
    def detect_feature_interactions(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        task: str = "regression",
        threshold: float = 0.01
    ) -> Dict[Tuple[str, str], float]:
        """Detect significant feature interactions using mutual information."""
        interactions = {}
        features = X.columns.tolist()
        
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                interaction = X[features[i]] * X[features[j]]
                if task == "regression":
                    mi_score = mutual_info_regression(
                        interaction.values.reshape(-1, 1),
                        y
                    )[0]
                else:
                    mi_score = mutual_info_classif(
                        interaction.values.reshape(-1, 1),
                        y
                    )[0]
                
                if mi_score > threshold:
                    interactions[(features[i], features[j])] = mi_score
        
        return dict(sorted(
            interactions.items(),
            key=lambda x: x[1],
            reverse=True
        ))
    
    def create_time_features(
        self,
        df: pd.DataFrame,
        date_column: str,
        features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Create time-based features from a datetime column."""
        if features is None:
            features = [
                "year", "month", "day", "dayofweek",
                "quarter", "is_month_start", "is_month_end",
                "is_quarter_start", "is_quarter_end"
            ]
        
        df = df.copy()
        date_series = pd.to_datetime(df[date_column])
        
        if "year" in features:
            df[f"{date_column}_year"] = date_series.dt.year
        if "month" in features:
            df[f"{date_column}_month"] = date_series.dt.month
        if "day" in features:
            df[f"{date_column}_day"] = date_series.dt.day
        if "dayofweek" in features:
            df[f"{date_column}_dayofweek"] = date_series.dt.dayofweek
        if "quarter" in features:
            df[f"{date_column}_quarter"] = date_series.dt.quarter
        if "is_month_start" in features:
            df[f"{date_column}_is_month_start"] = date_series.dt.is_month_start.astype(int)
        if "is_month_end" in features:
            df[f"{date_column}_is_month_end"] = date_series.dt.is_month_end.astype(int)
        if "is_quarter_start" in features:
            df[f"{date_column}_is_quarter_start"] = date_series.dt.is_quarter_start.astype(int)
        if "is_quarter_end" in features:
            df[f"{date_column}_is_quarter_end"] = date_series.dt.is_quarter_end.astype(int)
        
        return df
    
    def create_rolling_features(
        self,
        df: pd.DataFrame,
        value_column: str,
        date_column: str,
        windows: List[int] = [7, 14, 30],
        functions: List[str] = ["mean", "std", "min", "max"]
    ) -> pd.DataFrame:
        """Create rolling window features."""
        df = df.copy()
        date_series = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)
        
        for window in windows:
            for func in functions:
                col_name = f"{value_column}_rolling_{window}d_{func}"
                df[col_name] = df[value_column].rolling(
                    window=window,
                    min_periods=1
                ).agg(func)
        
        return df
    
    def analyze_feature_importance(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        task: str = "regression",
        n_estimators: int = 100
    ) -> pd.Series:
        """Analyze feature importance using Random Forest."""
        if task == "regression":
            model = RandomForestRegressor(n_estimators=n_estimators)
        else:
            model = RandomForestClassifier(n_estimators=n_estimators)
        
        model.fit(X, y)
        importance = pd.Series(
            model.feature_importances_,
            index=X.columns
        ).sort_values(ascending=False)
        
        return importance
    
    def plot_feature_importance(
        self,
        importance: pd.Series,
        top_n: Optional[int] = None
    ) -> None:
        """Plot feature importance scores."""
        if top_n is not None:
            importance = importance.head(top_n)
        
        plt.figure(figsize=(10, 6))
        importance.plot(kind="bar")
        plt.title("Feature Importance")
        plt.xlabel("Features")
        plt.ylabel("Importance Score")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
    
    def create_domain_features(
        self,
        df: pd.DataFrame,
        rules: Dict[str, callable]
    ) -> pd.DataFrame:
        """Create domain-specific features using custom rules."""
        df = df.copy()
        for feature_name, rule in rules.items():
            df[feature_name] = rule(df)
        return df
    
    def detect_feature_correlations(
        self,
        df: pd.DataFrame,
        method: str = "pearson",
        threshold: float = 0.8
    ) -> pd.DataFrame:
        """Detect highly correlated features."""
        corr_matrix = df.corr(method=method)
        high_corr = np.where(np.abs(corr_matrix) > threshold)
        high_corr = [(corr_matrix.index[x], corr_matrix.columns[y], corr_matrix.iloc[x, y])
                    for x, y in zip(*high_corr) if x != y and x < y]
        
        return pd.DataFrame(
            high_corr,
            columns=["Feature 1", "Feature 2", "Correlation"]
        )
    
    def plot_correlation_matrix(
        self,
        df: pd.DataFrame,
        method: str = "pearson"
    ) -> None:
        """Plot correlation matrix heatmap."""
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            df.corr(method=method),
            annot=True,
            cmap="coolwarm",
            center=0,
            fmt=".2f"
        )
        plt.title("Feature Correlation Matrix")
        plt.tight_layout()
        plt.show() 
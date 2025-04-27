"""
Feature Engineering Module for ThinkML.

This module provides advanced feature engineering functionality including:
- Feature creation and transformation
- Feature selection
- Feature scaling and normalization
- Feature interaction and polynomial features
- Time series feature engineering
- Text feature engineering
"""

import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any, Optional, Tuple
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression, mutual_info_classif
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import PolynomialFeatures
import category_encoders as ce

class FeatureEngineer:
    """
    A class for advanced feature engineering techniques.
    
    This class provides methods for:
    - Feature creation and transformation
    - Feature selection
    - Feature scaling and normalization
    - Feature interaction and polynomial features
    - Time series feature engineering
    - Text feature engineering
    """
    
    def __init__(self):
        """Initialize the FeatureEngineer class."""
        self.transformers = {}
        self.selected_features = None
        
    def create_features(self, 
                       df: pd.DataFrame,
                       numeric_cols: Optional[List[str]] = None,
                       categorical_cols: Optional[List[str]] = None,
                       datetime_cols: Optional[List[str]] = None,
                       text_cols: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Create new features from existing columns.
        
        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe
        numeric_cols : list, optional
            List of numeric column names
        categorical_cols : list, optional
            List of categorical column names
        datetime_cols : list, optional
            List of datetime column names
        text_cols : list, optional
            List of text column names
            
        Returns
        -------
        pd.DataFrame
            DataFrame with new features
        """
        df_new = df.copy()
        
        # Numeric feature creation
        if numeric_cols:
            for col in numeric_cols:
                if col in df.columns:
                    # Square and cube
                    df_new[f'{col}_squared'] = df[col] ** 2
                    df_new[f'{col}_cubed'] = df[col] ** 3
                    # Log transform (handle zeros)
                    df_new[f'{col}_log'] = np.log1p(df[col])
                    # Rolling statistics
                    df_new[f'{col}_rolling_mean'] = df[col].rolling(window=3, min_periods=1).mean()
                    df_new[f'{col}_rolling_std'] = df[col].rolling(window=3, min_periods=1).std()
        
        # Categorical feature creation
        if categorical_cols:
            for col in categorical_cols:
                if col in df.columns:
                    # Frequency encoding
                    df_new[f'{col}_freq'] = df[col].map(df[col].value_counts(normalize=True))
                    # One-hot encoding
                    dummies = pd.get_dummies(df[col], prefix=col)
                    df_new = pd.concat([df_new, dummies], axis=1)
        
        # Datetime feature creation
        if datetime_cols:
            for col in datetime_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])
                    df_new[f'{col}_year'] = df[col].dt.year
                    df_new[f'{col}_month'] = df[col].dt.month
                    df_new[f'{col}_day'] = df[col].dt.day
                    df_new[f'{col}_dayofweek'] = df[col].dt.dayofweek
                    df_new[f'{col}_quarter'] = df[col].dt.quarter
        
        # Text feature creation
        if text_cols:
            for col in text_cols:
                if col in df.columns:
                    # Basic text features
                    df_new[f'{col}_length'] = df[col].str.len()
                    df_new[f'{col}_word_count'] = df[col].str.split().str.len()
                    # TF-IDF features
                    tfidf = TfidfVectorizer(max_features=10)
                    tfidf_features = tfidf.fit_transform(df[col])
                    tfidf_df = pd.DataFrame(tfidf_features.toarray(), 
                                          columns=[f'{col}_tfidf_{i}' for i in range(10)])
                    df_new = pd.concat([df_new, tfidf_df], axis=1)
        
        return df_new
    
    def select_features(self,
                       X: Union[np.ndarray, pd.DataFrame],
                       y: Union[np.ndarray, pd.Series],
                       method: str = 'mutual_info',
                       n_features: int = 10,
                       task: str = 'regression') -> Tuple[np.ndarray, List[int]]:
        """
        Select the most important features.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        method : str, default='mutual_info'
            Feature selection method ('mutual_info', 'pca')
        n_features : int, default=10
            Number of features to select
        task : str, default='regression'
            Task type ('regression' or 'classification')
            
        Returns
        -------
        tuple
            Selected features array and indices of selected features
        """
        if method == 'mutual_info':
            if task == 'regression':
                selector = SelectKBest(score_func=mutual_info_regression, k=n_features)
            else:
                selector = SelectKBest(score_func=mutual_info_classif, k=n_features)
            X_selected = selector.fit_transform(X, y)
            selected_indices = selector.get_support(indices=True)
        elif method == 'pca':
            pca = PCA(n_components=n_features)
            X_selected = pca.fit_transform(X)
            selected_indices = list(range(n_features))
        else:
            raise ValueError(f"Unknown feature selection method: {method}")
        
        self.selected_features = selected_indices
        return X_selected, selected_indices
    
    def scale_features(self,
                      X: Union[np.ndarray, pd.DataFrame],
                      method: str = 'standard') -> np.ndarray:
        """
        Scale features using various methods.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Features to scale
        method : str, default='standard'
            Scaling method ('standard', 'minmax', 'robust')
            
        Returns
        -------
        np.ndarray
            Scaled features
        """
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        return scaler.fit_transform(X)
    
    def create_interactions(self,
                          X: Union[np.ndarray, pd.DataFrame],
                          degree: int = 2) -> np.ndarray:
        """
        Create polynomial feature interactions.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Features to create interactions from
        degree : int, default=2
            Degree of polynomial features
            
        Returns
        -------
        np.ndarray
            Features with interactions
        """
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        return poly.fit_transform(X)
    
    def encode_categorical(self,
                         X: Union[np.ndarray, pd.DataFrame],
                         method: str = 'target',
                         cols: Optional[List[str]] = None) -> np.ndarray:
        """
        Encode categorical variables.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Features to encode
        method : str, default='target'
            Encoding method ('target', 'onehot', 'label')
        cols : list, optional
            List of categorical columns to encode
            
        Returns
        -------
        np.ndarray
            Encoded features
        """
        if method == 'target':
            encoder = ce.TargetEncoder(cols=cols)
        elif method == 'onehot':
            encoder = ce.OneHotEncoder(cols=cols)
        elif method == 'label':
            encoder = ce.LabelEncoder(cols=cols)
        else:
            raise ValueError(f"Unknown encoding method: {method}")
        
        return encoder.fit_transform(X)
    
    def create_time_features(self,
                           df: pd.DataFrame,
                           time_col: str,
                           freq: str = 'D') -> pd.DataFrame:
        """
        Create time-based features.
        
        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe
        time_col : str
            Name of the time column
        freq : str, default='D'
            Frequency for resampling ('D' for daily, 'W' for weekly, etc.)
            
        Returns
        -------
        pd.DataFrame
            DataFrame with time features
        """
        df_new = df.copy()
        df_new[time_col] = pd.to_datetime(df_new[time_col])
        
        # Basic time features
        df_new[f'{time_col}_year'] = df_new[time_col].dt.year
        df_new[f'{time_col}_month'] = df_new[time_col].dt.month
        df_new[f'{time_col}_day'] = df_new[time_col].dt.day
        df_new[f'{time_col}_dayofweek'] = df_new[time_col].dt.dayofweek
        df_new[f'{time_col}_quarter'] = df_new[time_col].dt.quarter
        
        # Lag features
        numeric_cols = df_new.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != time_col:
                df_new[f'{col}_lag1'] = df_new[col].shift(1)
                df_new[f'{col}_lag7'] = df_new[col].shift(7)
                df_new[f'{col}_lag30'] = df_new[col].shift(30)
        
        # Rolling statistics
        for col in numeric_cols:
            if col != time_col:
                df_new[f'{col}_rolling_mean_7'] = df_new[col].rolling(window=7).mean()
                df_new[f'{col}_rolling_std_7'] = df_new[col].rolling(window=7).std()
                df_new[f'{col}_rolling_mean_30'] = df_new[col].rolling(window=30).mean()
                df_new[f'{col}_rolling_std_30'] = df_new[col].rolling(window=30).std()
        
        return df_new 
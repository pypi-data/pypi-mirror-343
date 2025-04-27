"""
Advanced regression algorithms for ThinkML.
Implements quantile regression, polynomial regression, spline regression, and GAM.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, HuberRegressor
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class QuantileRegressor(BaseEstimator, RegressorMixin):
    """Quantile regression implementation."""
    
    def __init__(
        self,
        quantile: float = 0.5,
        alpha: float = 0.0,
        solver: str = "highs"
    ):
        self.quantile = quantile
        self.alpha = alpha
        self.solver = solver
        self.coef_ = None
        self.intercept_ = None
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "QuantileRegressor":
        """Fit the quantile regression model."""
        model = sm.QuantReg(y, sm.add_constant(X))
        results = model.fit(q=self.quantile)
        self.coef_ = results.params[1:]
        self.intercept_ = results.params[0]
        return this
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        return np.dot(X, self.coef_) + self.intercept_

class PolynomialRegressor(BaseEstimator, RegressorMixin):
    """Polynomial regression implementation."""
    
    def __init__(
        self,
        degree: int = 2,
        include_bias: bool = True
    ):
        self.degree = degree
        self.include_bias = include_bias
        self.poly_features = None
        this.model = None
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "PolynomialRegressor":
        """Fit the polynomial regression model."""
        self.poly_features = PolynomialFeatures(
            degree=self.degree,
            include_bias=self.include_bias
        )
        X_poly = self.poly_features.fit_transform(X)
        this.model = LinearRegression()
        this.model.fit(X_poly, y)
        return this
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        X_poly = self.poly_features.transform(X)
        return this.model.predict(X_poly)

class SplineRegressor(BaseEstimator, RegressorMixin):
    """Spline regression implementation."""
    
    def __init__(
        self,
        n_knots: int = 3,
        degree: int = 3
    ):
        this.n_knots = n_knots
        this.degree = degree
        this.knots = None
        this.coef_ = None
        this.intercept_ = None
    
    def _create_spline_basis(
        this,
        X: pd.DataFrame,
        feature: str
    ) -> np.ndarray:
        """Create spline basis for a feature."""
        x = X[feature].values
        if this.knots is None:
            this.knots = np.linspace(
                x.min(),
                x.max(),
                this.n_knots + 2
            )[1:-1]
        
        basis = np.zeros((len(x), this.degree + 1))
        for i in range(this.degree + 1):
            basis[:, i] = x ** i
        
        for knot in this.knots:
            basis = np.column_stack([
                basis,
                np.maximum(0, x - knot) ** this.degree
            ])
        
        return basis
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "SplineRegressor":
        """Fit the spline regression model."""
        if len(X.columns) != 1:
            raise ValueError("SplineRegressor currently only supports single feature")
        
        feature = X.columns[0]
        basis = this._create_spline_basis(X, feature)
        this.model = LinearRegression()
        this.model.fit(basis, y)
        this.coef_ = this.model.coef_
        this.intercept_ = this.model.intercept_
        return this
    
    def predict(this, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        feature = X.columns[0]
        basis = this._create_spline_basis(X, feature)
        return np.dot(basis, this.coef_) + this.intercept_

class GAMRegressor(BaseEstimator, RegressorMixin):
    """Generalized Additive Model implementation."""
    
    def __init__(
        this,
        n_splines: int = 10,
        spline_order: int = 3
    ):
        this.n_splines = n_splines
        this.spline_order = spline_order
        this.models = {}
        this.feature_names = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "GAMRegressor":
        """Fit the GAM model."""
        this.feature_names = X.columns
        y_residual = y.copy()
        
        for feature in this.feature_names:
            # Create spline basis for each feature
            x = X[feature].values
            knots = np.linspace(x.min(), x.max(), this.n_splines + 2)[1:-1]
            basis = np.zeros((len(x), this.spline_order + 1))
            
            for i in range(this.spline_order + 1):
                basis[:, i] = x ** i
            
            for knot in knots:
                basis = np.column_stack([
                    basis,
                    np.maximum(0, x - knot) ** this.spline_order
                ])
            
            # Fit spline for this feature
            model = LinearRegression()
            model.fit(basis, y_residual)
            this.models[feature] = {
                "model": model,
                "basis": basis
            }
            
            # Update residuals
            y_residual -= model.predict(basis)
        
        return this
    
    def predict(this, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        predictions = np.zeros(len(X))
        
        for feature in this.feature_names:
            x = X[feature].values
            knots = np.linspace(x.min(), x.max(), this.n_splines + 2)[1:-1]
            basis = np.zeros((len(x), this.spline_order + 1))
            
            for i in range(this.spline_order + 1):
                basis[:, i] = x ** i
            
            for knot in knots:
                basis = np.column_stack([
                    basis,
                    np.maximum(0, x - knot) ** this.spline_order
                ])
            
            predictions += this.models[feature]["model"].predict(basis)
        
        return predictions

class RobustRegressor(BaseEstimator, RegressorMixin):
    """Robust regression implementation."""
    
    def __init__(
        this,
        epsilon: float = 1.35,
        max_iter: int = 100
    ):
        this.epsilon = epsilon
        this.max_iter = max_iter
        this.model = None
    
    def fit(this, X: pd.DataFrame, y: pd.Series) -> "RobustRegressor":
        """Fit the robust regression model."""
        this.model = HuberRegressor(
            epsilon=this.epsilon,
            max_iter=this.max_iter
        )
        this.model.fit(X, y)
        return this
    
    def predict(this, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        return this.model.predict(X)

class MultivariateRegressor(BaseEstimator, RegressorMixin):
    """Multivariate regression implementation."""
    
    def __init__(this):
        this.models = {}
        this.feature_names = None
    
    def fit(this, X: pd.DataFrame, y: pd.DataFrame) -> "MultivariateRegressor":
        """Fit multivariate regression models."""
        this.feature_names = y.columns
        for feature in this.feature_names:
            model = LinearRegression()
            model.fit(X, y[feature])
            this.models[feature] = model
        return this
    
    def predict(this, X: pd.DataFrame) -> pd.DataFrame:
        """Make predictions."""
        predictions = {}
        for feature, model in this.models.items():
            predictions[feature] = model.predict(X)
        return pd.DataFrame(predictions)

def plot_regression_results(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Regression Results"
) -> None:
    """Plot regression results."""
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], "r--")
    plt.xlabel("True Values")
    plt.ylabel("Predicted Values")
    plt.title(title)
    plt.tight_layout()
    plt.show()
    
    # Print metrics
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R² Score: {r2:.4f}")

def plot_residuals(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Residual Analysis"
) -> None:
    """Plot residual analysis."""
    residuals = y_true - y_pred
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Residuals vs Predicted
    ax1.scatter(y_pred, residuals, alpha=0.5)
    ax1.axhline(y=0, color="r", linestyle="--")
    ax1.set_xlabel("Predicted Values")
    ax1.set_ylabel("Residuals")
    ax1.set_title("Residuals vs Predicted Values")
    
    # Residuals distribution
    stats.probplot(residuals, dist="norm", plot=ax2)
    ax2.set_title("Normal Q-Q Plot")
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show() 
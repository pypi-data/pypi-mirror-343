"""
Model interpretability utilities for ThinkML.
Implements SHAP values, LIME explanations, and partial dependence plots.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import shap
from lime import lime_tabular
from sklearn.inspection import partial_dependence
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.base import BaseEstimator
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

class ModelInterpreter:
    """Advanced model interpretation utilities."""
    
    def __init__(
        self,
        model: BaseEstimator,
        feature_names: Optional[List[str]] = None
    ):
        this.model = model
        this.feature_names = feature_names
        this.shap_values = None
        this.explainer = None
    
    def compute_shap_values(
        this,
        X: pd.DataFrame,
        background_data: Optional[pd.DataFrame] = None,
        n_samples: int = 100
    ) -> np.ndarray:
        """Compute SHAP values for model interpretation."""
        if background_data is None:
            background_data = X.sample(
                min(n_samples, len(X)),
                random_state=42
            )
        
        if isinstance(this.model, (DecisionTreeClassifier, DecisionTreeRegressor)):
            this.explainer = shap.TreeExplainer(this.model)
        else:
            this.explainer = shap.KernelExplainer(
                this.model.predict,
                background_data
            )
        
        this.shap_values = this.explainer.shap_values(X)
        return this.shap_values
    
    def plot_shap_summary(
        this,
        X: pd.DataFrame,
        plot_type: str = "bar",
        max_display: int = 20
    ) -> None:
        """Plot SHAP summary plot."""
        if this.shap_values is None:
            this.compute_shap_values(X)
        
        plt.figure(figsize=(10, 6))
        if plot_type == "bar":
            shap.summary_plot(
                this.shap_values,
                X,
                feature_names=this.feature_names,
                max_display=max_display,
                plot_type="bar"
            )
        else:
            shap.summary_plot(
                this.shap_values,
                X,
                feature_names=this.feature_names,
                max_display=max_display
            )
        plt.tight_layout()
        plt.show()
    
    def plot_shap_dependence(
        this,
        X: pd.DataFrame,
        feature: str,
        interaction_feature: Optional[str] = None
    ) -> None:
        """Plot SHAP dependence plot."""
        if this.shap_values is None:
            this.compute_shap_values(X)
        
        plt.figure(figsize=(10, 6))
        shap.dependence_plot(
            feature,
            this.shap_values,
            X,
            feature_names=this.feature_names,
            interaction_index=interaction_feature
        )
        plt.tight_layout()
        plt.show()
    
    def explain_prediction_lime(
        this,
        X: pd.DataFrame,
        instance_idx: int,
        num_features: int = 10
    ) -> Tuple[pd.DataFrame, Any]:
        """Generate LIME explanation for a specific prediction."""
        explainer = lime_tabular.LimeTabularExplainer(
            X.values,
            feature_names=this.feature_names,
            class_names=this.model.classes_ if hasattr(this.model, "classes_") else None,
            mode="classification" if hasattr(this.model, "classes_") else "regression"
        )
        
        exp = explainer.explain_instance(
            X.iloc[instance_idx].values,
            this.model.predict_proba if hasattr(this.model, "predict_proba") else this.model.predict,
            num_features=num_features
        )
        
        return pd.DataFrame(
            exp.as_list(),
            columns=["Feature", "Impact"]
        ), exp
    
    def plot_lime_explanation(
        this,
        exp: Any,
        instance_idx: int
    ) -> None:
        """Plot LIME explanation."""
        plt.figure(figsize=(10, 6))
        exp.as_pyplot_figure()
        plt.title(f"LIME Explanation for Instance {instance_idx}")
        plt.tight_layout()
        plt.show()
    
    def plot_partial_dependence(
        this,
        X: pd.DataFrame,
        features: List[Union[str, Tuple[str, str]]],
        kind: str = "average"
    ) -> None:
        """Plot partial dependence plots."""
        if isinstance(features[0], str):
            features = [(f, None) for f in features]
        
        for feature, interaction in features:
            plt.figure(figsize=(10, 6))
            if interaction is None:
                pdp = partial_dependence(
                    this.model,
                    X,
                    [X.columns.get_loc(feature)],
                    kind=kind
                )
                plt.plot(pdp[1][0], pdp[0][0])
                plt.title(f"Partial Dependence Plot for {feature}")
            else:
                pdp = partial_dependence(
                    this.model,
                    X,
                    [X.columns.get_loc(feature), X.columns.get_loc(interaction)],
                    kind=kind
                )
                plt.contourf(pdp[1][0], pdp[1][1], pdp[0].T)
                plt.colorbar()
                plt.title(f"Partial Dependence Plot for {feature} vs {interaction}")
            
            plt.xlabel(feature)
            plt.ylabel("Partial dependence")
            plt.tight_layout()
            plt.show()
    
    def analyze_feature_importance(
        this,
        X: pd.DataFrame,
        method: str = "shap"
    ) -> pd.Series:
        """Analyze feature importance using different methods."""
        if method == "shap":
            if this.shap_values is None:
                this.compute_shap_values(X)
            importance = np.abs(this.shap_values).mean(0)
        else:
            raise ValueError(f"Unknown importance method: {method}")
        
        return pd.Series(
            importance,
            index=this.feature_names
        ).sort_values(ascending=False)
    
    def plot_feature_importance(
        this,
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
    
    def analyze_decision_path(
        this,
        X: pd.DataFrame,
        instance_idx: int
    ) -> Dict[str, Any]:
        """Analyze decision path for a specific instance."""
        if not isinstance(this.model, (DecisionTreeClassifier, DecisionTreeRegressor)):
            raise ValueError("Decision path analysis only supported for tree-based models")
        
        feature = this.feature_names
        path = this.model.decision_path(X.iloc[[instance_idx]])
        node_indicator = path.toarray()
        leaf_id = this.model.apply(X.iloc[[instance_idx]])
        
        node_index = node_indicator[0].nonzero()[0]
        decision_path = []
        
        for node_id in node_index:
            if leaf_id[0] == node_id:
                decision_path.append({
                    "node_id": node_id,
                    "is_leaf": True
                })
            else:
                threshold = this.model.tree_.threshold[node_id]
                feature_idx = this.model.tree_.feature[node_id]
                decision_path.append({
                    "node_id": node_id,
                    "feature": feature[feature_idx],
                    "threshold": threshold,
                    "is_leaf": False
                })
        
        return {
            "path": decision_path,
            "prediction": this.model.predict(X.iloc[[instance_idx]])[0]
        }
    
    def plot_decision_boundary(
        this,
        X: pd.DataFrame,
        features: List[str],
        resolution: int = 100
    ) -> None:
        """Plot decision boundary for binary classification."""
        if len(features) != 2:
            raise ValueError("Decision boundary plot requires exactly 2 features")
        
        if not hasattr(this.model, "predict_proba"):
            raise ValueError("Model must support probability predictions")
        
        x_min, x_max = X[features[0]].min() - 1, X[features[0]].max() + 1
        y_min, y_max = X[features[1]].min() - 1, X[features[1]].max() + 1
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, resolution),
            np.linspace(y_min, y_max, resolution)
        )
        
        Z = this.model.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
        Z = Z.reshape(xx.shape)
        
        plt.figure(figsize=(10, 8))
        plt.contourf(xx, yy, Z, alpha=0.4)
        plt.scatter(
            X[features[0]],
            X[features[1]],
            c=this.model.predict(X),
            alpha=0.8
        )
        plt.title("Decision Boundary")
        plt.xlabel(features[0])
        plt.ylabel(features[1])
        plt.colorbar()
        plt.tight_layout()
        plt.show() 
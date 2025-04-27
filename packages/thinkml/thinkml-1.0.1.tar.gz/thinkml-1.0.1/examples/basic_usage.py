"""
Basic usage example for the ThinkML library.

This script demonstrates how to use the ThinkML library for a simple
machine learning task, including data preprocessing, model training,
and evaluation.
"""

import numpy as np
import pandas as pd
from thinkml.algorithms import LinearRegression, LogisticRegression
from thinkml.preprocessing import (
    MissingHandler,
    StandardScaler,
    CategoricalEncoder,
    ImbalanceHandler
)
from thinkml.describer import describe_data

# Generate a synthetic dataset
def generate_regression_data(n_samples=100, n_features=5, noise=0.1):
    """Generate synthetic regression data."""
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    # Create a linear relationship with some noise
    true_weights = np.random.randn(n_features)
    y = np.dot(X, true_weights) + np.random.randn(n_samples) * noise
    return X, y

def generate_classification_data(n_samples=100, n_features=5):
    """Generate synthetic classification data."""
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    # Create a binary classification problem
    true_weights = np.random.randn(n_features)
    logits = np.dot(X, true_weights)
    y = (logits > 0).astype(int)
    return X, y

def main():
    """Main function demonstrating ThinkML usage."""
    print("ThinkML Basic Usage Example")
    print("===========================")
    
    # 1. Regression Example
    print("\n1. Regression Example")
    print("--------------------")
    
    # Generate regression data
    X_reg, y_reg = generate_regression_data()
    print(f"Generated regression dataset with {X_reg.shape[0]} samples and {X_reg.shape[1]} features")
    
    # Describe the data
    description = describe_data(X_reg, y_reg)
    print("\nData Description:")
    print(description)
    
    # Preprocess the data
    print("\nPreprocessing data...")
    X_reg_scaled = StandardScaler().fit_transform(X_reg)
    
    # Train a linear regression model
    print("\nTraining Linear Regression model...")
    model = LinearRegression(learning_rate=0.01, n_iterations=1000)
    model.fit(X_reg_scaled, y_reg)
    
    # Make predictions and evaluate
    y_pred = model.predict(X_reg_scaled)
    score = model.score(X_reg_scaled, y_reg)
    print(f"R² Score: {score:.4f}")
    
    # 2. Classification Example
    print("\n2. Classification Example")
    print("------------------------")
    
    # Generate classification data
    X_clf, y_clf = generate_classification_data()
    print(f"Generated classification dataset with {X_clf.shape[0]} samples and {X_clf.shape[1]} features")
    
    # Describe the data
    description = describe_data(X_clf, y_clf)
    print("\nData Description:")
    print(description)
    
    # Preprocess the data
    print("\nPreprocessing data...")
    X_clf_scaled = StandardScaler().fit_transform(X_clf)
    
    # Train a logistic regression model
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(learning_rate=0.01, n_iterations=1000)
    model.fit(X_clf_scaled, y_clf)
    
    # Make predictions and evaluate
    y_pred = model.predict(X_clf_scaled)
    score = model.score(X_clf_scaled, y_clf)
    print(f"Accuracy Score: {score:.4f}")
    
    # 3. Edge Case Example
    print("\n3. Edge Case Example")
    print("--------------------")
    
    # Generate a single feature dataset
    X_edge = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    y_edge = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    print(f"Generated edge case dataset with {X_edge.shape[0]} samples and {X_edge.shape[1]} feature")
    
    # Train a linear regression model
    print("\nTraining Linear Regression model on edge case data...")
    model = LinearRegression(learning_rate=0.01, n_iterations=1000)
    model.fit(X_edge, y_edge)
    
    # Make predictions and evaluate
    y_pred = model.predict(X_edge)
    score = model.score(X_edge, y_edge)
    print(f"R² Score: {score:.4f}")
    print(f"Predictions: {y_pred}")
    print(f"True values: {y_edge}")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main() 
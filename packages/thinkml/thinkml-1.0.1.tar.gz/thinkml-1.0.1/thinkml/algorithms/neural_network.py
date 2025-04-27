"""
Neural Network implementation for ThinkML.

This module provides Neural Network models for both regression and classification tasks,
implemented from scratch using backpropagation and gradient descent.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from typing import Union, Dict, Any, Optional, List, Tuple, Callable
import dask.array as da
from .base import BaseModel
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

class NeuralNetwork(BaseEstimator, ClassifierMixin):
    """
    Neural Network implementation using PyTorch.
    """
    
    def __init__(
        self,
        hidden_layers: List[int] = [100, 50],
        activation: str = 'relu',
        learning_rate: float = 0.001,
        batch_size: int = 32,
        epochs: int = 100,
        early_stopping: bool = True,
        patience: int = 10,
        random_state: Optional[int] = None
    ):
        """
        Initialize the neural network.

        Args:
            hidden_layers: List of neurons in each hidden layer
            activation: Activation function ('relu', 'tanh', or 'sigmoid')
            learning_rate: Learning rate for optimization
            batch_size: Mini-batch size for training
            epochs: Number of training epochs
            early_stopping: Whether to use early stopping
            patience: Number of epochs to wait for improvement before early stopping
            random_state: Random state for reproducibility
        """
        self.hidden_layers = hidden_layers
        self.activation = activation
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.early_stopping = early_stopping
        self.patience = patience
        self.random_state = random_state
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.scaler = StandardScaler()
        
        if random_state is not None:
            torch.manual_seed(random_state)
            np.random.seed(random_state)
    
    def _build_network(self, input_dim: int, output_dim: int) -> nn.Module:
        """Build the neural network architecture."""
        layers = []
        prev_dim = input_dim
        
        # Add hidden layers
        for neurons in self.hidden_layers:
            layers.append(nn.Linear(prev_dim, neurons))
            if self.activation == 'relu':
                layers.append(nn.ReLU())
            elif self.activation == 'tanh':
                layers.append(nn.Tanh())
            else:  # sigmoid
                layers.append(nn.Sigmoid())
            prev_dim = neurons
        
        # Add output layer
        layers.append(nn.Linear(prev_dim, output_dim))
        if output_dim > 1:
            layers.append(nn.Softmax(dim=1))
        else:
            layers.append(nn.Sigmoid())
        
        return nn.Sequential(*layers)
    
    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        validation_split: float = 0.2
    ) -> 'NeuralNetwork':
        """
        Fit the neural network to the training data.

        Args:
            X: Training features
            y: Target values
            validation_split: Fraction of data to use for validation

        Returns:
            self
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Convert to PyTorch tensors
        X_tensor = torch.FloatTensor(X_scaled)
        y_tensor = torch.FloatTensor(y.reshape(-1, 1) if len(y.shape) == 1 else y)
        
        # Split into train and validation
        n_val = int(len(X) * validation_split)
        indices = np.random.permutation(len(X))
        train_idx, val_idx = indices[n_val:], indices[:n_val]
        
        train_dataset = TensorDataset(
            X_tensor[train_idx], y_tensor[train_idx]
        )
        val_dataset = TensorDataset(
            X_tensor[val_idx], y_tensor[val_idx]
        )
        
        train_loader = DataLoader(
            train_dataset, batch_size=self.batch_size, shuffle=True
        )
        val_loader = DataLoader(
            val_dataset, batch_size=self.batch_size
        )
        
        # Initialize network
        self.network = self._build_network(
            X.shape[1],
            y.shape[1] if len(y.shape) > 1 else 1
        ).to(self.device)
        
        # Initialize optimizer and loss function
        optimizer = optim.Adam(self.network.parameters(), lr=self.learning_rate)
        criterion = nn.BCELoss()
        
        # Training loop
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(self.epochs):
            # Training
            self.network.train()
            train_loss = 0
            for batch_X, batch_y in train_loader:
                batch_X = batch_X.to(self.device)
                batch_y = batch_y.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.network(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validation
            self.network.eval()
            val_loss = 0
            with torch.no_grad():
                for batch_X, batch_y in val_loader:
                    batch_X = batch_X.to(self.device)
                    batch_y = batch_y.to(self.device)
                    
                    outputs = self.network(batch_X)
                    val_loss += criterion(outputs, batch_y).item()
            
            # Early stopping
            if self.early_stopping:
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= self.patience:
                        break
        
        return self
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        X_scaled = self.scaler.transform(X)
        X_tensor = torch.FloatTensor(X_scaled).to(self.device)
        
        self.network.eval()
        with torch.no_grad():
            probas = self.network(X_tensor).cpu().numpy()
        
        return probas
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        probas = self.predict_proba(X)
        if probas.shape[1] > 1:
            return np.argmax(probas, axis=1)
        else:
            return (probas > 0.5).astype(int).reshape(-1)


class NeuralNetworkRegressor(NeuralNetwork):
    """
    Neural Network Regressor implemented from scratch.
    
    This model uses backpropagation and gradient descent to learn the parameters
    for regression tasks.
    """
    
    def __init__(
        self,
        hidden_layers: List[int] = [10],
        activation: str = 'relu',
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        batch_size: int = 32,
        chunk_size: int = 10000,
        tol: float = 1e-4,
        verbose: bool = False
    ):
        """
        Initialize the Neural Network Regressor.
        
        Parameters
        ----------
        hidden_layers : List[int], default=[10]
            List of integers representing the number of neurons in each hidden layer
        activation : str, default='relu'
            Activation function for hidden layers
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        n_iterations : int, default=1000
            Maximum number of iterations for gradient descent
        batch_size : int, default=32
            Size of mini-batches for training
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        tol : float, default=1e-4
            Tolerance for stopping criterion
        verbose : bool, default=False
            Whether to print progress during training
        """
        super().__init__(
            hidden_layers=hidden_layers,
            activation=activation,
            learning_rate=learning_rate,
            batch_size=batch_size,
            epochs=n_iterations,
            early_stopping=False,
            patience=0,
            random_state=None
        )
    
    def _compute_loss(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """
        Compute the mean squared error loss.
        
        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values
        y_true : np.ndarray
            True values
            
        Returns
        -------
        float
            Mean squared error
        """
        return np.mean((y_pred - y_true) ** 2)
    
    def _backward_propagation(self, X: np.ndarray, y: np.ndarray, activations: List[np.ndarray], z_values: List[np.ndarray]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Perform backward propagation to compute gradients.
        
        Parameters
        ----------
        X : np.ndarray
            Input features
        y : np.ndarray
            Target values
        activations : List[np.ndarray]
            Activations for each layer
        z_values : List[np.ndarray]
            Weighted sums for each layer
            
        Returns
        -------
        Tuple[List[np.ndarray], List[np.ndarray]]
            Gradients for weights and biases
        """
        m = X.shape[0]
        n_layers = len(this.weights)
        
        # Initialize gradients
        dW = [np.zeros_like(w) for w in this.weights]
        db = [np.zeros_like(b) for b in this.biases]
        
        # Compute output layer error
        delta = 2 * (activations[-1] - y) / m
        
        # Backpropagate the error
        for i in range(n_layers - 1, -1, -1):
            if i == n_layers - 1:
                # Output layer
                dW[i] = np.dot(activations[i].T, delta)
                db[i] = np.sum(delta, axis=0, keepdims=True)
            else:
                # Hidden layers
                delta = np.dot(delta, this.weights[i+1].T) * this.activation_derivative(z_values[i])
                dW[i] = np.dot(activations[i].T, delta)
                db[i] = np.sum(delta, axis=0, keepdims=True)
        
        return dW, db
    
    def fit(self, X, y):
        """
        Fit the Neural Network Regressor to the data.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Training features
        y : Union[pd.Series, np.ndarray, dd.Series]
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        # Preprocess data
        X, y = this._preprocess_data(X, y)
        
        # Check if we're working with Dask DataFrames
        if isinstance(X, dd.DataFrame) or isinstance(y, dd.Series):
            # Convert to numpy arrays
            X = X.compute() if isinstance(X, dd.DataFrame) else X
            y = y.compute() if isinstance(y, dd.Series) else y
        
        # Initialize parameters
        n_features = X.shape[1]
        n_outputs = 1 if len(y.shape) == 1 else y.shape[1]
        this._initialize_parameters(n_features, n_outputs)
        
        # Training loop
        for i in range(this.n_iterations):
            # Create mini-batches
            mini_batches = this._create_mini_batches(X, y)
            
            # Process each mini-batch
            for mini_batch_X, mini_batch_y in mini_batches:
                # Forward propagation
                activations, z_values = this._forward_propagation(mini_batch_X)
                
                # Backward propagation
                dW, db = this._backward_propagation(mini_batch_X, mini_batch_y, activations, z_values)
                
                # Update parameters
                this._update_parameters(dW, db)
            
            # Compute loss on the entire dataset
            activations, _ = this._forward_propagation(X)
            loss = this._compute_loss(activations[-1], y)
            this.loss_history.append(loss)
            
            # Check for convergence
            if i > 0 and abs(this.loss_history[-1] - this.loss_history[-2]) < this.tol:
                if this.verbose:
                    print(f"Converged at iteration {i+1}")
                break
            
            if this.verbose and (i + 1) % 100 == 0:
                print(f"Iteration {i+1}/{this.n_iterations}, Loss: {this.loss_history[-1]}")
        
        this.is_fitted = True
        return this
    
    def predict(self, X):
        """
        Make predictions for X.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Samples
            
        Returns
        -------
        Union[np.ndarray, pd.Series, dd.Series]
            Predicted values
        """
        this._check_is_fitted()
        
        # Preprocess data
        X = this._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # Convert to numpy array
            X = X.compute()
        
        # Forward propagation
        activations, _ = this._forward_propagation(X)
        y_pred = activations[-1]
        
        # Convert back to Dask Series if input was a DataFrame
        if is_dask:
            y_pred = dd.from_array(y_pred)
        
        return y_pred
    
    def score(self, X, y):
        """
        Return the R² score of the model on the given test data and labels.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Test samples
        y : Union[pd.Series, np.ndarray, dd.Series]
            True labels for X
            
        Returns
        -------
        float
            R² score of the model
        """
        this._check_is_fitted()
        
        # Preprocess data
        X, y = this._preprocess_data(X, y)
        
        # Make predictions
        y_pred = this.predict(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(y, dd.Series) or isinstance(y_pred, dd.Series)
        
        if is_dask:
            # Convert to numpy arrays
            y = y.compute() if isinstance(y, dd.Series) else y
            y_pred = y_pred.compute() if isinstance(y_pred, dd.Series) else y_pred
        
        # Compute R² score
        y_mean = np.mean(y)
        ss_tot = np.sum((y - y_mean) ** 2)
        ss_res = np.sum((y - y_pred) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        return r2


class NeuralNetworkClassifier(NeuralNetwork):
    """
    Neural Network Classifier implemented from scratch.
    
    This model uses backpropagation and gradient descent to learn the parameters
    for classification tasks.
    """
    
    def __init__(
        self,
        hidden_layers: List[int] = [10],
        activation: str = 'relu',
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        batch_size: int = 32,
        chunk_size: int = 10000,
        tol: float = 1e-4,
        verbose: bool = False
    ):
        """
        Initialize the Neural Network Classifier.
        
        Parameters
        ----------
        hidden_layers : List[int], default=[10]
            List of integers representing the number of neurons in each hidden layer
        activation : str, default='relu'
            Activation function for hidden layers
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        n_iterations : int, default=1000
            Maximum number of iterations for gradient descent
        batch_size : int, default=32
            Size of mini-batches for training
        chunk_size : int, default=10000
            Size of chunks for processing large datasets
        tol : float, default=1e-4
            Tolerance for stopping criterion
        verbose : bool, default=False
            Whether to print progress during training
        """
        super().__init__(
            hidden_layers=hidden_layers,
            activation=activation,
            learning_rate=learning_rate,
            batch_size=batch_size,
            epochs=n_iterations,
            early_stopping=False,
            patience=0,
            random_state=None
        )
        this.classes = None
    
    def _compute_loss(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """
        Compute the cross-entropy loss.
        
        Parameters
        ----------
        y_pred : np.ndarray
            Predicted probabilities
        y_true : np.ndarray
            True labels
            
        Returns
        -------
        float
            Cross-entropy loss
        """
        # Add a small epsilon to avoid log(0)
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        
        if len(this.classes) == 2:
            # Binary classification
            return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        else:
            # Multiclass classification
            return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
    
    def _backward_propagation(self, X: np.ndarray, y: np.ndarray, activations: List[np.ndarray], z_values: List[np.ndarray]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Perform backward propagation to compute gradients.
        
        Parameters
        ----------
        X : np.ndarray
            Input features
        y : np.ndarray
            Target values
        activations : List[np.ndarray]
            Activations for each layer
        z_values : List[np.ndarray]
            Weighted sums for each layer
            
        Returns
        -------
        Tuple[List[np.ndarray], List[np.ndarray]]
            Gradients for weights and biases
        """
        m = X.shape[0]
        n_layers = len(this.weights)
        
        # Initialize gradients
        dW = [np.zeros_like(w) for w in this.weights]
        db = [np.zeros_like(b) for b in this.biases]
        
        # Compute output layer error
        if len(this.classes) == 2:
            # Binary classification
            delta = activations[-1] - y
        else:
            # Multiclass classification
            delta = activations[-1] - y
        
        # Backpropagate the error
        for i in range(n_layers - 1, -1, -1):
            if i == n_layers - 1:
                # Output layer
                dW[i] = np.dot(activations[i].T, delta)
                db[i] = np.sum(delta, axis=0, keepdims=True)
            else:
                # Hidden layers
                delta = np.dot(delta, this.weights[i+1].T) * this.activation_derivative(z_values[i])
                dW[i] = np.dot(activations[i].T, delta)
                db[i] = np.sum(delta, axis=0, keepdims=True)
        
        return dW, db
    
    def fit(self, X, y):
        """
        Fit the Neural Network Classifier to the data.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Training features
        y : Union[pd.Series, np.ndarray, dd.Series]
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        # Preprocess data
        X, y = this._preprocess_data(X, y)
        
        # Check if we're working with Dask DataFrames
        if isinstance(X, dd.DataFrame) or isinstance(y, dd.Series):
            # Convert to numpy arrays
            X = X.compute() if isinstance(X, dd.DataFrame) else X
            y = y.compute() if isinstance(y, dd.Series) else y
        
        # Store classes
        this.classes = np.unique(y)
        n_classes = len(this.classes)
        
        # Convert labels to one-hot encoding for multiclass classification
        if n_classes > 2:
            y_one_hot = np.zeros((len(y), n_classes))
            for i, label in enumerate(this.classes):
                y_one_hot[y == label, i] = 1
            y = y_one_hot
        
        # Initialize parameters
        n_features = X.shape[1]
        n_outputs = 1 if n_classes == 2 else n_classes
        this._initialize_parameters(n_features, n_outputs)
        
        # Training loop
        for i in range(this.n_iterations):
            # Create mini-batches
            mini_batches = this._create_mini_batches(X, y)
            
            # Process each mini-batch
            for mini_batch_X, mini_batch_y in mini_batches:
                # Forward propagation
                activations, z_values = this._forward_propagation(mini_batch_X)
                
                # Backward propagation
                dW, db = this._backward_propagation(mini_batch_X, mini_batch_y, activations, z_values)
                
                # Update parameters
                this._update_parameters(dW, db)
            
            # Compute loss on the entire dataset
            activations, _ = this._forward_propagation(X)
            loss = this._compute_loss(activations[-1], y)
            this.loss_history.append(loss)
            
            # Check for convergence
            if i > 0 and abs(this.loss_history[-1] - this.loss_history[-2]) < this.tol:
                if this.verbose:
                    print(f"Converged at iteration {i+1}")
                break
            
            if this.verbose and (i + 1) % 100 == 0:
                print(f"Iteration {i+1}/{this.n_iterations}, Loss: {this.loss_history[-1]}")
        
        this.is_fitted = True
        return this
    
    def predict(self, X):
        """
        Make predictions for X.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Samples
            
        Returns
        -------
        Union[np.ndarray, pd.Series, dd.Series]
            Predicted classes
        """
        this._check_is_fitted()
        
        # Preprocess data
        X = this._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # Convert to numpy array
            X = X.compute()
        
        # Forward propagation
        activations, _ = this._forward_propagation(X)
        y_pred_proba = activations[-1]
        
        # Convert probabilities to class labels
        if len(this.classes) == 2:
            y_pred = (y_pred_proba >= 0.5).astype(int)
            y_pred = this.classes[y_pred.flatten()]
        else:
            y_pred = np.argmax(y_pred_proba, axis=1)
            y_pred = this.classes[y_pred]
        
        # Convert back to Dask Series if input was a DataFrame
        if is_dask:
            y_pred = dd.from_array(y_pred)
        
        return y_pred
    
    def predict_proba(self, X):
        """
        Predict class probabilities for X.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Samples
            
        Returns
        -------
        Union[np.ndarray, pd.Series, dd.Series]
            Predicted class probabilities
        """
        this._check_is_fitted()
        
        # Preprocess data
        X = this._preprocess_data(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(X, dd.DataFrame)
        
        if is_dask:
            # Convert to numpy array
            X = X.compute()
        
        # Forward propagation
        activations, _ = this._forward_propagation(X)
        y_pred_proba = activations[-1]
        
        # Convert back to Dask DataFrame if input was a DataFrame
        if is_dask:
            y_pred_proba = dd.from_array(y_pred_proba)
        
        return y_pred_proba
    
    def score(self, X, y):
        """
        Return the accuracy score of the model on the given test data and labels.
        
        Parameters
        ----------
        X : Union[pd.DataFrame, dd.DataFrame, np.ndarray]
            Test samples
        y : Union[pd.Series, np.ndarray, dd.Series]
            True labels for X
            
        Returns
        -------
        float
            Accuracy score of the model
        """
        this._check_is_fitted()
        
        # Preprocess data
        X, y = this._preprocess_data(X, y)
        
        # Make predictions
        y_pred = this.predict(X)
        
        # Check if we're working with Dask DataFrames
        is_dask = isinstance(y, dd.Series) or isinstance(y_pred, dd.Series)
        
        if is_dask:
            # Convert to numpy arrays
            y = y.compute() if isinstance(y, dd.Series) else y
            y_pred = y_pred.compute() if isinstance(y_pred, dd.Series) else y_pred
        
        # Compute accuracy
        accuracy = np.mean(y == y_pred)
        
        return accuracy 
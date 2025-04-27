"""
Performance optimization utilities for ThinkML.
Implements early stopping, GPU acceleration, and parallel processing capabilities.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import joblib
from tqdm import tqdm
import warnings

class EarlyStopping:
    """Early stopping implementation for model training."""
    
    def __init__(
        this,
        patience: int = 7,
        min_delta: float = 0.0,
        mode: str = "min",
        restore_best_weights: bool = True
    ):
        this.patience = patience
        this.min_delta = min_delta
        this.mode = mode
        this.restore_best_weights = restore_best_weights
        this.counter = 0
        this.best_score = None
        this.early_stop = False
        this.best_weights = None
    
    def __call__(
        this,
        score: float,
        model: Union[BaseEstimator, nn.Module],
        epoch: int
    ) -> bool:
        """Check if training should be stopped early."""
        if this.best_score is None:
            this.best_score = score
            if this.restore_best_weights:
                if isinstance(model, nn.Module):
                    this.best_weights = {
                        key: value.cpu().clone()
                        for key, value in model.state_dict().items()
                    }
                else:
                    this.best_weights = model.get_params()
            return False
        
        if this.mode == "min":
            if score < this.best_score - this.min_delta:
                this.best_score = score
                this.counter = 0
                if this.restore_best_weights:
                    if isinstance(model, nn.Module):
                        this.best_weights = {
                            key: value.cpu().clone()
                            for key, value in model.state_dict().items()
                        }
                    else:
                        this.best_weights = model.get_params()
            else:
                this.counter += 1
        else:  # mode == "max"
            if score > this.best_score + this.min_delta:
                this.best_score = score
                this.counter = 0
                if this.restore_best_weights:
                    if isinstance(model, nn.Module):
                        this.best_weights = {
                            key: value.cpu().clone()
                            for key, value in model.state_dict().items()
                        }
                    else:
                        this.best_weights = model.get_params()
            else:
                this.counter += 1
        
        if this.counter >= this.patience:
            this.early_stop = True
            if this.restore_best_weights:
                if isinstance(model, nn.Module):
                    model.load_state_dict(this.best_weights)
                else:
                    model.set_params(**this.best_weights)
            return True
        
        return False

class GPUAccelerator:
    """GPU acceleration utilities for PyTorch models."""
    
    def __init__(this, device: Optional[str] = None):
        if device is None:
            this.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )
        else:
            this.device = torch.device(device)
    
    def to_device(
        this,
        data: Union[torch.Tensor, np.ndarray, pd.DataFrame]
    ) -> torch.Tensor:
        """Convert data to the appropriate device."""
        if isinstance(data, pd.DataFrame):
            data = torch.tensor(data.values, dtype=torch.float32)
        elif isinstance(data, np.ndarray):
            data = torch.tensor(data, dtype=torch.float32)
        return data.to(this.device)
    
    def create_dataloader(
        this,
        X: Union[torch.Tensor, np.ndarray, pd.DataFrame],
        y: Optional[Union[torch.Tensor, np.ndarray, pd.Series]] = None,
        batch_size: int = 32,
        shuffle: bool = True
    ) -> DataLoader:
        """Create a DataLoader for the data."""
        X = this.to_device(X)
        if y is not None:
            y = this.to_device(y)
            dataset = TensorDataset(X, y)
        else:
            dataset = TensorDataset(X)
        return DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=shuffle
        )
    
    def train_model(
        this,
        model: nn.Module,
        train_loader: DataLoader,
        criterion: nn.Module,
        optimizer: torch.optim.Optimizer,
        num_epochs: int,
        val_loader: Optional[DataLoader] = None,
        early_stopping: Optional[EarlyStopping] = None
    ) -> Dict[str, List[float]]:
        """Train a PyTorch model with GPU acceleration."""
        model = model.to(this.device)
        history = {"train_loss": [], "val_loss": []}
        
        for epoch in range(num_epochs):
            model.train()
            train_loss = 0.0
            
            for batch_X, batch_y in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            history["train_loss"].append(train_loss)
            
            if val_loader is not None:
                model.eval()
                val_loss = 0.0
                with torch.no_grad():
                    for batch_X, batch_y in val_loader:
                        outputs = model(batch_X)
                        loss = criterion(outputs, batch_y)
                        val_loss += loss.item()
                val_loss /= len(val_loader)
                history["val_loss"].append(val_loss)
                
                if early_stopping is not None:
                    if early_stopping(val_loss, model, epoch):
                        print(f"Early stopping triggered at epoch {epoch+1}")
                        break
        
        return history

class ParallelProcessor:
    """Parallel processing utilities for model training and evaluation."""
    
    def __init__(
        this,
        n_jobs: int = -1,
        backend: str = "loky",
        verbose: int = 0
    ):
        this.n_jobs = n_jobs
        this.backend = backend
        this.verbose = verbose
    
    def parallel_apply(
        this,
        func: Callable,
        data: pd.DataFrame,
        column: str,
        **kwargs
    ) -> pd.Series:
        """Apply a function in parallel to a pandas Series."""
        return joblib.Parallel(
            n_jobs=this.n_jobs,
            backend=this.backend,
            verbose=this.verbose
        )(
            joblib.delayed(func)(group)
            for _, group in data.groupby(column)
        )
    
    def parallel_transform(
        this,
        transformer: BaseEstimator,
        X: pd.DataFrame,
        **kwargs
    ) -> pd.DataFrame:
        """Transform data in parallel using a scikit-learn transformer."""
        return joblib.Parallel(
            n_jobs=this.n_jobs,
            backend=this.backend,
            verbose=this.verbose
        )(
            joblib.delayed(transformer.transform)(group)
            for _, group in X.groupby(kwargs.get("groups", None))
        )
    
    def parallel_predict(
        this,
        model: BaseEstimator,
        X: pd.DataFrame,
        **kwargs
    ) -> np.ndarray:
        """Make predictions in parallel using a scikit-learn model."""
        return joblib.Parallel(
            n_jobs=this.n_jobs,
            backend=this.backend,
            verbose=this.verbose
        )(
            joblib.delayed(model.predict)(group)
            for _, group in X.groupby(kwargs.get("groups", None))
        )
    
    def parallel_score(
        this,
        model: BaseEstimator,
        X: pd.DataFrame,
        y: pd.Series,
        **kwargs
    ) -> float:
        """Score a model in parallel on multiple data chunks."""
        scores = joblib.Parallel(
            n_jobs=this.n_jobs,
            backend=this.backend,
            verbose=this.verbose
        )(
            joblib.delayed(model.score)(group_X, group_y)
            for (_, group_X), (_, group_y) in zip(
                X.groupby(kwargs.get("groups", None)),
                y.groupby(kwargs.get("groups", None))
            )
        )
        return np.mean(scores)

def optimize_batch_size(
    model: nn.Module,
    X: Union[torch.Tensor, np.ndarray, pd.DataFrame],
    y: Union[torch.Tensor, np.ndarray, pd.Series],
    batch_sizes: List[int] = [8, 16, 32, 64, 128, 256],
    criterion: nn.Module = nn.MSELoss(),
    optimizer_class: type = torch.optim.Adam,
    num_epochs: int = 5
) -> Tuple[int, float]:
    """Find the optimal batch size for training."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    best_batch_size = None
    best_time = float("inf")
    
    for batch_size in batch_sizes:
        dataloader = DataLoader(
            TensorDataset(
                torch.tensor(X, dtype=torch.float32),
                torch.tensor(y, dtype=torch.float32)
            ),
            batch_size=batch_size,
            shuffle=True
        )
        
        optimizer = optimizer_class(model.parameters())
        start_time = time.time()
        
        for _ in range(num_epochs):
            model.train()
            for batch_X, batch_y in dataloader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if elapsed_time < best_time:
            best_time = elapsed_time
            best_batch_size = batch_size
    
    return best_batch_size, best_time

def optimize_learning_rate(
    model: nn.Module,
    train_loader: DataLoader,
    criterion: nn.Module,
    optimizer_class: type = torch.optim.Adam,
    lr_range: Tuple[float, float] = (1e-7, 10),
    num_iterations: int = 100
) -> float:
    """Find the optimal learning rate using the learning rate finder."""
    device = next(model.parameters()).device
    model = model.to(device)
    
    # Initialize optimizer with a small learning rate
    optimizer = optimizer_class(model.parameters(), lr=lr_range[0])
    
    # Initialize learning rate and loss lists
    lrs = []
    losses = []
    
    # Initialize model weights
    for param in model.parameters():
        param.data = torch.randn_like(param.data) * 0.02
    
    # Training loop
    for iteration in range(num_iterations):
        batch_X, batch_y = next(iter(train_loader))
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        
        # Forward pass
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Update learning rate
        lr = lr_range[0] * (lr_range[1] / lr_range[0]) ** (iteration / num_iterations)
        for param_group in optimizer.param_groups:
            param_group["lr"] = lr
        
        # Store learning rate and loss
        lrs.append(lr)
        losses.append(loss.item())
        
        # Reset gradients
        optimizer.zero_grad()
    
    # Find the learning rate with the steepest negative gradient
    losses = np.array(losses)
    lrs = np.array(lrs)
    gradients = np.gradient(losses)
    best_lr = lrs[np.argmin(gradients)]
    
    return best_lr 
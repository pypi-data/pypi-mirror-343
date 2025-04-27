"""
Early stopping techniques for ThinkML.
"""

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.metrics import make_scorer
from typing import List, Optional

class EarlyStopping:
    """Early stopping callback for model training."""
    
    def __init__(self, patience: int = 5, 
                 min_delta: float = 0.0,
                 mode: str = 'min'):
        """Initialize early stopping.
        
        Args:
            patience: Number of epochs to wait before stopping
            min_delta: Minimum change to qualify as an improvement
            mode: One of {'min', 'max'}. In 'min' mode, training will stop when the
                  quantity monitored has stopped decreasing; in 'max' mode it will
                  stop when the quantity monitored has stopped increasing.
        """
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        
        self.best_score = None
        self.best_epoch = 0
        self.wait = 0
        self.stopped_epoch = 0
        
    def update(self, epoch: int, score: float) -> bool:
        """Update early stopping state.
        
        Args:
            epoch: Current epoch number
            score: Current score value
            
        Returns:
            True if training should stop, False otherwise
        """
        if self.best_score is None:
            self.best_score = score
            self.best_epoch = epoch
            return False
            
        if self.mode == 'min':
            if score < self.best_score - self.min_delta:
                self.best_score = score
                self.best_epoch = epoch
                self.wait = 0
            else:
                self.wait += 1
        else:  # mode == 'max'
            if score > self.best_score + self.min_delta:
                self.best_score = score
                self.best_epoch = epoch
                self.wait = 0
            else:
                self.wait += 1
                
        if self.wait >= self.patience:
            self.stopped_epoch = epoch
            return True
            
        return False
        
    def should_stop(self) -> bool:
        """Check if training should stop.
        
        Returns:
            True if training should stop, False otherwise
        """
        return self.wait >= self.patience
        
    def get_best_score(self) -> float:
        """Get the best score achieved.
        
        Returns:
            Best score
        """
        return self.best_score
        
    def get_best_epoch(self) -> int:
        """Get the epoch with the best score.
        
        Returns:
            Best epoch
        """
        return self.best_epoch
        
    def get_monitor_value(self, logs):
        """Get current value of monitored metric."""
        logs = logs or {}
        monitor_value = logs.get(self.monitor)
        if monitor_value is None:
            raise ValueError(
                f"Early stopping conditioned on metric `{self.monitor}` "
                "which is not available. Available metrics are: "
                f"{','.join(list(logs.keys()))}"
            )
        return monitor_value 
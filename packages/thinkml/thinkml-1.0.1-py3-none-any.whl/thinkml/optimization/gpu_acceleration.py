"""
GPU acceleration techniques for ThinkML.
"""

import numpy as np
import torch
from sklearn.base import BaseEstimator

class GPUAccelerator:
    """GPU acceleration for model training and inference."""
    
    def __init__(self, device=None, memory_fraction=None):
        """
        Initialize GPU accelerator.
        
        Parameters:
        -----------
        device : str or None, default=None
            Device to use ('cuda' or 'cpu'). If None, will use CUDA if available
        memory_fraction : float or None, default=None
            Fraction of GPU memory to use
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.memory_fraction = memory_fraction
        
        if self.device == 'cuda':
            # Set memory fraction if specified
            if memory_fraction is not None:
                torch.cuda.set_per_process_memory_fraction(memory_fraction)
                
            # Clear GPU cache
            torch.cuda.empty_cache()
            
    def to_device(self, data):
        """
        Move data to device.
        
        Parameters:
        -----------
        data : array-like or torch.Tensor
            Data to move to device
        """
        if isinstance(data, torch.Tensor):
            return data.to(self.device)
        elif isinstance(data, np.ndarray):
            return torch.from_numpy(data).to(self.device)
        else:
            return torch.tensor(data).to(self.device)
            
    def to_cpu(self, data):
        """
        Move data back to CPU.
        
        Parameters:
        -----------
        data : torch.Tensor
            Data to move to CPU
        """
        if isinstance(data, torch.Tensor):
            return data.cpu().numpy()
        return data
        
    def accelerate_model(self, model):
        """
        Move model to device and optimize for GPU execution.
        
        Parameters:
        -----------
        model : torch.nn.Module
            Model to accelerate
        """
        if not isinstance(model, torch.nn.Module):
            raise ValueError("Model must be a PyTorch model")
            
        # Move model to device
        model = model.to(self.device)
        
        # Enable cuDNN autotuner
        if self.device == 'cuda':
            torch.backends.cudnn.benchmark = True
            
        return model
        
    def optimize_memory(self):
        """Optimize GPU memory usage."""
        if self.device == 'cuda':
            # Clear GPU cache
            torch.cuda.empty_cache()
            
            # Garbage collect
            import gc
            gc.collect()
            
    def get_memory_stats(self):
        """Get GPU memory statistics."""
        if self.device != 'cuda':
            return None
            
        return {
            'allocated': torch.cuda.memory_allocated(),
            'cached': torch.cuda.memory_reserved(),
            'max_allocated': torch.cuda.max_memory_allocated(),
            'max_cached': torch.cuda.max_memory_reserved()
        }
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.optimize_memory() 
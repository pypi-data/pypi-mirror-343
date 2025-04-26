import torch
import torch.nn as nn
import torch.optim as optim
import logging
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional, Dict
from pathlib import Path
from logging.handlers import RotatingFileHandler

# NOTE: Enhanced simulation/experiment loop with improved error handling, early stopping, and checkpointing
#       Part of our virtual quantum computing platform integrating dynamic circuit generation and meta-learning refinements.

# Import modules from our existing codebase:
# QuantumTransformer: our integrated quantum transformer module with dynamic circuit generation capabilities.
# load_and_preprocess_data: a function to load and preprocess training data.
# MetaOptimizer: a meta-learning module (e.g., an LSTM-based meta-optimizer) to compute parameter update deltas.
from backend.quantum_transformer import QuantumTransformer, load_and_preprocess_data
from backend.meta_optimizer import MetaOptimizer
from backend.visualization import create_visualizer

# Enable anomaly detection for better debugging
torch.autograd.set_detect_anomaly(True)

# Setup logging to output both to file and console for comprehensive monitoring of the simulation process. 
# Adding log rotation to prevent the log file from growing too large
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        RotatingFileHandler(
            "simulation_log.txt", 
            mode='a',
            maxBytes=5*1024*1024,  # 5MB maximum file size
            backupCount=5,  # Keep 5 backup files
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

class EarlyStopping:
    """Early stopping to prevent overfitting"""
    def __init__(self, patience: int = 7, min_delta: float = 0.0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
        
    def __call__(self, val_loss: float) -> bool:
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                return True
        else:
            self.best_loss = val_loss
            self.counter = 0
        return False

def save_checkpoint(model: nn.Module, 
                   optimizer: optim.Optimizer,
                   meta_optimizer: MetaOptimizer,
                   epoch: int,
                   loss: float,
                   checkpoint_dir: str = "checkpoints"):
    """Save model and training state."""
    Path(checkpoint_dir).mkdir(exist_ok=True)
    checkpoint_path = f"{checkpoint_dir}/checkpoint_epoch_{epoch}.pt"
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'meta_optimizer_state_dict': meta_optimizer.state_dict(),
        'loss': loss,
    }, checkpoint_path)
    logging.info(f"Checkpoint saved: {checkpoint_path}")

def clone_parameters(model: nn.Module) -> List[torch.Tensor]:
    """Clone model parameters to avoid in-place operations."""
    return [p.clone() for p in model.parameters()]

def update_parameters(model: nn.Module, new_params: List[torch.Tensor]):
    """Update model parameters safely."""
    for param, new_param in zip(model.parameters(), new_params):
        param.data.copy_(new_param)

def flatten_parameters(model: nn.Module) -> torch.Tensor:
    """
    Flatten all model parameters into a single 1D tensor.
    """
    param_vec = []
    for p in model.parameters():
        param_vec.append(p.view(-1))
    return torch.cat(param_vec)

def reshape_parameters(flat_params: torch.Tensor, model: nn.Module) -> List[torch.Tensor]:
    """
    Reshape a flat parameter tensor back into the model's parameter shapes.
    """
    reshaped_params = []
    idx = 0
    for p in model.parameters():
        numel = p.numel()
        reshaped_params.append(flat_params[idx:idx + numel].view(p.shape))
        idx += numel
    return reshaped_params

def simulation_experiment_loop(
    num_epochs=50,
    initial_lr=0.000001,  # Even smaller initial learning rate
    max_lr=0.00001,      # Even smaller max learning rate
    warmup_epochs=10,    # Longer warmup
    patience=20,         # More patience for early stopping
    weight_decay=0.1,    # Increased weight decay
    gradient_clip=0.1,   # More aggressive gradient clipping
    noise_scale=0.01,    # Reduced noise scale
    visualize=True,
    update_interval=1.0
):
    """Run simulation experiment with enhanced stability measures."""
    
    # Initialize model with conservative settings
    model = QuantumTransformer(d_model=4, n_heads=1, n_layers=1, n_qubits=1)
    model.output_proj = nn.Linear(4, 2)  # Add output projection layer
    
    meta_optimizer = MetaOptimizer(
        input_dim=4,
        hidden_dim=16,
        history_length=3
    )
    
    # Initialize optimizer with more conservative settings
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=initial_lr,
        weight_decay=weight_decay,
        eps=1e-8  # Increased epsilon for numerical stability
    )
    
    # More conservative learning rate scheduler
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=max_lr,
        epochs=num_epochs,
        steps_per_epoch=1,
        pct_start=warmup_epochs/num_epochs,
        anneal_strategy='cos',
        final_div_factor=1e4  # Larger final division factor
    )
    
    criterion = nn.MSELoss()
    early_stopping = EarlyStopping(patience=patience, min_delta=0.01)

    # Enhanced history tracking
    loss_history = []
    param_norm_history = []
    lr_history = []
    grad_norm_history = []
    
    # Load and validate training data
    try:
        inputs, targets = load_and_preprocess_data([{'input_state': [1, 0], 'gates': ['H'], 'n_qubits': 1}])
        device = next(model.parameters()).device
        inputs, targets = inputs.to(device), targets.to(device)
        
        # Add data normalization
        input_mean = inputs.mean()
        input_std = inputs.std()
        inputs = (inputs - input_mean) / (input_std + 1e-8)
        
    except Exception as e:
        logging.error(f"Error loading training data: {str(e)}")
        raise

    model.train()
    best_loss = float('inf')
    best_model_state = None
    
    # Reset meta-optimizer metrics at start of training
    meta_optimizer.reset_metrics()
    
    # Training loop with enhanced stability measures
    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        
        # Forward pass with gradient noise
        outputs = model(inputs)
        outputs = model.output_proj(outputs)  # Project to correct dimension
        loss = criterion(outputs, targets)
        
        # Compute gradients
        loss.backward()
        
        # Add scaled noise to gradients for regularization
        if noise_scale > 0:
            for param in model.parameters():
                if param.grad is not None:
                    noise = torch.randn_like(param.grad) * noise_scale * torch.norm(param.grad)
                    param.grad.add_(noise)
        
        # Compute gradient norm safely
        grad_norms = [torch.norm(p.grad) for p in model.parameters() if p.grad is not None]
        grad_norm = torch.norm(torch.stack(grad_norms)) if grad_norms else torch.tensor(0.0)
        
        # Clip gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), gradient_clip)
        
        # Optimize
        optimizer.step()
        scheduler.step()
        
        # Get current metrics
        current_lr = scheduler.get_last_lr()[0]
        param_norms = [torch.norm(p) for p in model.parameters()]
        param_norm = torch.norm(torch.stack(param_norms))
        
        # Update meta-optimizer
        meta_optimizer.optimize(
            parameter_history=torch.cat([p.data.flatten() for p in model.parameters()]).numpy(),
            current_loss=loss.item()
        )
        
        # Early stopping check
        if early_stopping(loss.item()):
            logging.info(f"Early stopping triggered at epoch {epoch}")
            break
        
        # Checkpoint saving
        if epoch % 5 == 0:
            save_checkpoint(model, optimizer, meta_optimizer, epoch, loss.item())
        
        # Update best model if we have a new best loss
        if loss.item() < best_loss:
            best_loss = loss.item()
            best_model_state = {
                'model_state': clone_parameters(model),
                'meta_optimizer_state': meta_optimizer.state_dict(),
                'epoch': epoch,
                'loss': loss.item()
            }
        
        loss_history.append(loss.item())
        param_norm_history.append(param_norm.detach().item())
        lr_history.append(current_lr)
        grad_norm_history.append(grad_norm.detach().item())
        
        logging.info(f"Epoch {epoch}: loss={loss.item():.6f}, lr={current_lr:.6f}, "
                   f"grad_norm={grad_norm:.6f}, param_norm={param_norm:.6f}")
        
    # Final checkpoint and metrics
    save_checkpoint(model, optimizer, meta_optimizer, epoch, loss.item(), checkpoint_dir="final_checkpoint")
    final_metrics = meta_optimizer.get_performance_metrics()
    logging.info("Final training metrics:")
    for metric_name, values in final_metrics.items():
        if values:
            avg_value = np.mean(values[-10:])  # Average of last 10 values
            logging.info(f"  Average {metric_name}: {avg_value:.6f}")
    
    if visualize:
        visualize_training_history(loss_history, param_norm_history, lr_history, grad_norm_history)
    return loss_history, param_norm_history, lr_history, grad_norm_history

def visualize_training_history(loss_vals, param_norms, lr_history, grad_norms):
    """Visualize training metrics."""
    plt.figure(figsize=(15, 10))
    
    # Convert tensors to numpy arrays if needed
    def to_numpy(x):
        if torch.is_tensor(x):
            return x.detach().cpu().numpy()
        return x
    
    loss_vals = to_numpy(loss_vals)
    param_norms = to_numpy(param_norms)
    lr_history = to_numpy(lr_history)
    grad_norms = to_numpy(grad_norms)
    
    # Plot loss
    plt.subplot(2, 2, 1)
    plt.plot(loss_vals, marker='o', markersize=3, alpha=0.7)
    plt.title('Loss History')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    
    # Plot parameter norms
    plt.subplot(2, 2, 2)
    plt.plot(param_norms, marker='o', markersize=3, alpha=0.7, color='orange')
    plt.title('Parameter Norm History')
    plt.xlabel('Epoch')
    plt.ylabel('Parameter Norm')
    plt.grid(True)
    
    # Plot learning rates
    plt.subplot(2, 2, 3)
    plt.plot(lr_history, marker='o', markersize=3, alpha=0.7, color='green')
    plt.title('Learning Rate History')
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.grid(True)
    
    # Plot gradient norms
    plt.subplot(2, 2, 4)
    plt.plot(grad_norms, marker='o', markersize=3, alpha=0.7, color='red')
    plt.title('Gradient Norm History')
    plt.xlabel('Epoch')
    plt.ylabel('Gradient Norm')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        # Initialize components
        model = QuantumTransformer(d_model=4, n_heads=1, n_layers=1, n_qubits=1)
        model.output_proj = nn.Linear(4, 2)  # Add output projection layer
        
        meta_optimizer = MetaOptimizer(
            input_dim=4,
            hidden_dim=16,
            history_length=3
        )
        
        # Generate sample training data
        sample_train_data = [
            {'input_state': [1, 0], 'target_state': [0, 1], 'n_qubits': 1}
            for _ in range(10)
        ]
        
        # Run experiment
        epochs = 50  # Increased epochs for slower training
        loss_vals, param_norms, lr_history, grad_norms = simulation_experiment_loop(
            num_epochs=epochs,
            initial_lr=0.000001,  # Very small initial learning rate
            max_lr=0.00001,     # Very small maximum learning rate
            warmup_epochs=10,    # Longer warmup period
            patience=20,         # More patience
            weight_decay=0.1,    # Strong regularization
            gradient_clip=0.1,   # Aggressive gradient clipping
            noise_scale=0.01,    # Small noise scale
            visualize=True,
            update_interval=1.0
        )
        
        # Visualize results
        visualize_training_history(loss_vals, param_norms, lr_history, grad_norms)
        
    except Exception as e:
        logging.error(f"Fatal error in main execution: {str(e)}")
        raise

# END OF simulation_experiment.py

# NOTE: Enhanced with comprehensive error handling, early stopping, and checkpointing
# History tracking:
# - Added anomaly detection for better debugging
# - Fixed in-place operations in parameter updates
# - Added gradient clipping to prevent exploding gradients
# - Reduced epochs and adjusted checkpoint frequency for testing
# - Improved error handling and recovery mechanisms

# NOTE: This file is crucial for monitoring model convergence and performance over iterative meta-learning updates. Detailed inline comments help maintain clarity for future enhancements. 
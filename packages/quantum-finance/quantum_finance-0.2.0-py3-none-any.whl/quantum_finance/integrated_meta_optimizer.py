import numpy as np
from advanced_meta_update import advanced_meta_update


def simulated_loss(params):
    """
    Compute a simple quadratic loss function.
    In this case, the target is a vector of ones.
    Loss = sum((params - target)^2)
    """
    target = np.ones_like(params)
    return np.sum((params - target) ** 2)


def simulated_gradient(params):
    """
    Compute the gradient of the quadratic loss function.
    For loss = sum((params - target)^2), the gradient is 2*(params - target).
    """
    target = np.ones_like(params)
    return 2 * (params - target)


def training_loop(num_epochs, init_params, alpha=0.1, scaling=1.0):
    """
    Simulate a training loop where model parameters are updated using the advanced_meta_update function.
    At each epoch, the loss, its gradient, and the change in loss (delta_loss) are computed. 
    The advanced_meta_update function then adapts the update based on these values.

    Parameters:
        num_epochs (int): The number of epochs to simulate.
        init_params (np.array): Initial parameters of the model.
        alpha (float): Learning rate or scaling factor for the update step.
        scaling (float): Additional metric (scaling) passed to advanced_meta_update.

    Returns:
        np.array: The optimized parameters after training.
    """
    params = init_params.copy()
    prev_loss = simulated_loss(params)
    
    print("Starting training loop with initial parameters:", params)
    
    for epoch in range(num_epochs):
        # Compute current loss and its gradient
        loss = simulated_loss(params)
        grad = simulated_gradient(params)
        
        # Calculate change in loss since last epoch
        delta_loss = loss - prev_loss
        
        # Prepare additional metrics. In this case, using a scaling factor.
        additional_metrics = {'scaling': scaling}
        
        # Update parameters using the advanced meta update mechanism
        new_params = advanced_meta_update(params, grad, delta_loss, additional_metrics, alpha)
        
        # Log current epoch details
        print(f"Epoch {epoch+1}: Loss = {loss:.5f}, Delta Loss = {delta_loss:.5f}, Params = {params}")
        
        # Update parameters and previous loss for the next iteration
        params = new_params
        prev_loss = loss
        
    print("Training completed. Optimized parameters:", params)
    return params


if __name__ == "__main__":
    # Example usage: starting with an initial parameter vector far from the target [1, 1, 1]
    init_params = np.array([5.0, 5.0, 5.0])
    optimized_params = training_loop(num_epochs=10, init_params=init_params, alpha=0.1, scaling=1.0) 
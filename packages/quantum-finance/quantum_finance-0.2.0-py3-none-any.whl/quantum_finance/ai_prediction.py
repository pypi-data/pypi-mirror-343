import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from sklearn.preprocessing import MinMaxScaler
# Import from quantum-AI interface - but only what's needed for type hints
from typing import TYPE_CHECKING, List, Tuple, Dict, Optional, Any, Union
if TYPE_CHECKING:
    from quantum_ai_interface import QuantumMeasurementResult
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import logging

# Configure logging - but make it less verbose
logging.basicConfig(level=logging.WARNING)

def prepare_data(data, time_steps):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps), 0])
        y.append(data[i + time_steps, 0])
    # Reshape X to be [samples, time steps, features]
    return np.array(X).reshape(len(X), time_steps, 1), np.array(y)

def create_lstm_model(input_shape, output_shape=1):
    """Create an LSTM model for time series prediction.
    
    Args:
        input_shape: Shape of input data (time_steps, features)
        output_shape: Number of output dimensions
        
    Returns:
        Compiled Keras model
    """
    from tensorflow.keras.models import Model as KerasModel
    
    # Create a proper input layer to avoid the warnings
    inputs = Input(shape=input_shape)
    x = LSTM(64, return_sequences=True)(inputs)
    x = Dropout(0.2)(x)
    x = LSTM(32)(x)
    x = Dropout(0.2)(x)
    outputs = Dense(output_shape)(x)
    
    model = KerasModel(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='mse')
    
    return model

def train_and_predict(data, time_steps, future_steps):
    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))
    
    # Prepare data for LSTM
    X, y = prepare_data(scaled_data, time_steps)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    # Create and train the model
    model = create_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=100, batch_size=32, verbose=0)
    
    # Make predictions
    last_sequence = scaled_data[-time_steps:]
    current_batch = last_sequence.reshape((1, time_steps, 1))
    future_predictions = []
    
    for _ in range(future_steps):
        current_pred = model.predict(current_batch)[0]
        future_predictions.append(current_pred)
        current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)
    
    # Inverse transform the predictions
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
    
    return future_predictions

def train_quantum_enhanced_model(data=None, time_steps=10, future_steps=5):
    """Train a model enhanced with quantum measurements and predict future values.
    
    Args:
        data: Time series data (if None, synthetic data is generated)
        time_steps: Number of time steps in each sample
        future_steps: Number of steps to predict into the future
        
    Returns:
        Tuple of (predictor, predictions, uncertainties)
    """
    print("Training quantum-enhanced AI model...")
    
    # Generate synthetic time series data if not provided
    if data is None:
        np.random.seed(42)
        t = np.linspace(0, 1, 200)
        data = np.sin(2 * np.pi * 2 * t) + 0.1 * np.random.randn(len(t))
        data = data.reshape(-1, 1)
    
    # Prepare data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    X, y = prepare_data(scaled_data, time_steps)
    
    # Split into train/test
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Create and train model
    model = create_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]), output_shape=1)
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
    
    # Create a quantum-AI predictor
    quantum_predictor = AiQuantumPredictor(model=model, uncertainty_aware=True)
    
    # Make future predictions using quantum measurements
    future_predictions = []
    prediction_uncertainties = []
    
    # Start with the last sequence from the test set
    current_batch = X_test[-1:].copy()
    
    # When using with actual quantum measurement results, we would pass those in
    # Here we'll simulate this by creating a dummy QuantumMeasurementResult from the data
    for i in range(future_steps):
        # In a real application, this would come from a quantum circuit execution
        dummy_quantum_result = create_dummy_quantum_measurement(current_batch[0])
        
        # Get prediction with uncertainty using the quantum-AI interface
        prediction, uncertainty = quantum_predictor.predict(dummy_quantum_result, include_uncertainty=True)
        
        # Extract the scalar value - prediction is now directly the array without batch dimension
        # and uncertainty is also directly the array
        future_predictions.append(prediction[0])  # First output dimension
        prediction_uncertainties.append(uncertainty[0])  # First output dimension uncertainty
        
        # Update batch for next prediction
        new_value = np.array([[[prediction[0]]]])
        current_batch = np.append(current_batch[:, 1:, :], new_value, axis=1)
    
    # Convert predictions back to original scale
    future_predictions = np.array(future_predictions).reshape(-1, 1)
    future_predictions = scaler.inverse_transform(future_predictions)
    
    # Visualize predictions with uncertainty
    plt.figure(figsize=(12, 6))
    
    # Plot training data
    plt.plot(range(len(data)), data, 'b-', label='Historical Data')
    
    # Plot future predictions with uncertainty range
    x_future = np.arange(len(data), len(data) + future_steps)
    plt.plot(x_future, future_predictions, 'r-', label='Quantum-Enhanced Prediction')
    
    # Calculate uncertainty in original scale
    uncertainty_scale = (scaler.data_max_ - scaler.data_min_) * np.array(prediction_uncertainties)
    plt.fill_between(
        x_future,
        future_predictions.reshape(-1) - uncertainty_scale.reshape(-1),
        future_predictions.reshape(-1) + uncertainty_scale.reshape(-1),
        color='r', alpha=0.2, label='Prediction Uncertainty'
    )
    
    plt.title('Quantum-Enhanced Time Series Prediction')
    plt.xlabel('Time Step')
    plt.ylabel('Value')
    plt.legend()
    
    # Save the visualization
    os.makedirs('quantum_ai_test_results', exist_ok=True)
    plt.savefig('quantum_ai_test_results/quantum_ai_prediction.png')
    plt.close()
    
    print("Prediction visualization saved to 'quantum_ai_test_results/quantum_ai_prediction.png'")
    
    return quantum_predictor, future_predictions, prediction_uncertainties

def create_dummy_quantum_measurement(data_sequence):
    """
    Create a dummy QuantumMeasurementResult from classical data for testing.
    In a real application, this would come from actual quantum circuit execution.
    
    Args:
        data_sequence: Input data sequence to convert
        
    Returns:
        QuantumMeasurementResult: A measurement result object usable by AiQuantumPredictor
    """
    from quantum_ai_interface import CircuitMetadata, UncertaintyMetrics
    
    # Convert the data sequence to probabilities that sum to 1
    # For simplicity, we'll create a 2-qubit system (4 states) from the data
    values = np.abs(data_sequence)
    probabilities = values / (np.sum(values) + 1e-10)  # Avoid division by zero
    
    # Map to quantum states (00, 01, 10, 11)
    states = ['00', '01', '10', '11']
    
    # For data with more than 4 elements, we'll just use the first 4
    # In a real application, we would map this more carefully
    num_states = min(len(probabilities), 4)
    
    # Create a counts dictionary based on 1000 shots
    shots = 1000
    counts = {}
    for i in range(num_states):
        state = states[i]
        # Ensure we have reasonable number of counts
        count = int(probabilities[i] * shots)
        if count > 0:
            counts[state] = count
    
    # If we have fewer than 4 states, add some defaults
    for i in range(num_states, 4):
        counts[states[i]] = 1  # Add minimal counts for missing states
    
    # Create metadata and uncertainty
    metadata = CircuitMetadata(
        num_qubits=2,
        circuit_depth=3,
        gate_counts={'h': 2, 'cx': 2, 'measure': 2},
        simulation_method='generated'
    )
    
    uncertainty = UncertaintyMetrics(
        shot_noise=1.0 / np.sqrt(shots),
        standard_error=0.01,
        confidence_interval=(0.0, 0.02),
        total_uncertainty=0.02
    )
    
    return QuantumMeasurementResult(counts=counts, metadata=metadata, uncertainty=uncertainty, shots=shots)

# Example usage
if __name__ == "__main__":
    # Generate some sample data
    np.random.seed(42)
    data = np.sin(np.linspace(0, 100, 1000)) + np.random.normal(0, 0.1, 1000)
    
    time_steps = 60
    future_steps = 30
    
    # Standard prediction
    predictions = train_and_predict(data, time_steps, future_steps)
    print("Future predictions (standard):", predictions.flatten())
    
    # Enhanced prediction with quantum integration and uncertainty
    quantum_predictor, quantum_predictions, uncertainties = train_quantum_enhanced_model(
        data, time_steps, future_steps
    )
    
    print("Future predictions (quantum-enhanced):", quantum_predictions.flatten())
    print("Prediction uncertainties:", uncertainties.flatten())
    
    # Visualize results with uncertainty bands
    plt.figure(figsize=(10, 6))
    x = np.arange(future_steps)
    
    # Plot standard predictions
    plt.plot(x, predictions, 'b-', label='Standard Prediction')
    
    # Plot quantum-enhanced predictions with uncertainty bands
    plt.plot(x, quantum_predictions, 'r-', label='Quantum-Enhanced Prediction')
    plt.fill_between(
        x, 
        quantum_predictions.flatten() - 2*uncertainties.flatten(),  # 95% confidence band
        quantum_predictions.flatten() + 2*uncertainties.flatten(),
        color='r', alpha=0.2, label='Uncertainty (95% CI)'
    )
    
    plt.title('Prediction Comparison with Uncertainty Quantification')
    plt.xlabel('Time Steps')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('quantum_enhanced_prediction.png')
    plt.close()
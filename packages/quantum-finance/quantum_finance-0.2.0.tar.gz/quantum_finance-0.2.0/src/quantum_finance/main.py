"""Module: main.py
This is the main integration script that demonstrates the interaction of the modular components:
- quantum_simulation (simulate_quantum_system)
- ai_prediction (predict_quantum_state)
- data_handling (process_quantum_data)

The purpose of this script is to provide a runnable example that ties together our core functionalities, enabling further development and testing.
"""

# Importing functions from modularized components
from backend.quantum_simulation import simulate_quantum_system
from backend.ai_prediction import predict_quantum_state
from backend.data_handling import process_quantum_data
import time
import datetime
import os
import sys
import signal
import logging
import random
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()  # Automatically load environment variables from .env file at startup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            "simulation_worker.log",
            maxBytes=5*1024*1024,  # 5MB maximum file size
            backupCount=3,  # Keep 3 backup files
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

# Configure separate logger for experiment results
experiment_logger = logging.getLogger('experiment_results')
experiment_logger.setLevel(logging.INFO)
# Ensure experiment logger doesn't inherit handlers from root logger
experiment_logger.propagate = False
# Add rotating file handler specifically for simulation_log.txt
experiment_logger.addHandler(
    RotatingFileHandler(
        "simulation_log.txt",
        maxBytes=5*1024*1024,  # 5MB maximum file size
        backupCount=5,  # Keep 5 backup files
        encoding='utf-8'
    )
)

# Global flag to control worker execution
running = True

def signal_handler(sig, frame):
    """Handle termination signals gracefully."""
    global running
    logging.info(f"Received signal {sig}, shutting down gracefully...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Main function to run the integrated simulation, prediction, and data processing routines."""
    # === Startup check for required environment variables ===
    REQUIRED_ENV_VARS = [
        'IBM_QUANTUM_TOKEN',
        'DATABASE_URL',
        # Add any other required secrets or API keys here
    ]
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    if missing_vars:
        logging.critical(f"Missing required environment variables: {', '.join(missing_vars)}. Exiting for production safety.")
        sys.exit(1)
    # === End startup check ===
    
    # Check if running in worker mode (continuous operation)
    worker_mode = os.environ.get('WORKER_MODE', 'default')
    
    # Run once or continuously based on mode
    if worker_mode == 'simulation':
        # In simulation worker mode, run continuously
        logging.info("Starting in simulation worker mode (continuous operation)")
        run_simulation_worker()
    else:
        # Default is to run once
        logging.info("Starting in default mode (single run)")
        single_simulation_run()


def single_simulation_run():
    """Run a single simulation cycle."""
    # Example parameters for quantum simulation
    simulation_params = {
        'qubits': 5,
        'iterations': 1000
    }
    
    # Run quantum simulation
    simulation_result = simulate_quantum_system(simulation_params)
    print('Quantum Simulation Result:', simulation_result)
    
    # Example input data for AI prediction
    ai_input = {
        'feature_vector': [0.1, 0.5, 0.3],
        'metadata': {'experiment': 'test_run'}
    }
    
    # Run AI prediction routine
    prediction_result = predict_quantum_state(ai_input)
    print('AI Prediction Result:', prediction_result)
    
    # Process data using the data handling module
    processed_data = process_quantum_data(ai_input)
    print('Processed Data:', processed_data)

    # Write experiment results to simulation_log.txt for persistent storage
    log_experiment_results(simulation_result, prediction_result, processed_data)


def run_simulation_worker():
    """Run in continuous worker mode, processing simulations repeatedly with robust error handling."""
    logging.info("Starting simulation worker in continuous mode...")
    
    # Initialize counters for monitoring
    iteration_count = 0
    error_count = 0
    last_success_time = datetime.datetime.now()
    
    # Main worker loop - continue until signaled to stop
    while running:
        try:
            iteration_count += 1
            logging.info(f"Starting iteration {iteration_count}")
            
            # Vary simulation parameters slightly to simulate different workloads
            qubits = 5 + random.randint(0, 3)  # Vary between 5-8 qubits
            iterations = 1000 + random.randint(-200, 200)  # Vary iterations
            
            # Example parameters for quantum simulation
            simulation_params = {
                'qubits': qubits,
                'iterations': iterations
            }
            
            # Run quantum simulation
            simulation_result = simulate_quantum_system(simulation_params)
            logging.info(f'Quantum Simulation Result: {simulation_result}')
            
            # Example input data for AI prediction
            ai_input = {
                'feature_vector': [random.random(), random.random(), random.random()],
                'metadata': {'experiment': f'worker_run_{iteration_count}'}
            }
            
            # Run AI prediction routine
            prediction_result = predict_quantum_state(ai_input)
            logging.info(f'AI Prediction Result: {prediction_result}')
            
            # Process data using the data handling module
            processed_data = process_quantum_data(ai_input)
            logging.info(f'Processed Data: {processed_data}')

            # Write experiment results to simulation_log.txt for persistent storage
            log_experiment_results(simulation_result, prediction_result, processed_data)
            
            # Update success metrics
            last_success_time = datetime.datetime.now()
            error_count = 0  # Reset error count after successful run
            
            # Sleep between iterations to avoid overloading the system
            # Use a dynamic sleep time based on system load or configuration
            sleep_time = float(os.environ.get('WORKER_SLEEP_TIME', '10'))
            logging.info(f"Sleeping for {sleep_time} seconds before next iteration")
            
            # Use a loop with small sleeps to check the running flag frequently
            # This allows for faster response to shutdown signals
            for _ in range(int(sleep_time)):
                if not running:
                    break
                time.sleep(1)
                
        except Exception as e:
            error_count += 1
            logging.error(f"Error in simulation worker (attempt {error_count}): {e}", exc_info=True)
            
            # Write error to dedicated error log
            with open("simulation_error_log.txt", "a") as error_log:
                error_log.write(f"Error at {datetime.datetime.now()}: {str(e)}\n")
            
            # Implement exponential backoff for repeated errors
            backoff_time = min(30 * (2 ** min(error_count - 1, 5)), 300)  # Cap at 5 minutes
            logging.info(f"Backing off for {backoff_time} seconds before retry")
            
            # Use a loop with small sleeps to check the running flag frequently
            for _ in range(int(backoff_time)):
                if not running:
                    break
                time.sleep(1)
    
    # Cleanup when loop exits
    logging.info("Simulation worker shutting down...")
    # Perform any necessary cleanup here


def log_experiment_results(simulation_result, prediction_result, processed_data):
    """Log experiment results using the logging module."""
    try:
        # Create a formatted log message
        log_message = (
            "====================\n"
            f"Experiment run at {datetime.datetime.now()}:\n"
            f"Quantum Simulation Result: {simulation_result}\n"
            f"AI Prediction Result: {prediction_result}\n"
            f"Processed Data: {processed_data}\n"
        )
        
        # Use the experiment logger instead of the root logger
        experiment_logger.info(log_message)
    except Exception as e:
        logging.error(f"Failed to log experiment results: {e}")


if __name__ == '__main__':
    main()
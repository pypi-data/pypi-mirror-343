import time
from quantum_algorithms import shors_algorithm, grovers_algorithm
from ml_framework import transformer_model

def run_benchmarks():
    print("Running benchmarks...")

    # Benchmark Shor's Algorithm
    start_time = time.time()
    shors_algorithm(15)  # Example input
    shor_time = time.time() - start_time
    print(f"Shor's Algorithm execution time: {shor_time:.4f} seconds")

    # Benchmark Grover's Algorithm
    start_time = time.time()
    grovers_algorithm([0, 1, 0, 1])  # Example input
    grover_time = time.time() - start_time
    print(f"Grover's Algorithm execution time: {grover_time:.4f} seconds")

    # Benchmark Transformer Model
    start_time = time.time()
    transformer_model.predict(input_data)  # Example input
    transformer_time = time.time() - start_time
    print(f"Transformer Model execution time: {transformer_time:.4f} seconds")

if __name__ == "__main__":
    run_benchmarks()
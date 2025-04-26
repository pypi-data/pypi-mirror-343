"""
Benchmark script for evaluating the performance of the memory-enhanced quantum transformer.

This script measures various performance metrics including:
1. Memory capacity and utilization
2. Processing speed
3. Prediction accuracy
4. Memory effect on sequential tasks
"""

import torch
import numpy as np
import time
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
from tqdm import tqdm

from quantum_finance.backend.quantum_transformer import QuantumTransformer
from quantum_finance.backend.quantum_memory import QuantumMemristor

class QuantumMemoryBenchmark:
    def __init__(self,
                 d_model: int = 64,
                 n_heads: int = 4,
                 n_layers: int = 2,
                 n_qubits: int = 4,
                 memory_size: int = 32,
                 device: str = 'cuda' if torch.cuda.is_available() else 'cpu'):
        """Initialize benchmark environment"""
        self.device = device
        self.model = QuantumTransformer(
            d_model=d_model,
            n_heads=n_heads,
            n_layers=n_layers,
            n_qubits=n_qubits,
            memory_size=memory_size
        ).to(device)
        
        # Model parameters
        self.d_model = d_model
        self.memory_size = memory_size
        
        # Benchmark results
        self.results = {}
        
    def generate_sequence_data(self, 
                             seq_len: int, 
                             batch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generate synthetic sequence data for benchmarking"""
        # Create input sequence
        x = torch.randn(seq_len, batch_size, self.d_model, device=self.device)
        
        # Create target sequence (shifted by 1 step)
        y = torch.roll(x, -1, dims=0)
        
        return x, y
        
    def benchmark_memory_capacity(self, 
                                n_steps: int = 100) -> Dict[str, List[float]]:
        """Measure memory capacity over time"""
        capacities = []
        entanglement = []
        
        # Generate test input
        x = torch.randn(1, 1, self.d_model, device=self.device)
        
        # Track memory metrics over time
        for _ in tqdm(range(n_steps), desc="Measuring memory capacity"):
            self.model(x)
            states = self.model.get_memory_states()
            
            # Average capacity across layers
            avg_capacity = np.mean([state['capacity'] for state in states])
            avg_entanglement = np.mean([
                np.mean(state['entanglement']) for state in states
            ])
            
            capacities.append(avg_capacity)
            entanglement.append(avg_entanglement)
            
        return {
            'capacity': capacities,
            'entanglement': entanglement
        }
        
    def benchmark_processing_speed(self,
                                 batch_sizes: List[int],
                                 seq_lens: List[int],
                                 n_runs: int = 10) -> Dict[str, List[float]]:
        """Measure processing speed for different batch sizes and sequence lengths"""
        results = {
            'batch_size': [],
            'seq_len': [],
            'time_per_token': []
        }
        
        for batch_size in batch_sizes:
            for seq_len in seq_lens:
                times = []
                for _ in range(n_runs):
                    x = torch.randn(seq_len, batch_size, self.d_model, 
                                  device=self.device)
                    
                    # Measure processing time
                    start_time = time.time()
                    with torch.no_grad():
                        self.model(x)
                    end_time = time.time()
                    
                    # Calculate time per token
                    total_tokens = batch_size * seq_len
                    time_per_token = (end_time - start_time) / total_tokens
                    times.append(time_per_token)
                
                # Record average results
                results['batch_size'].append(batch_size)
                results['seq_len'].append(seq_len)
                results['time_per_token'].append(np.mean(times))
                
        return results
        
    def benchmark_memory_effect(self,
                              seq_len: int = 50,
                              n_sequences: int = 10) -> Dict[str, List[float]]:
        """Measure the effect of memory on prediction accuracy"""
        results = {
            'with_memory_loss': [],
            'without_memory_loss': []
        }
        
        # Generate test sequences
        sequences = []
        for _ in range(n_sequences):
            x, y = self.generate_sequence_data(seq_len, batch_size=1)
            sequences.append((x, y))
        
        # Test with memory
        self.model.train()
        for x, y in sequences:
            output = self.model(x)
            loss = torch.nn.functional.mse_loss(output, y)
            results['with_memory_loss'].append(loss.item())
            
        # Test without memory (reset between sequences)
        for x, y in sequences:
            self.model.reset_memory()
            output = self.model(x)
            loss = torch.nn.functional.mse_loss(output, y)
            results['without_memory_loss'].append(loss.item())
            
        return results
        
    def plot_results(self) -> None:
        """Plot benchmark results"""
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot memory capacity
        if 'memory_capacity' in self.results:
            axes[0, 0].plot(self.results['memory_capacity']['capacity'])
            axes[0, 0].plot(self.results['memory_capacity']['entanglement'])
            axes[0, 0].set_title('Memory Capacity Over Time')
            axes[0, 0].set_xlabel('Steps')
            axes[0, 0].set_ylabel('Capacity / Entanglement')
            axes[0, 0].legend(['Capacity', 'Entanglement'])
            
        # Plot processing speed
        if 'processing_speed' in self.results:
            speed_data = self.results['processing_speed']
            for seq_len in set(speed_data['seq_len']):
                mask = [s == seq_len for s in speed_data['seq_len']]
                axes[0, 1].plot(
                    [speed_data['batch_size'][i] for i in range(len(mask)) if mask[i]],
                    [speed_data['time_per_token'][i] for i in range(len(mask)) if mask[i]],
                    label=f'Seq Len {seq_len}'
                )
            axes[0, 1].set_title('Processing Speed')
            axes[0, 1].set_xlabel('Batch Size')
            axes[0, 1].set_ylabel('Time per Token (s)')
            axes[0, 1].legend()
            
        # Plot memory effect
        if 'memory_effect' in self.results:
            effect_data = self.results['memory_effect']
            axes[1, 0].plot(effect_data['with_memory_loss'], label='With Memory')
            axes[1, 0].plot(effect_data['without_memory_loss'], label='Without Memory')
            axes[1, 0].set_title('Memory Effect on Prediction')
            axes[1, 0].set_xlabel('Sequence')
            axes[1, 0].set_ylabel('Loss')
            axes[1, 0].legend()
            
        plt.tight_layout()
        plt.savefig('benchmark_results.png')
        plt.close()
        
    def run_all_benchmarks(self) -> Dict[str, Dict]:
        """Run all benchmarks and collect results"""
        print("Running memory capacity benchmark...")
        self.results['memory_capacity'] = self.benchmark_memory_capacity()
        
        print("\nRunning processing speed benchmark...")
        self.results['processing_speed'] = self.benchmark_processing_speed(
            batch_sizes=[1, 2, 4, 8, 16],
            seq_lens=[10, 50, 100]
        )
        
        print("\nRunning memory effect benchmark...")
        self.results['memory_effect'] = self.benchmark_memory_effect()
        
        print("\nGenerating plots...")
        self.plot_results()
        
        return self.results

def main():
    """Run benchmarks and save results"""
    print("Initializing benchmark environment...")
    benchmark = QuantumMemoryBenchmark()
    
    print("\nRunning benchmarks...")
    results = benchmark.run_all_benchmarks()
    
    print("\nSaving results...")
    torch.save(results, 'benchmark_results.pt')
    
    print("\nBenchmark complete! Results saved to 'benchmark_results.pt' and 'benchmark_results.png'")

if __name__ == '__main__':
    main() 
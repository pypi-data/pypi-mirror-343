import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_execution_times(results, title="Quantum Circuit Execution Times"):
    """Plot execution times for different circuits."""
    # Extract data
    circuit_names = list(results.keys())
    avg_times = [result[0] for result in results.values()]
    std_times = [result[1] for result in results.values()]
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Create bar plot
    bars = plt.bar(range(len(circuit_names)), avg_times, yerr=std_times,
                  capsize=5, alpha=0.7)
    
    # Customize plot
    plt.title(title, fontsize=14, pad=20)
    plt.xlabel("Circuit Type", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.xticks(range(len(circuit_names)), circuit_names, rotation=45, ha='right')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}s',
                ha='center', va='bottom')
    
    plt.tight_layout()
    return plt.gcf()

def plot_scaling_analysis(results, circuit_type="ghz_state"):
    """Plot how execution time scales with number of qubits."""
    # Extract relevant results
    scaling_data = {
        k: v[0] for k, v in results.items() 
        if k.startswith(circuit_type) and '_' in k
    }
    
    # Extract number of qubits from keys
    n_qubits = [int(k.split('_')[-1]) for k in scaling_data.keys()]
    times = list(scaling_data.values())
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Plot actual data points
    plt.scatter(n_qubits, times, color='blue', label='Measured', s=100)
    
    # Fit exponential curve
    coeffs = np.polyfit(n_qubits, np.log(times), 1)
    fit_times = np.exp(coeffs[1]) * np.exp(coeffs[0] * np.array(n_qubits))
    plt.plot(n_qubits, fit_times, 'r--', label='Exponential fit')
    
    # Customize plot
    plt.title(f"Execution Time Scaling for {circuit_type.replace('_', ' ').title()}", 
              fontsize=14, pad=20)
    plt.xlabel("Number of Qubits", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Add scaling factor annotation
    scaling_factor = np.exp(coeffs[0])
    plt.annotate(f"Scaling factor: {scaling_factor:.2f}x per qubit",
                xy=(0.05, 0.95), xycoords='axes fraction',
                bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    return plt.gcf()

def plot_gate_distribution(results, circuit_name):
    """Plot gate distribution for a specific circuit."""
    # Get the gate counts from the first run
    gate_counts = results[circuit_name][2][0].metadata.gate_counts
    
    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(gate_counts.values(), labels=gate_counts.keys(), autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title(f"Gate Distribution for {circuit_name}", fontsize=14, pad=20)
    
    plt.axis('equal')
    return plt.gcf()

def create_performance_report(results, output_dir="performance_reports"):
    """Create a comprehensive performance report with visualizations."""
    import os
    from datetime import datetime
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp for the report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create main report figures
    figs = []
    
    # 1. Overall execution times
    fig1 = plot_execution_times(results)
    figs.append(("overall_execution_times", fig1))
    
    # 2. Scaling analysis for different circuit types
    for circuit_type in ['ghz_state', 'qft']:
        fig = plot_scaling_analysis(results, circuit_type)
        figs.append((f"{circuit_type}_scaling", fig))
    
    # 3. Gate distribution for each circuit type
    for circuit_name in results.keys():
        if not any(x in circuit_name for x in ['random', 'depth']):  # Skip random circuits
            fig = plot_gate_distribution(results, circuit_name)
            figs.append((f"{circuit_name}_gates", fig))
    
    # Save all figures
    for name, fig in figs:
        fig.savefig(os.path.join(output_dir, f"{timestamp}_{name}.png"))
        plt.close(fig)
    
    # Generate HTML report
    html_content = f"""
    <html>
    <head>
        <title>Quantum Circuit Performance Report - {timestamp}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            .figure {{ margin: 20px 0; text-align: center; }}
            .figure img {{ max-width: 100%; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Quantum Circuit Performance Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <h2>Performance Summary</h2>
        <table>
            <tr>
                <th>Circuit Type</th>
                <th>Average Time (s)</th>
                <th>Standard Deviation (s)</th>
            </tr>
    """
    
    # Add results to HTML
    for circuit_name, (avg_time, std_time, _) in results.items():
        html_content += f"""
            <tr>
                <td>{circuit_name}</td>
                <td>{avg_time:.4f}</td>
                <td>{std_time:.4f}</td>
            </tr>
        """
    
    # Add figures to HTML
    html_content += "</table><h2>Visualizations</h2>"
    for name, _ in figs:
        html_content += f"""
        <div class="figure">
            <h3>{name.replace('_', ' ').title()}</h3>
            <img src="{timestamp}_{name}.png" alt="{name}">
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    # Save HTML report
    with open(os.path.join(output_dir, f"{timestamp}_report.html"), 'w') as f:
        f.write(html_content)
    
    return os.path.join(output_dir, f"{timestamp}_report.html") 
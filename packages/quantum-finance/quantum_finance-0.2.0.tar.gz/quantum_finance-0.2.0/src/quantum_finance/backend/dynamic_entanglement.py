import torch
from typing import List, Tuple


def dynamic_entanglement(gradient_metrics: torch.Tensor, threshold: float = 0.5) -> List[Tuple[int, int]]:
    """
    Generate dynamic qubit pairs for entanglement based on gradient metrics.

    Args:
        gradient_metrics (torch.Tensor): A tensor containing gradient magnitudes for each qubit.
        threshold (float, optional): A threshold value; only qubits with gradient above this value considered for pairing.

    Returns:
        List[Tuple[int, int]]: A list of tuples, each representing a pair of qubit indices.

    Implementation Notes:
        - This simple algorithm pairs adjacent qubits if both have gradient metrics above the threshold.
        - This method can be extended to more advanced pairing strategies, e.g., based on relative gradient differences or non-adjacent qubit combinations.
    """
    n_qubits = gradient_metrics.shape[0]
    pairs = []
    # Iterate over the qubits and form pairs based on adjacent high gradient values
    for i in range(n_qubits - 1):
        # Debug: Print gradient values being compared
        # print(f"Comparing qubit {i} with value {gradient_metrics[i]:.4f} and qubit {i+1} with value {gradient_metrics[i+1]:.4f}")
        if gradient_metrics[i] > threshold and gradient_metrics[i+1] > threshold:
            pairs.append((i, i+1))

    # Optional: Further logic can be implemented to explore non-adjacent pairings or probabilistic selection
    return pairs


# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Create a sample gradient tensor for 5 qubits
    sample_gradients = torch.tensor([0.6, 0.7, 0.4, 0.8, 0.9])
    entanglement_pairs = dynamic_entanglement(sample_gradients, threshold=0.5)
    print("Dynamic Entanglement Pairs:", entanglement_pairs)  # Expected output: [(0, 1), (3, 4)] 
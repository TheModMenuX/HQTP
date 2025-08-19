import numpy as np
from typing import Callable, List
from .statevector import QuantumRegister
from .gates import hadamard_all, phase_oracle, diffusion

def grover_search(
    oracle_func: Callable[[List[int]], bool],
    num_qubits: int,
    num_iterations: int = None
) -> List[int]:
    """
    Implement Grover's algorithm
    
    Args:
        oracle_func: Function that returns True for marked states
        num_qubits: Number of qubits in search space
        num_iterations: Number of Grover iterations (defaults to π/4 * sqrt(N))
    
    Returns:
        Measured bit string that hopefully satisfies oracle
    """
    if num_iterations is None:
        # π/4 * sqrt(N) iterations
        num_iterations = int(np.pi/4 * np.sqrt(2**num_qubits))
        
    # Initialize in uniform superposition
    reg = QuantumRegister(num_qubits)
    hadamard_all(reg)
    
    # Grover iterations
    for _ in range(num_iterations):
        # Oracle
        phase_oracle(reg, oracle_func)
        # Diffusion
        hadamard_all(reg)
        diffusion(reg)
        hadamard_all(reg)
        
    return reg.measure()
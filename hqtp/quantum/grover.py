
import numpy as np
from typing import Callable, List, Optional
from .statevector import QuantumRegister
from .gates import hadamard_all, phase_oracle, diffusion

def grover_search(num_vars: int, oracle: Callable[[List[int]], bool], 
                 max_iterations: int = None) -> Optional[List[int]]:
    """
    Grover's algorithm for searching satisfying assignments
    
    Args:
        num_vars: Number of Boolean variables
        oracle: Function that returns True for satisfying assignments
        max_iterations: Maximum Grover iterations
    
    Returns:
        Satisfying assignment or None if not found
    """
    if max_iterations is None:
        max_iterations = int(np.pi * np.sqrt(2**num_vars) / 4)
    
    # Initialize quantum register
    reg = QuantumRegister(num_vars)
    
    # Create uniform superposition
    hadamard_all(reg)
    
    # Grover iterations
    for _ in range(max_iterations):
        # Apply oracle
        phase_oracle(reg, oracle)
        
        # Apply diffusion operator
        diffusion(reg)
    
    # Measure result
    result = reg.measure()
    
    # Verify result
    if oracle(result):
        return result
    
    return None

def amplitude_amplification(reg: QuantumRegister, 
                          oracle: Callable[[List[int]], bool],
                          iterations: int):
    """Apply amplitude amplification for the given oracle"""
    for _ in range(iterations):
        # Mark target states
        phase_oracle(reg, oracle)
        
        # Invert about average
        hadamard_all(reg)
        
        # Phase flip |0...0⟩
        reg.state[0] *= -1
        
        hadamard_all(reg)
        
        # Global phase correction
        reg.state *= -1

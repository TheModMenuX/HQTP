import numpy as np
from typing import List
from .statevector import QuantumRegister

# Common single-qubit gates
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # Hadamard
X = np.array([[0, 1], [1, 0]])                # Pauli-X (NOT)
Z = np.array([[1, 0], [0, -1]])               # Pauli-Z (Phase)

def hadamard_all(reg: QuantumRegister):
    """Apply Hadamard to all qubits"""
    for i in range(reg.num_qubits):
        reg.apply_gate(H, [i])
        
def phase_oracle(reg: QuantumRegister, 
                oracle_func: callable):
    """Apply phase oracle |x⟩ → (-1)^{f(x)}|x⟩"""
    for i in range(len(reg.state)):
        if oracle_func(list(map(int, f"{i:0{reg.num_qubits}b}"))):
            reg.state[i] *= -1
            
def diffusion(reg: QuantumRegister):
    """Apply Grover diffusion operator"""
    # |s⟩⟨s| - I where |s⟩ is uniform superposition
    reg.state = 2 * np.mean(reg.state) - reg.state
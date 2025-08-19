
import numpy as np
from typing import List, Tuple

class QuantumRegister:
    """Quantum state vector simulator"""
    
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1.0  # Initialize to |00...0⟩
    
    def apply_gate(self, gate: np.ndarray, qubits: List[int]):
        """Apply quantum gate to specified qubits"""
        if len(qubits) == 1:
            self._apply_single_qubit_gate(gate, qubits[0])
        elif len(qubits) == 2:
            self._apply_two_qubit_gate(gate, qubits[0], qubits[1])
        else:
            raise NotImplementedError("Gates on >2 qubits not implemented")
    
    def _apply_single_qubit_gate(self, gate: np.ndarray, qubit: int):
        """Apply single-qubit gate"""
        new_state = np.zeros_like(self.state)
        
        for i in range(len(self.state)):
            # Extract bit at position 'qubit'
            bit = (i >> qubit) & 1
            other_bits = i ^ (bit << qubit)
            
            # Apply gate
            for new_bit in [0, 1]:
                new_i = other_bits | (new_bit << qubit)
                new_state[new_i] += gate[new_bit, bit] * self.state[i]
        
        self.state = new_state
    
    def _apply_two_qubit_gate(self, gate: np.ndarray, qubit1: int, qubit2: int):
        """Apply two-qubit gate"""
        new_state = np.zeros_like(self.state)
        
        for i in range(len(self.state)):
            bit1 = (i >> qubit1) & 1
            bit2 = (i >> qubit2) & 1
            other_bits = i ^ (bit1 << qubit1) ^ (bit2 << qubit2)
            
            # Two-qubit basis state
            basis_state = (bit2 << 1) | bit1
            
            for new_basis in range(4):
                new_bit1 = new_basis & 1
                new_bit2 = (new_basis >> 1) & 1
                new_i = other_bits | (new_bit1 << qubit1) | (new_bit2 << qubit2)
                
                new_state[new_i] += gate[new_basis, basis_state] * self.state[i]
        
        self.state = new_state
    
    def measure(self) -> List[int]:
        """Measure all qubits, returning classical bit string"""
        probabilities = np.abs(self.state) ** 2
        outcome = np.random.choice(len(self.state), p=probabilities)
        
        # Convert to bit string
        bits = []
        for i in range(self.num_qubits):
            bits.append((outcome >> i) & 1)
        
        return bits
    
    def get_probabilities(self) -> np.ndarray:
        """Get measurement probabilities for all basis states"""
        return np.abs(self.state) ** 2

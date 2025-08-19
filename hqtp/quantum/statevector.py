import numpy as np
from typing import List

class QuantumRegister:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        # Initialize to |0...0⟩ state
        self.state = np.zeros(2**num_qubits, dtype=np.complex128)
        self.state[0] = 1.0
        
    def apply_gate(self, gate: np.ndarray, targets: List[int]):
        """Apply quantum gate to target qubits"""
        # TODO: Implement general quantum gate application
        pass
        
    def measure(self) -> List[int]:
        """Measure all qubits in computational basis"""
        probs = np.abs(self.state) ** 2
        outcome = np.random.choice(len(self.state), p=probs)
        return [int(x) for x in f"{outcome:0{self.num_qubits}b}"]
from typing import List
import numpy as np
from ..logic.parser import Clause, Literal

def extract_clause_features(clause: Clause) -> np.ndarray:
    """Extract numerical features from a clause"""
    features = [
        len(clause.literals),  # Clause size
        sum(1 for lit in clause.literals if lit.positive),  # Num positive lits
        sum(1 for lit in clause.literals if not lit.positive),  # Num negative lits
        # TODO: Add more sophisticated features
    ]
    return np.array(features, dtype=np.float32)

def extract_literal_features(lit: Literal, clause: Clause) -> np.ndarray:
    """Extract numerical features from a literal in context"""
    features = [
        1.0 if lit.positive else 0.0,  # Polarity
        len(lit.args),  # Arity
        # TODO: Add more sophisticated features
    ]
    return np.array(features, dtype=np.float32)
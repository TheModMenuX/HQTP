from dataclasses import dataclass
from typing import List, Set

@dataclass(frozen=True)
class Literal:
    var: int
    positive: bool
    
    def __invert__(self) -> 'Literal':
        """Return negation of literal"""
        return Literal(self.var, not self.positive)

@dataclass(frozen=True)
class Clause:
    literals: Set[Literal]
    
    def __len__(self) -> int:
        return len(self.literals)
    
    def is_unit(self) -> bool:
        """Check if clause has exactly one literal"""
        return len(self.literals) == 1
    
    def is_empty(self) -> bool:
        """Check if clause has no literals"""
        return len(self.literals) == 0

@dataclass
class CNFFormula:
    clauses: List[Clause]
    num_vars: int
    
    def add_clause(self, clause: Clause):
        self.clauses.append(clause)
        for lit in clause.literals:
            self.num_vars = max(self.num_vars, lit.var)
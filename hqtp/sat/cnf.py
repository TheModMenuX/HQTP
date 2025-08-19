
from typing import List, Set
from dataclasses import dataclass

@dataclass
class Literal:
    var: int
    positive: bool
    
    def __hash__(self):
        return hash((self.var, self.positive))
    
    def __eq__(self, other):
        return self.var == other.var and self.positive == other.positive

@dataclass
class Clause:
    literals: List[Literal]
    
    def __hash__(self):
        return hash(tuple(sorted(self.literals, key=lambda l: (l.var, l.positive))))
    
    def __len__(self):
        return len(self.literals)

class CNFFormula:
    """Conjunctive Normal Form formula representation"""
    
    def __init__(self):
        self.clauses: List[Clause] = []
        self.num_vars = 0
    
    def add_clause(self, clause: Clause):
        """Add clause to formula"""
        self.clauses.append(clause)
        
        # Update variable count
        for lit in clause.literals:
            self.num_vars = max(self.num_vars, lit.var)
    
    def get_variables(self) -> Set[int]:
        """Get all variables in formula"""
        variables = set()
        for clause in self.clauses:
            for lit in clause.literals:
                variables.add(lit.var)
        return variables
    
    def is_satisfied(self, assignment: dict) -> bool:
        """Check if formula is satisfied by assignment"""
        for clause in self.clauses:
            clause_satisfied = False
            
            for lit in clause.literals:
                if lit.var in assignment:
                    if assignment[lit.var] == lit.positive:
                        clause_satisfied = True
                        break
            
            if not clause_satisfied:
                return False
        
        return True

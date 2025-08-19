from typing import Dict, Optional
from .cnf import CNFFormula, Clause, Literal

class DPLLSolver:
    """Basic DPLL SAT solver (without modern CDCL features)"""
    
    def __init__(self):
        self.assignment: Dict[int, bool] = {}
        
    def unit_propagate(self, formula: CNFFormula) -> Optional[bool]:
        """Perform unit propagation"""
        changed = True
        while changed:
            changed = False
            for clause in formula.clauses:
                if clause.is_empty():
                    return False  # UNSAT
                    
                unassigned = []
                for lit in clause.literals:
                    if lit.var in self.assignment:
                        if self.assignment[lit.var] == lit.positive:
                            break  # Clause is satisfied
                    else:
                        unassigned.append(lit)
                else:  # Clause not satisfied
                    if len(unassigned) == 1:
                        lit = unassigned[0]
                        self.assignment[lit.var] = lit.positive
                        changed = True
                        
        return None  # No conclusion
        
    def solve(self, formula: CNFFormula) -> bool:
        """Solve CNF formula using DPLL algorithm"""
        # Unit propagation
        result = self.unit_propagate(formula)
        if result is not None:
            return result
            
        # All clauses satisfied?
        if all(any(self.assignment.get(lit.var) == lit.positive 
                  for lit in clause.literals)
               for clause in formula.clauses):
            return True
            
        # Choose variable to branch on
        for var in range(1, formula.num_vars + 1):
            if var not in self.assignment:
                # Try var = True
                self.assignment[var] = True
                if self.solve(formula):
                    return True
                    
                # Try var = False
                self.assignment[var] = False
                if self.solve(formula):
                    return True
                    
                del self.assignment[var]
                return False
                
        return True  # All variables assigned
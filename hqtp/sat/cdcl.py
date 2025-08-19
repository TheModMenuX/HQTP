
from typing import List, Set, Dict, Optional, Tuple
from .cnf import CNFFormula, Clause, Literal

class CDCLSolver:
    """Conflict-Driven Clause Learning SAT solver"""
    
    def __init__(self):
        self.formula = CNFFormula()
        self.assignment: Dict[int, bool] = {}  # Variable -> assignment
        self.decision_level: Dict[int, int] = {}  # Variable -> decision level
        self.antecedent: Dict[int, Optional[Clause]] = {}  # Variable -> antecedent clause
        self.level = 0
        self.decision_stack: List[int] = []
        
    def add_clauses(self, clauses):
        """Add clauses to the formula"""
        for clause in clauses:
            cnf_clause = self._convert_to_cnf_clause(clause)
            self.formula.add_clause(cnf_clause)
    
    def _convert_to_cnf_clause(self, clause) -> Clause:
        """Convert internal clause representation to CNF clause"""
        literals = []
        var_map = {}  # Map predicate names to variable numbers
        
        for lit in clause.literals:
            if lit.predicate not in var_map:
                var_map[lit.predicate] = len(var_map) + 1
            
            var = var_map[lit.predicate]
            cnf_lit = Literal(var, lit.positive)
            literals.append(cnf_lit)
        
        return Clause(literals)
    
    def solve(self) -> Optional[Dict[int, bool]]:
        """Main CDCL solving loop"""
        while True:
            conflict_clause = self.unit_propagation()
            
            if conflict_clause is not None:
                if self.level == 0:
                    return None  # UNSAT
                
                learned = self.analyze_conflict(conflict_clause)
                self.add_learned_clause(learned)
                self.backtrack(learned)
            else:
                if self.all_variables_assigned():
                    return self.assignment.copy()
                
                if not self.decide_next_branch():
                    return self.assignment.copy()
    
    def solve_partial(self) -> bool:
        """Partial solve for hybrid dispatch"""
        conflict_clause = self.unit_propagation()
        return conflict_clause is None
    
    def solve_step(self) -> bool:
        """Single solving step"""
        conflict_clause = self.unit_propagation()
        
        if conflict_clause is not None:
            if self.level == 0:
                return False  # UNSAT
            
            learned = self.analyze_conflict(conflict_clause)
            self.add_learned_clause(learned)
            self.backtrack(learned)
            return True
        
        if self.all_variables_assigned():
            return True
        
        return self.decide_next_branch()
    
    def unit_propagation(self) -> Optional[Clause]:
        """Perform unit propagation, return conflict clause if found"""
        changed = True
        
        while changed:
            changed = False
            
            for clause in self.formula.clauses:
                status = self.evaluate_clause(clause)
                
                if status == 'satisfied':
                    continue
                elif status == 'conflict':
                    return clause
                elif status == 'unit':
                    unit_lit = self.find_unit_literal(clause)
                    if unit_lit:
                        self.assign_variable(unit_lit.var, 
                                           unit_lit.positive, 
                                           clause)
                        changed = True
        
        return None
    
    def evaluate_clause(self, clause: Clause) -> str:
        """Evaluate clause status: satisfied, conflict, unit, or unresolved"""
        unassigned = []
        
        for lit in clause.literals:
            if lit.var not in self.assignment:
                unassigned.append(lit)
            elif self.assignment[lit.var] == lit.positive:
                return 'satisfied'
        
        if not unassigned:
            return 'conflict'
        elif len(unassigned) == 1:
            return 'unit'
        else:
            return 'unresolved'
    
    def find_unit_literal(self, clause: Clause) -> Optional[Literal]:
        """Find the unit literal in a unit clause"""
        for lit in clause.literals:
            if lit.var not in self.assignment:
                return lit
        return None
    
    def assign_variable(self, var: int, value: bool, antecedent: Optional[Clause]):
        """Assign variable with given value and antecedent"""
        self.assignment[var] = value
        self.decision_level[var] = self.level
        self.antecedent[var] = antecedent
    
    def decide_next_branch(self) -> bool:
        """Make next decision"""
        unassigned = [var for var in range(1, self.formula.num_vars + 1) 
                     if var not in self.assignment]
        
        if not unassigned:
            return False
        
        # Simple decision heuristic: pick first unassigned variable
        var = unassigned[0]
        self.level += 1
        self.assign_variable(var, True, None)
        self.decision_stack.append(var)
        
        return True
    
    def analyze_conflict(self, conflict_clause: Clause) -> Clause:
        """Analyze conflict and derive learned clause"""
        # Simplified conflict analysis - just return the conflict clause
        # TODO: Implement proper conflict analysis with resolution
        return conflict_clause
    
    def add_learned_clause(self, clause: Clause):
        """Add learned clause to formula"""
        self.formula.add_clause(clause)
    
    def backtrack(self, learned_clause: Clause):
        """Backtrack to appropriate decision level"""
        # Simple backtracking: go back one level
        if self.level > 0:
            self.level -= 1
            
            # Remove assignments from higher levels
            to_remove = [var for var, level in self.decision_level.items() 
                        if level > self.level]
            
            for var in to_remove:
                del self.assignment[var]
                del self.decision_level[var]
                del self.antecedent[var]
            
            if self.decision_stack:
                self.decision_stack.pop()
    
    def all_variables_assigned(self) -> bool:
        """Check if all variables are assigned"""
        return len(self.assignment) == self.formula.num_vars
    
    def get_model(self) -> Dict[int, bool]:
        """Get current satisfying assignment"""
        return self.assignment.copy()


from typing import Set, List, Optional
from .parser import Clause, Literal
from .unification import unify, apply_substitution

class ResolutionProver:
    def __init__(self, clauses: List[Clause]):
        self.usable: Set[Clause] = set()
        self.sos: Set[Clause] = set()  # Set of support
        self.used: Set[Clause] = set()
        
        # Separate goal clauses from axioms
        for clause in clauses:
            if self.is_goal_clause(clause):
                self.sos.add(clause)
            else:
                self.usable.add(clause)
    
    def is_goal_clause(self, clause: Clause) -> bool:
        """Heuristic to identify goal clauses (typically negated goals)"""
        # Simple heuristic: clauses with only negative literals might be goals
        return all(not lit.positive for lit in clause.literals)
    
    def resolve(self, clause1: Clause, clause2: Clause) -> List[Clause]:
        """Generate all possible resolvents between two clauses"""
        resolvents = []
        
        for i, lit1 in enumerate(clause1.literals):
            for j, lit2 in enumerate(clause2.literals):
                subst = unify(lit1, lit2)
                if subst is not None:
                    # Build resolvent
                    new_literals = []
                    
                    # Add remaining literals from clause1
                    for k, lit in enumerate(clause1.literals):
                        if k != i:
                            new_lit = self.apply_subst_to_literal(lit, subst)
                            new_literals.append(new_lit)
                    
                    # Add remaining literals from clause2
                    for k, lit in enumerate(clause2.literals):
                        if k != j:
                            new_lit = self.apply_subst_to_literal(lit, subst)
                            new_literals.append(new_lit)
                    
                    # Remove duplicates
                    new_literals = list(set(new_literals))
                    resolvent = Clause(new_literals)
                    resolvents.append(resolvent)
        
        return resolvents
    
    def apply_subst_to_literal(self, lit: Literal, subst: dict) -> Literal:
        """Apply substitution to a literal"""
        new_args = [apply_substitution(arg, subst) for arg in lit.args]
        return Literal(lit.positive, lit.predicate, new_args)
    
    def subsumes(self, clause1: Clause, clause2: Clause) -> bool:
        """Check if clause1 subsumes clause2"""
        if len(clause1.literals) > len(clause2.literals):
            return False
        
        # Try to find a substitution that makes clause1 a subset of clause2
        # Simplified implementation
        return False  # TODO: Implement proper subsumption
    
    def factor(self, clause: Clause) -> List[Clause]:
        """Generate factors of a clause by unifying literals"""
        factors = []
        
        for i in range(len(clause.literals)):
            for j in range(i + 1, len(clause.literals)):
                lit1, lit2 = clause.literals[i], clause.literals[j]
                
                if (lit1.positive == lit2.positive and 
                    lit1.predicate == lit2.predicate):
                    # Try to unify same-polarity literals
                    subst = {}
                    can_unify = True
                    
                    if len(lit1.args) == len(lit2.args):
                        for arg1, arg2 in zip(lit1.args, lit2.args):
                            from .unification import unify_terms
                            subst = unify_terms(arg1, arg2, subst)
                            if subst is None:
                                can_unify = False
                                break
                    
                    if can_unify and subst:
                        # Create factor
                        new_literals = []
                        for k, lit in enumerate(clause.literals):
                            if k != j:  # Skip the unified literal
                                new_lit = self.apply_subst_to_literal(lit, subst)
                                new_literals.append(new_lit)
                        
                        factors.append(Clause(new_literals))
        
        return factors
    
    def prove(self, max_steps: int = 1000) -> bool:
        """Main resolution loop with set-of-support strategy"""
        step = 0
        
        while self.sos and step < max_steps:
            # Select clause from SOS
            given = min(self.sos, key=lambda c: len(c.literals))  # Prefer shorter clauses
            self.sos.remove(given)
            self.used.add(given)
            
            # Empty clause found - proof complete
            if not given.literals:
                return True
            
            # Generate factors
            factors = self.factor(given)
            for factor in factors:
                if not factor.literals:  # Empty clause
                    return True
                self.sos.add(factor)
            
            # Generate resolvents with usable and used clauses
            for partner in self.usable | self.used:
                resolvents = self.resolve(given, partner)
                
                for resolvent in resolvents:
                    if not resolvent.literals:  # Empty clause
                        return True
                    
                    # Check if resolvent is new and non-redundant
                    if not any(self.subsumes(c, resolvent) 
                             for c in self.usable | self.sos | self.used):
                        self.sos.add(resolvent)
            
            step += 1
        
        return False

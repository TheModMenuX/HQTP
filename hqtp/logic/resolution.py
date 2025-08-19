from typing import List, Set, Tuple
from .parser import Clause, Literal
from .unification import unify

class ResolutionProver:
    def __init__(self):
        self.usable: Set[Clause] = set()
        self.sos: Set[Clause] = set()  # Set of support
        self.used: Set[Clause] = set()  # Already processed clauses
        
    def add_clause(self, clause: Clause, to_sos: bool = False):
        """Add a clause to usable or set-of-support"""
        if to_sos:
            self.sos.add(clause)
        else:
            self.usable.add(clause)
            
    def resolve(self, c1: Clause, c2: Clause) -> List[Clause]:
        """Try to resolve two clauses, return all possible resolvents"""
        results = []
        
        for l1 in c1.literals:
            for l2 in c2.literals:
                # Try to unify complementary literals
                if l1.positive != l2.positive and l1.predicate == l2.predicate:
                    subst = unify(l1, l2)
                    if subst is not None:
                        # Create resolvent by applying substitution
                        new_lits = []
                        for lit in c1.literals + c2.literals:
                            if lit != l1 and lit != l2:
                                new_lits.append(lit.apply_subst(subst))
                        results.append(Clause(new_lits))
        
        return results
    
    def subsumes(self, c1: Clause, c2: Clause) -> bool:
        """Check if c1 subsumes c2"""
        # TODO: Implement subsumption checking
        pass
        
    def factor(self, clause: Clause) -> List[Clause]:
        """Generate factors of a clause by unifying literals"""
        # TODO: Implement factoring
        pass
        
    def prove(self, max_steps: int = 1000) -> bool:
        """Main resolution loop with set-of-support strategy"""
        step = 0
        
        while self.sos and step < max_steps:
            # Select clause from SOS
            given = min(self.sos, key=len)  # Prefer shorter clauses
            self.sos.remove(given)
            self.used.add(given)
            
            # Empty clause found - proof complete
            if not given.literals:
                return True
                
            # Generate resolvents with usable and used clauses
            for partner in self.usable | self.used:
                resolvents = self.resolve(given, partner)
                
                for resolvent in resolvents:
                    # Check if resolvent is new and non-redundant
                    if not any(self.subsumes(c, resolvent) 
                             for c in self.usable | self.sos | self.used):
                        self.sos.add(resolvent)
            
            step += 1
            
        return False
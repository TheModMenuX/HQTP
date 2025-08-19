from typing import List
from .parser import Clause, Literal, Term

def standardize_apart(clauses: List[Clause]) -> List[Clause]:
    """Rename variables to ensure no variable names are shared between clauses"""
    counter = 0
    result = []
    
    for clause in clauses:
        var_map = {}  # Original var name -> New var name
        new_lits = []
        
        for lit in clause.literals:
            new_args = []
            for arg in lit.args:
                if arg.kind == 'var':
                    if arg.name not in var_map:
                        var_map[arg.name] = f"V{counter}"
                        counter += 1
                    new_args.append(Term('var', var_map[arg.name]))
                else:
                    new_args.append(arg)
            new_lits.append(Literal(lit.positive, lit.predicate, new_args))
            
        result.append(Clause(new_lits))
    return result

def to_cnf(clauses: List[Clause]) -> List[Clause]:
    """Convert clauses to Conjunctive Normal Form"""
    # TODO: Implement CNF conversion
    # 1. Eliminate implications
    # 2. Move negations inward
    # 3. Distribute OR over AND
    pass
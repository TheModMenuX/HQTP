
from typing import Dict, Any
from ..logic.parser import Clause, Literal, Term

def lift_sat_model(sat_model: Dict[int, bool]) -> Dict[str, Any]:
    """
    Lift a propositional SAT model to first-order interpretation
    
    Args:
        sat_model: Variable assignments from SAT solver
    
    Returns:
        First-order model interpretation
    """
    interpretation = {
        'predicates': {},
        'functions': {},
        'constants': {}
    }
    
    # Map SAT variables back to predicates
    # This is a simplified mapping - in practice would need
    # to track the encoding used in clausification
    
    for var, value in sat_model.items():
        # Assume variable names encode predicate information
        predicate_name = f"p_{var}"
        interpretation['predicates'][predicate_name] = value
    
    return interpretation

def herbrand_interpretation(clauses: list) -> Dict[str, Any]:
    """
    Construct Herbrand interpretation from clauses
    
    Args:
        clauses: List of first-order clauses
    
    Returns:
        Herbrand interpretation
    """
    # Collect all constants and function symbols
    constants = set()
    functions = set()
    predicates = set()
    
    for clause in clauses:
        for literal in clause.literals:
            predicates.add(literal.predicate)
            
            for arg in literal.args:
                if arg.kind == 'const':
                    constants.add(arg.name)
                elif arg.kind == 'func':
                    functions.add((arg.name, len(arg.args)))
    
    # If no constants, add one
    if not constants:
        constants.add('a')
    
    return {
        'domain': list(constants),
        'predicates': {p: set() for p in predicates},
        'functions': {f: {} for f in functions},
        'constants': {c: c for c in constants}
    }

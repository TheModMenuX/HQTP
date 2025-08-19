
from typing import Dict, Optional, List
from .parser import Term, Literal

def occurs_check(var: Term, term: Term) -> bool:
    """Check if variable occurs in term (prevents infinite structures)"""
    if term.kind == 'var':
        return var.name == term.name
    elif term.kind == 'func':
        return any(occurs_check(var, arg) for arg in term.args)
    return False

def unify_terms(term1: Term, term2: Term, subst: Dict[str, Term] = None) -> Optional[Dict[str, Term]]:
    """Unify two terms, returning substitution or None if impossible"""
    if subst is None:
        subst = {}
    
    # Apply existing substitution
    term1 = apply_substitution(term1, subst)
    term2 = apply_substitution(term2, subst)
    
    # Same term
    if term1.kind == term2.kind == 'const' and term1.name == term2.name:
        return subst
    
    # Variable unification
    if term1.kind == 'var':
        if term1.name in subst:
            return unify_terms(subst[term1.name], term2, subst)
        elif occurs_check(term1, term2):
            return None
        else:
            subst[term1.name] = term2
            return subst
    
    if term2.kind == 'var':
        return unify_terms(term2, term1, subst)
    
    # Function unification
    if (term1.kind == term2.kind == 'func' and 
        term1.name == term2.name and 
        len(term1.args) == len(term2.args)):
        
        for arg1, arg2 in zip(term1.args, term2.args):
            subst = unify_terms(arg1, arg2, subst)
            if subst is None:
                return None
        return subst
    
    return None

def apply_substitution(term: Term, subst: Dict[str, Term]) -> Term:
    """Apply substitution to a term"""
    if term.kind == 'var' and term.name in subst:
        return apply_substitution(subst[term.name], subst)
    elif term.kind == 'func':
        new_args = [apply_substitution(arg, subst) for arg in term.args]
        return Term(term.kind, term.name, new_args)
    return term

def unify(lit1: Literal, lit2: Literal) -> Optional[Dict[str, Term]]:
    """Unify two literals if they have opposite polarity and same predicate"""
    if (lit1.positive == lit2.positive or 
        lit1.predicate != lit2.predicate or
        len(lit1.args) != len(lit2.args)):
        return None
    
    subst = {}
    for arg1, arg2 in zip(lit1.args, lit2.args):
        subst = unify_terms(arg1, arg2, subst)
        if subst is None:
            return None
    
    return subst

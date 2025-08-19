from typing import Dict, Optional
from .parser import Term, Literal

def occurs_check(var: Term, term: Term) -> bool:
    """Check if variable occurs in term"""
    if term.kind == 'var':
        return var.name == term.name
    elif term.kind in ('const', 'func'):
        if term.args:
            return any(occurs_check(var, arg) for arg in term.args)
        return False

def unify(t1: Term, t2: Term, subst: Dict[str, Term] = None) -> Optional[Dict[str, Term]]:
    """Robinson's unification algorithm with occurs check"""
    if subst is None:
        subst = {}
        
    if t1.kind == 'var':
        if t1.name in subst:
            return unify(subst[t1.name], t2, subst)
        if occurs_check(t1, t2):
            return None
        subst[t1.name] = t2
        return subst
        
    if t2.kind == 'var':
        return unify(t2, t1, subst)
        
    if t1.kind != t2.kind or t1.name != t2.name:
        return None
        
    if t1.args and t2.args:
        if len(t1.args) != len(t2.args):
            return None
        for a1, a2 in zip(t1.args, t2.args):
            subst = unify(a1, a2, subst)
            if subst is None:
                return None
    return subst
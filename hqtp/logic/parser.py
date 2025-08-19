
from dataclasses import dataclass
from typing import List, Union, Dict
import re

@dataclass
class Term:
    kind: str  # 'var', 'const', or 'func'
    name: str
    args: List['Term'] = None

    def __post_init__(self):
        if self.args is None:
            self.args = []

@dataclass
class Literal:
    positive: bool
    predicate: str
    args: List[Term]

@dataclass
class Clause:
    literals: List[Literal]

def parse_term(term_str: str) -> Term:
    """Parse a term from string representation"""
    term_str = term_str.strip()
    
    # Variable (starts with uppercase or contains underscore)
    if term_str[0].isupper() or '_' in term_str:
        return Term('var', term_str)
    
    # Function/constant
    if '(' in term_str:
        name = term_str[:term_str.index('(')]
        args_str = term_str[term_str.index('(')+1:-1]
        args = []
        if args_str.strip():
            # Simple comma split (doesn't handle nested functions perfectly)
            for arg in args_str.split(','):
                args.append(parse_term(arg.strip()))
        return Term('func', name, args)
    else:
        return Term('const', term_str)

def parse_literal(lit_str: str) -> Literal:
    """Parse a literal from string representation"""
    lit_str = lit_str.strip()
    positive = True
    
    if lit_str.startswith('~') or lit_str.startswith('\\+'):
        positive = False
        lit_str = lit_str[1:].strip()
    
    if '(' in lit_str:
        predicate = lit_str[:lit_str.index('(')]
        args_str = lit_str[lit_str.index('(')+1:-1]
        args = []
        if args_str.strip():
            for arg in args_str.split(','):
                args.append(parse_term(arg.strip()))
    else:
        predicate = lit_str
        args = []
    
    return Literal(positive, predicate, args)

def parse_tptp(input_str: str) -> List[Clause]:
    """Parse TPTP format into internal clause representation"""
    clauses = []
    
    # Remove comments and split into lines
    lines = []
    for line in input_str.split('\n'):
        line = line.strip()
        if line and not line.startswith('%'):
            lines.append(line)
    
    for line in lines:
        if line.startswith('cnf('):
            # Extract the formula part
            formula_start = line.find(',', line.find(',') + 1) + 1
            formula_end = line.rfind(')')
            formula = line[formula_start:formula_end].strip()
            
            # Parse disjunction of literals
            literals = []
            if '|' in formula:
                lit_strs = formula.split('|')
            else:
                lit_strs = [formula]
            
            for lit_str in lit_strs:
                literals.append(parse_literal(lit_str.strip()))
            
            clauses.append(Clause(literals))
    
    return clauses

def parse_smtlib(input_str: str) -> List[Clause]:
    """Parse SMT-LIB format into internal clause representation"""
    # Simplified SMT-LIB parser for basic propositional logic
    clauses = []
    
    # Find assert statements
    assert_pattern = r'\(assert\s+([^)]+)\)'
    matches = re.findall(assert_pattern, input_str)
    
    for match in matches:
        # Convert SMT-LIB to clause form (very simplified)
        formula = match.strip()
        
        # Handle basic OR statements
        if formula.startswith('(or'):
            lit_strs = re.findall(r'(\w+|\(not\s+\w+\))', formula)
            literals = []
            
            for lit_str in lit_strs:
                if lit_str.startswith('(not'):
                    pred = re.search(r'not\s+(\w+)', lit_str).group(1)
                    literals.append(Literal(False, pred, []))
                else:
                    literals.append(Literal(True, lit_str, []))
            
            clauses.append(Clause(literals))
        else:
            # Single literal
            if formula.startswith('(not'):
                pred = re.search(r'not\s+(\w+)', formula).group(1)
                literals = [Literal(False, pred, [])]
            else:
                literals = [Literal(True, formula, [])]
            
            clauses.append(Clause(literals))
    
    return clauses

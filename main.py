
from hqtp.logic.parser import parse_tptp
from hqtp.logic.resolution import ResolutionProver
from hqtp.sat.cdcl import CDCLSolver
from hqtp.quantum.grover import grover_search

def demo_resolution():
    """Demonstrate resolution theorem proving"""
    print("=== Resolution Theorem Proving Demo ===")
    
    # Sample TPTP problem
    tptp_input = """
    cnf(clause1, axiom, (p | q)).
    cnf(clause2, axiom, (~p | r)).
    cnf(clause3, axiom, (~q | r)).
    cnf(clause4, negated_conjecture, (~r)).
    """
    
    clauses = parse_tptp(tptp_input)
    prover = ResolutionProver(clauses)
    
    result = prover.prove()
    print(f"Resolution result: {'PROVED' if result else 'NOT PROVED'}")

def demo_sat():
    """Demonstrate SAT solving"""
    print("\n=== SAT Solving Demo ===")
    
    solver = CDCLSolver()
    
    # Add some clauses manually for demo
    from hqtp.sat.cnf import Clause, Literal
    
    # (p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ r) ∧ ¬r
    clause1 = Clause([Literal(1, True), Literal(2, True)])      # p ∨ q
    clause2 = Clause([Literal(1, False), Literal(3, True)])     # ¬p ∨ r
    clause3 = Clause([Literal(2, False), Literal(3, True)])     # ¬q ∨ r
    clause4 = Clause([Literal(3, False)])                       # ¬r
    
    solver.formula.add_clause(clause1)
    solver.formula.add_clause(clause2)
    solver.formula.add_clause(clause3)
    solver.formula.add_clause(clause4)
    
    result = solver.solve()
    print(f"SAT result: {'SAT' if result else 'UNSAT'}")
    if result:
        print(f"Model: {result}")

def demo_quantum():
    """Demonstrate quantum search"""
    print("\n=== Quantum Search Demo ===")
    
    # Simple 3-SAT oracle
    def sat_oracle(assignment):
        # (x1 ∨ x2 ∨ ¬x3) ∧ (¬x1 ∨ x3) ∧ (x2 ∨ x3)
        x1, x2, x3 = assignment
        clause1 = x1 or x2 or not x3
        clause2 = not x1 or x3
        clause3 = x2 or x3
        return clause1 and clause2 and clause3
    
    result = grover_search(3, sat_oracle, max_iterations=2)
    print(f"Quantum search result: {result}")
    
    if result:
        print(f"Oracle verification: {sat_oracle(result)}")

def main():
    print("Hybrid Quantum-Guided Theorem Prover Demo")
    print("=========================================")
    
    try:
        demo_resolution()
        demo_sat()
        demo_quantum()
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

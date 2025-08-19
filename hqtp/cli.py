import argparse
from pathlib import Path
from .logic.parser import parse_tptp, parse_smtlib
from .bridge.dispatcher import HybridDispatcher

def main():
    parser = argparse.ArgumentParser(description='Hybrid Quantum-Guided Theorem Prover')
    parser.add_argument('input', type=Path, help='Input file (TPTP or SMT-LIB format)')
    parser.add_argument('--quantum', action='store_true', help='Enable quantum acceleration')
    parser.add_argument('--learning', action='store_true', help='Enable learned guidance')
    args = parser.parse_args()
    
    # Parse input
    if args.input.suffix == '.p':
        clauses = parse_tptp(args.input.read_text())
    else:
        clauses = parse_smtlib(args.input.read_text())
        
    # Initialize prover
    dispatcher = HybridDispatcher(
        max_quantum_vars=14,  # Default max qubits
        use_quantum=args.quantum,
        use_learning=args.learning
    )
    
    # Run proof search
    result = dispatcher.solve(clauses)
    
    if result is True:
        print("Theorem proved!")
    elif result is False:
        print("Counter-example found!")
    else:
        print("Proof attempt exhausted")

if __name__ == '__main__':
    main()
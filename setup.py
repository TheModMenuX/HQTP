from setuptools import setup, find_packages

setup(
    name="hqtp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "torch>=1.9.0",
        "qiskit>=0.34.0",  # For quantum simulation
        "networkx>=2.6.0",  # For graph algorithms
    ],
    entry_points={
        'console_scripts': [
            'hqtp=hqtp.cli:main',
        ],
    },
    author="lionking-ai",
    description="Hybrid Quantum-Guided Theorem Prover",
    python_requires=">=3.8",
)
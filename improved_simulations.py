# Import necessary libraries
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys

# Function to ensure required libraries are installed
def ensure_libraries_installed():
    print("Checking and installing missing libraries...")
    required_libraries = ["qiskit", "numpy", "matplotlib"]
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Quantum State Evolution Example
def simulate_quantum_state_evolution():
    """
    Simulate the time evolution of a quantum state using a simple quantum circuit.
    """
    print("Simulating Quantum State Evolution...")
    try:
        # Create a simple quantum circuit
        qc = QuantumCircuit(1)
        qc.h(0)  # Apply Hadamard gate to create superposition
        qc.measure_all()
        
        # Visualize the circuit
        print("Quantum Circuit:")
        print(qc.draw())

        # Simulate the circuit
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()
        
        # Plot results
        plot_histogram(counts)
        plt.title("Quantum State Evolution")
        plt.show()
    except Exception as e:
        print(f"Error during quantum state evolution simulation: {e}")

# Quantum Gates and Circuits Example
def create_and_test_quantum_circuit():
    """
    Create and test a quantum circuit for Grover's algorithm.
    """
    print("Creating and Testing Quantum Circuit...")
    try:
        # Grover's Algorithm Example
        qc = QuantumCircuit(3)
        qc.h([0, 1, 2])  # Apply Hadamard gates to all qubits
        qc.cz(0, 1)      # Controlled-Z gate
        qc.h([0, 1, 2])  # Apply Hadamard gates again
        qc.measure_all()
        
        # Visualize the circuit
        print("Quantum Circuit:")
        print(qc.draw())

        # Simulate the circuit
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()
        
        # Plot results
        plot_histogram(counts)
        plt.title("Quantum Gates and Circuits (Grover's Algorithm)")
        plt.show()
    except Exception as e:
        print(f"Error during quantum circuit simulation: {e}")

# Expanded Quantum Key Distribution Example (BB84 Protocol)
def simulate_quantum_key_distribution():
    """
    Simulate a Quantum Key Distribution (QKD) protocol (BB84).
    """
    print("Simulating Quantum Key Distribution (BB84 Protocol)...")
    try:
        # BB84 Protocol Example
        qc = QuantumCircuit(2)
        qc.h(0)          # Apply Hadamard gate to create superposition
        qc.cx(0, 1)      # Create entanglement
        qc.measure_all()
        
        # Visualize the circuit
        print("Quantum Circuit:")
        print(qc.draw())

        # Simulate the circuit
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()
        
        # Plot results
        plot_histogram(counts)
        plt.title("Quantum Cryptography (QKD - BB84 Protocol)")
        plt.show()
    except Exception as e:
        print(f"Error during QKD simulation: {e}")

# Main function to execute simulations
if __name__ == "__main__":
    print("Setting up the environment...")
    ensure_libraries_installed()

    # Run simulations
    simulate_quantum_state_evolution()
    create_and_test_quantum_circuit()
    simulate_quantum_key_distribution()
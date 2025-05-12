# Enhanced Cryptography Example (Quantum Key Distribution Simulation - BB84 Protocol)
def simulate_quantum_key_distribution_bb84():
    """
    Simulate a Quantum Key Distribution (QKD) protocol (BB84) with basis selection and key reconciliation.
    """
    print("Simulating Quantum Key Distribution (BB84 Protocol)...")
    
    # Number of qubits (representing bits in the key)
    num_bits = 10
    
    # Step 1: Generate random bits and bases for Alice
    alice_bits = np.random.randint(2, size=num_bits)  # Random bits (0 or 1)
    alice_bases = np.random.randint(2, size=num_bits)  # Random bases (0 = Z, 1 = X)
    
    # Step 2: Prepare qubits based on Alice's bits and bases
    qc = QuantumCircuit(num_bits, num_bits)
    for i in range(num_bits):
        if alice_bits[i] == 1:
            qc.x(i)  # Apply X gate for bit 1
        if alice_bases[i] == 1:
            qc.h(i)  # Apply H gate for X basis
    
    # Step 3: Bob randomly chooses measurement bases
    bob_bases = np.random.randint(2, size=num_bits)  # Random bases (0 = Z, 1 = X)
    for i in range(num_bits):
        if bob_bases[i] == 1:
            qc.h(i)  # Apply H gate for X basis measurement
    
    # Step 4: Measure all qubits
    qc.measure(range(num_bits), range(num_bits))
    
    # Simulate the circuit
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, simulator, shots=1).result()
    counts = result.get_counts()
    measured_bits = list(counts.keys())[0]  # Extract the measured bitstring
    
    # Step 5: Key reconciliation (compare bases)
    key = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:  # Keep bits where bases match
            key.append(int(measured_bits[num_bits - i - 1]))  # Reverse bit order
    
    # Display results
    print(f"Alice's Bits:    {alice_bits}")
    print(f"Alice's Bases:   {alice_bases}")
    print(f"Bob's Bases:     {bob_bases}")
    print(f"Measured Bits:   {measured_bits}")
    print(f"Final Key:       {key}")

# Call the enhanced QKD simulation
simulate_quantum_key_distribution_bb84()
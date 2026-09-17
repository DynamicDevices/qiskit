"""Three small, inspectable Qiskit experiments for the public demo."""

import math
import random

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def grover_search(items: int, marked: int, iterations: int) -> dict:
    """Mark one basis state and apply Grover's diffuser zero or more times."""
    qubits = items.bit_length() - 1
    circuit = QuantumCircuit(qubits)
    circuit.h(range(qubits))
    for _ in range(iterations):
        for qubit in range(qubits):
            if not (marked >> qubit) & 1:
                circuit.x(qubit)
        circuit.h(qubits - 1)
        circuit.mcx(list(range(qubits - 1)), qubits - 1)
        circuit.h(qubits - 1)
        for qubit in range(qubits):
            if not (marked >> qubit) & 1:
                circuit.x(qubit)
        circuit.h(range(qubits))
        circuit.x(range(qubits))
        circuit.h(qubits - 1)
        circuit.mcx(list(range(qubits - 1)), qubits - 1)
        circuit.h(qubits - 1)
        circuit.x(range(qubits))
        circuit.h(range(qubits))
    probabilities = Statevector.from_instruction(circuit).probabilities_dict()
    return {
        "probabilities": {format(item, f"0{qubits}b"): float(probabilities.get(format(item, f"0{qubits}b"), 0)) for item in range(items)},
        "success": float(probabilities.get(format(marked, f"0{qubits}b"), 0)),
        "circuit": str(circuit.draw(output="text", fold=100)),
    }


def repetition_code(bit: int, error_percent: int, shots: int, seed: int) -> dict:
    """Encode one classical bit across three qubits; correct one X error by majority."""
    outcomes = {}
    example = None
    for mask in range(8):
        circuit = QuantumCircuit(3)
        if bit:
            circuit.x(0)
        circuit.cx(0, 1)
        circuit.cx(0, 2)
        for qubit in range(3):
            if (mask >> qubit) & 1:
                circuit.x(qubit)
        probabilities = Statevector.from_instruction(circuit).probabilities_dict()
        outcome = max(probabilities, key=probabilities.get)
        outcomes[mask] = outcome
        if mask == 2:
            circuit.measure_all()
            example = str(circuit.draw(output="text", fold=100))
    rng = random.Random(seed)
    direct_errors = coded_errors = 0
    p = error_percent / 100
    for _ in range(shots):
        mask = sum((1 << qubit) for qubit in range(3) if rng.random() < p)
        measured = outcomes[mask]
        direct_errors += int(measured[-1] != str(bit))
        coded_errors += int((sum(digit == "1" for digit in measured) >= 2) != bit)
    return {
        "direct_errors": direct_errors,
        "coded_errors": coded_errors,
        "direct_rate": direct_errors / shots,
        "coded_rate": coded_errors / shots,
        "ideal_direct_rate": p,
        "ideal_coded_rate": 3 * p * p - 2 * p * p * p,
        "circuit": example,
    }


TOPOLOGIES = {
    "Chain": [(0, 1), (1, 2), (2, 3)],
    "Ring": [(0, 1), (1, 2), (2, 3), (3, 0)],
    "Star": [(0, 1), (0, 2), (0, 3)],
}


def sensor_allocation(topology: str, gamma_degrees: int, beta_degrees: int, layers: int) -> dict:
    """One or two QAOA layers for assigning four devices to two channels."""
    edges = TOPOLOGIES[topology]
    gamma = math.radians(gamma_degrees)
    beta = math.radians(beta_degrees)
    circuit = QuantumCircuit(4)
    circuit.h(range(4))
    for _ in range(layers):
        for first, second in edges:
            circuit.rzz(-gamma, first, second)
        for qubit in range(4):
            circuit.rx(2 * beta, qubit)
    probabilities = Statevector.from_instruction(circuit).probabilities_dict()
    scores = {}
    for allocation in range(16):
        label = format(allocation, "04b")
        scores[label] = sum(((allocation >> first) & 1) != ((allocation >> second) & 1) for first, second in edges)
    best_score = max(scores.values())
    best_labels = [label for label, score in scores.items() if score == best_score]
    expected = sum(float(probabilities.get(label, 0)) * score for label, score in scores.items())
    optimal_probability = sum(float(probabilities.get(label, 0)) for label in best_labels)
    ranked = sorted(scores, key=lambda label: float(probabilities.get(label, 0)), reverse=True)[:8]
    return {
        "edges": [["ABCD"[a], "ABCD"[b]] for a, b in edges],
        "best_score": best_score,
        "best_labels": best_labels,
        "expected_score": expected,
        "random_expected": len(edges) / 2,
        "optimal_probability": optimal_probability,
        "top_probabilities": {label: float(probabilities.get(label, 0)) for label in ranked},
        "circuit": str(circuit.draw(output="text", fold=100)),
    }

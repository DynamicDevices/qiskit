"""Small, reproducible quantum communication experiments built with Qiskit."""

import math
import random
from functools import lru_cache

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


@lru_cache(maxsize=8)
def probability_one(bit: int, prepared_basis: str, measured_basis: str) -> float:
    """Use Qiskit to find the probability of measuring 1 in the chosen basis."""
    circuit = QuantumCircuit(1)
    if bit:
        circuit.x(0)
    if prepared_basis == "X":
        circuit.h(0)
    if measured_basis == "X":
        circuit.h(0)
    return float(Statevector.from_instruction(circuit).probabilities()[1])


def simulate_bb84(rounds: int, intercept_percent: int, seed: int) -> dict:
    """Simulate ideal-channel BB84 with optional intercept and resend by Eve."""
    rng = random.Random(seed)
    transmissions = [
        (rng.randrange(2), rng.choice(("Z", "X")), rng.choice(("Z", "X")),
         rng.choice(("Z", "X")), rng.random() * 100 < intercept_percent)
        for _ in range(rounds)
    ]
    rows = []
    sifted = errors = intercepted = 0

    for alice_bit, alice_basis, bob_basis, eve_basis, eve_present in transmissions:
        sent_bit, sent_basis = alice_bit, alice_basis
        if eve_present:
            intercepted += 1
            eve_bit = int(rng.random() < probability_one(sent_bit, sent_basis, eve_basis))
            sent_bit, sent_basis = eve_bit, eve_basis
        bob_bit = int(rng.random() < probability_one(sent_bit, sent_basis, bob_basis))
        kept = alice_basis == bob_basis
        if kept:
            sifted += 1
            errors += alice_bit != bob_bit
        if len(rows) < 16:
            rows.append(
                {
                    "Alice bit": alice_bit,
                    "Alice basis": alice_basis,
                    "Eve basis": eve_basis if eve_present else "—",
                    "Bob basis": bob_basis,
                    "Bob bit": bob_bit,
                    "Kept?": "Yes" if kept else "No",
                    "Different?": "Yes" if kept and alice_bit != bob_bit else "No",
                }
            )

    return {
        "rounds": rounds,
        "intercepted": intercepted,
        "sifted": sifted,
        "errors": errors,
        "qber": errors / sifted if sifted else 0.0,
        "rows": rows,
    }


def teleportation_circuit(theta_degrees: int, phi_degrees: int, corrections: bool) -> QuantumCircuit:
    """Teleport qubit 0 to qubit 2, then undo its preparation to verify it."""
    theta = math.radians(theta_degrees)
    phi = math.radians(phi_degrees)
    circuit = QuantumCircuit(3, 3)
    circuit.ry(theta, 0)
    circuit.rz(phi, 0)
    circuit.barrier()
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.barrier()
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    if corrections:
        with circuit.if_test((circuit.clbits[1], 1)):
            circuit.x(2)
        with circuit.if_test((circuit.clbits[0], 1)):
            circuit.z(2)
    circuit.barrier()
    circuit.rz(-phi, 2)
    circuit.ry(-theta, 2)
    circuit.measure(2, 2)
    return circuit


def simulate_teleportation(theta_degrees: int, phi_degrees: int, shots: int, seed: int) -> dict:
    """Compare Bob's state with and without the two classical corrections."""
    theta = math.radians(theta_degrees)
    phi = math.radians(phi_degrees)
    preparation = QuantumCircuit(3)
    preparation.ry(theta, 0)
    preparation.rz(phi, 0)
    preparation.h(1)
    preparation.cx(1, 2)
    preparation.cx(0, 1)
    preparation.h(0)
    amplitudes = Statevector.from_instruction(preparation).data
    verification = QuantumCircuit(1)
    verification.rz(-phi, 0)
    verification.ry(-theta, 0)
    rng = random.Random(seed)
    results = {}
    for corrections in (False, True):
        circuit = teleportation_circuit(theta_degrees, phi_degrees, corrections)
        probabilities = {}
        for alice_bit in (0, 1):
            for pair_bit in (0, 1):
                branch = [amplitudes[alice_bit + 2 * pair_bit + 4 * bob_bit] for bob_bit in (0, 1)]
                branch_weight = sum(abs(value) ** 2 for value in branch)
                if not branch_weight:
                    continue
                bob = [value / math.sqrt(branch_weight) for value in branch]
                if corrections and pair_bit:
                    bob.reverse()
                if corrections and alice_bit:
                    bob[1] = -bob[1]
                checked = Statevector(bob).evolve(verification).probabilities()
                for bob_bit in (0, 1):
                    # Qiskit displays classical bits in the order c2 c1 c0.
                    key = f"{bob_bit}{pair_bit}{alice_bit}"
                    probabilities[key] = branch_weight * float(checked[bob_bit])
        labels = list(probabilities)
        samples = rng.choices(labels, weights=[probabilities[label] for label in labels], k=shots)
        counts = {label: samples.count(label) for label in labels if label in samples}
        # With one classical register, count keys are c2 c1 c0. c2 is Bob's check bit.
        matches = sum(count for bits, count in counts.items() if bits[0] == "0")
        results["with_corrections" if corrections else "without_corrections"] = {
            "matches": matches,
            "rate": matches / shots,
            "counts": counts,
            "circuit": circuit,
        }
    return results

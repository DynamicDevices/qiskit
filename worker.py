"""Run Qiskit calculations in a fresh process for each distinct demo setting."""

import json
import math
import random
import sys

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from experiments import simulate_bb84, simulate_teleportation


def entanglement(angle: int, entangle_qubits: bool, shots: int) -> dict:
    circuit = QuantumCircuit(2, 2)
    circuit.ry(math.radians(angle), 0)
    if entangle_qubits:
        circuit.cx(0, 1)
    probabilities = Statevector.from_instruction(circuit).probabilities_dict()
    circuit.measure([0, 1], [0, 1])
    labels = ["00", "01", "10", "11"]
    samples = random.Random(7).choices(
        labels, weights=[probabilities.get(label, 0) for label in labels], k=shots
    )
    return {
        "counts": {label: samples.count(label) for label in labels},
        "circuit": str(circuit.draw(output="text")),
    }


def main() -> None:
    request = json.loads(sys.argv[1])
    view = request.pop("view")
    if view == "entanglement":
        result = entanglement(**request)
    elif view == "bb84":
        result = simulate_bb84(**request)
    elif view == "teleportation":
        result = simulate_teleportation(**request)
        for run in result.values():
            run["circuit"] = str(run["circuit"].draw(output="text", fold=80))
    else:
        raise ValueError(f"Unknown experiment: {view}")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

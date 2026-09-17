"""A small, shareable Qiskit experiment using a local simulator."""

import math

import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


st.set_page_config(page_title="Qiskit: entanglement in two qubits", page_icon="⚛️")
st.title("Entanglement in two qubits")
st.caption("An interactive Qiskit experiment")

st.write(
    "Rotate the first qubit, optionally entangle it with a second one, and "
    "measure both. The bars are samples from Qiskit's local simulator."
)

angle = st.slider("Rotation angle (degrees)", 0, 180, 90, 15)
entangle = st.toggle("Apply entangling CNOT gate", value=True)
shots = st.select_slider("Measurements", options=[100, 500, 1000, 2000, 5000], value=1000)

circuit = QuantumCircuit(2, 2)
circuit.ry(math.radians(angle), 0)
if entangle:
    circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])

simulator = AerSimulator()
result = simulator.run(transpile(circuit, simulator), shots=shots).result()
counts = result.get_counts()
labels = ["00", "01", "10", "11"]
probabilities = {label: counts.get(label, 0) / shots for label in labels}

st.bar_chart(
    {"Outcome": labels, "Measured fraction": list(probabilities.values())},
    x="Outcome",
    y="Measured fraction",
)
st.write("Counts:", {label: counts.get(label, 0) for label in labels})

with st.expander("Circuit and interpretation"):
    st.code(str(circuit.draw(output="text")), language="text")
    st.write(
        "Qiskit displays bit 1 on the left and bit 0 on the right. At 90° with "
        "CNOT enabled, the ideal circuit produces 00 and 11 about half the time "
        "each. Turn CNOT off to see the first qubit vary independently."
    )

st.info(
    "This runs on a classical simulator. It demonstrates quantum circuit behaviour "
    "but does not execute on IBM quantum hardware or show a computational advantage."
)
st.markdown(
    "[Qiskit documentation](https://quantum.cloud.ibm.com/docs/en/guides) · "
    "[Run a first circuit on IBM hardware](https://quantum.cloud.ibm.com/docs/en/guides/hello-world)"
)

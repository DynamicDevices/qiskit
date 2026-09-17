"""Dynamic Devices' shareable Qiskit experiments."""

import math

import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


st.set_page_config(page_title="Qiskit | Dynamic Devices", page_icon="⚛️", layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Sora:wght@600;800&family=Space+Grotesk:wght@500;600&display=swap');
    .stApp { background: #0B1C2C; color: #F3F6F9; font-family: 'IBM Plex Sans', sans-serif; }
    .block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 4rem; }
    h1, h2, h3 { font-family: 'Sora', sans-serif; letter-spacing: -.035em; }
    h1 { font-size: clamp(2.7rem, 6vw, 5.2rem) !important; line-height: 1.05; }
    h2 { font-size: clamp(1.6rem, 3vw, 2.4rem) !important; }
    p, li { font-family: 'IBM Plex Sans', sans-serif; }
    .eyebrow { color: #A9C99A; font: 600 .78rem 'Space Grotesk', sans-serif;
       letter-spacing: .16em; text-transform: uppercase; margin: 0 0 1rem; }
    .hero-lede { max-width: 690px; color: #D7E2EC; font-size: 1.25rem; line-height: 1.65; }
    .hero-rule { height: 3px; width: 74px; background: linear-gradient(90deg,#6DB33F,#E88A3C);
       border-radius: 3px; margin: 1.3rem 0 1.8rem; }
    .section-intro { color: #B9C8D4; max-width: 700px; }
    .demo-card { min-height: 215px; border: 1px solid #3D5364; border-radius: 18px;
       background: #12293C; padding: 1.5rem; margin-bottom: .7rem; }
    .demo-card h3 { margin: .6rem 0 .7rem; font-size: 1.27rem; }
    .demo-card p { color: #C5D0D9; line-height: 1.55; margin: 0; }
    .chip { display: inline-block; border-radius: 100px; padding: .28rem .62rem;
       color: #D9F1CB; background: #26472E; font: 600 .72rem 'Space Grotesk', sans-serif;
       letter-spacing: .06em; text-transform: uppercase; }
    .chip.soon { color: #D2DCE5; background: #304354; }
    .fine-print { border-top: 1px solid #3D5364; padding-top: 1.4rem; margin-top: 3rem;
       color: #B9C8D4; font-size: .9rem; line-height: 1.6; }
    .stButton button[kind='primary'] { background: #6DB33F; color: #0B1C2C;
       border: 0; font-family: 'Space Grotesk', sans-serif; font-weight: 600; }
    .stButton button[kind='primary']:hover { background: #80C74F; color: #0B1C2C; }
    .stButton button[kind='secondary'] { border-color: #6DB33F; color: #F3F6F9;
       font-family: 'Space Grotesk', sans-serif; }
    a { color: #A9DC87 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def go_to(view: str) -> None:
    st.query_params["view"] = view


def brand_header() -> None:
    st.image("assets/dd-lockup.svg", width=300)


def landing() -> None:
    brand_header()
    st.markdown('<div class="hero-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Dynamic Devices / experiments</div>', unsafe_allow_html=True)
    st.title("Qiskit")
    st.markdown(
        '<p class="hero-lede">Quantum computing, made tangible. Change a circuit, '
        'see the result, and explore what today’s machines can—and cannot—do.</p>',
        unsafe_allow_html=True,
    )
    st.button("Explore the live experiment  →", type="primary", on_click=go_to, args=("entanglement",))
    st.write("")
    st.write("")
    st.subheader("Explore the experiments")
    st.markdown(
        '<p class="section-intro">Small, hands-on demonstrations built with IBM’s open-source '
        'Qiskit toolkit. Each one starts with a question you can test for yourself.</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="medium")
    cards = [
        ("Live now", "Entanglement in two qubits", "Rotate a qubit, add an entangling gate, and see how the measurement pattern changes.", False),
        ("Planned", "Alice, Bob and Eve", "Explore quantum key distribution and see how an eavesdropper changes the error rate.", True),
        ("Planned", "Quantum teleportation", "Follow the transfer of a quantum state using entanglement and two classical bits.", True),
    ]
    for col, (status, title, description, planned) in zip(cols, cards):
        with col:
            chip_class = "chip soon" if planned else "chip"
            st.markdown(
                f'<div class="demo-card"><span class="{chip_class}">{status}</span>'
                f'<h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True,
            )
            if not planned:
                st.button("Open experiment  →", key="open_demo", on_click=go_to, args=("entanglement",))

    st.markdown(
        '<div class="fine-print">Built by <strong>Dynamic Devices</strong> · '
        'Connected intelligence, engineered.<br>'
        'These are educational simulations, not claims of quantum speed-up. '
        '<a href="https://github.com/DynamicDevices/qiskit">View the source</a> · '
        '<a href="https://www.dynamicdevices.co.uk/">Dynamic Devices</a></div>',
        unsafe_allow_html=True,
    )


def entanglement() -> None:
    brand_header()
    st.button("← All experiments", on_click=go_to, args=("home",))
    st.markdown('<div class="eyebrow">Experiment 01 / live simulator</div>', unsafe_allow_html=True)
    st.title("Entanglement in two qubits")
    st.write(
        "Rotate the first qubit, optionally entangle it with a second one, and "
        "measure both. The bars are samples from Qiskit's local simulator."
    )

    controls, results = st.columns([1, 1.6], gap="large")
    with controls:
        angle = st.slider("Rotation angle (degrees)", 0, 180, 90, 15)
        entangle_qubits = st.toggle("Apply entangling CNOT gate", value=True)
        shots = st.select_slider("Measurements", options=[100, 500, 1000, 2000, 5000], value=1000)

    circuit = QuantumCircuit(2, 2)
    circuit.ry(math.radians(angle), 0)
    if entangle_qubits:
        circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    simulator = AerSimulator()
    counts = simulator.run(transpile(circuit, simulator), shots=shots).result().get_counts()
    labels = ["00", "01", "10", "11"]
    probabilities = [counts.get(label, 0) / shots for label in labels]

    with results:
        st.bar_chart(
            {"Outcome": labels, "Measured fraction": probabilities},
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


if st.query_params.get("view") == "entanglement":
    entanglement()
else:
    landing()

"""Dynamic Devices' shareable Qiskit experiments."""

import math

import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from diagrams import BB84_DIAGRAM, entanglement_diagram, render_mermaid, teleportation_diagram
from experiments import simulate_bb84, simulate_teleportation


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
    st.image("assets/dd-logo.svg", width=300)


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
    st.write("")
    st.subheader("Explore the experiments")
    st.markdown(
        '<p class="section-intro">Small, hands-on demonstrations built with IBM’s open-source '
        'Qiskit toolkit. Each one starts with a question you can test for yourself.</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="medium")
    cards = [
        ("Entanglement in two qubits", "Rotate a qubit, add an entangling gate, and see how the measurement pattern changes.", "entanglement"),
        ("Alice, Bob and Eve", "Explore quantum key distribution and see how an eavesdropper changes the error rate.", "bb84"),
        ("Quantum teleportation", "Follow the transfer of a quantum state using entanglement and two classical bits.", "teleportation"),
    ]
    for col, (title, description, view) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="demo-card"><span class="chip">Live now</span>'
                f'<h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True,
            )
            st.button("Open experiment  →", key=f"open_{view}", on_click=go_to, args=(view,))

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

    st.subheader("Circuit map")
    render_mermaid(entanglement_diagram(angle, entangle_qubits), height=260)
    st.caption("Mermaid shows the gate flow. The Qiskit drawing below is the exact circuit used by the simulator.")
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


def bb84() -> None:
    brand_header()
    st.button("← All experiments", on_click=go_to, args=("home",))
    st.markdown('<div class="eyebrow">Experiment 02 / quantum communication</div>', unsafe_allow_html=True)
    st.title("Alice, Bob and Eve")
    st.write(
        "Alice prepares quantum bits in one of two bases. Bob measures each in a "
        "random basis. They keep only rounds where their bases match. Eve can "
        "intercept and resend some of the bits; her measurement can disturb them."
    )

    controls = st.columns(3, gap="medium")
    with controls[0]:
        rounds = st.select_slider("Bits sent", options=[64, 128, 256, 512, 1024], value=512)
    with controls[1]:
        intercept = st.slider("Eve intercepts (%)", 0, 100, 100, 25)
    with controls[2]:
        seed = st.number_input("Trial seed", min_value=0, max_value=999999, value=7, step=1)

    result = simulate_bb84(rounds, intercept, seed)
    metrics = st.columns(3)
    metrics[0].metric("Bits intercepted", result["intercepted"])
    metrics[1].metric("Bits kept after basis comparison", result["sifted"])
    metrics[2].metric("Error rate in kept bits", f'{result["qber"]:.1%}')
    st.bar_chart(
        {"Scenario": ["No interception", "This run"],
         "Error rate": [0.0, result["qber"]]},
        x="Scenario", y="Error rate",
    )
    st.write("First 16 transmissions")
    st.dataframe(result["rows"], hide_index=True, width="stretch")
    st.subheader("Circuit and protocol map")
    render_mermaid(BB84_DIAGRAM, height=510)
    st.caption(
        "Mermaid summarizes preparation, optional interception, measurement and basis sifting. "
        "Qiskit evaluates the one-qubit measurement probabilities; Python samples each transmission."
    )
    st.info(
        "With an ideal channel, no interception gives a 0% error rate. Full "
        "intercept-and-resend gives about 25% on average; smaller trials vary. "
        "The Z and X labels are measurement bases, not network channels."
    )
    st.caption(
        "This is a Qiskit simulation of the BB84 idea. Real quantum key "
        "distribution needs a quantum channel and an authenticated classical "
        "channel; this page does not secure MQTT or any other traffic."
    )
    st.markdown(
        "[IBM's quantum key distribution lesson]"
        "(https://quantum.cloud.ibm.com/learning/en/modules/computer-science/quantum-key-distribution)"
    )


def teleportation() -> None:
    brand_header()
    st.button("← All experiments", on_click=go_to, args=("home",))
    st.markdown('<div class="eyebrow">Experiment 03 / quantum communication</div>', unsafe_allow_html=True)
    st.title("Quantum teleportation")
    st.write(
        "Choose a quantum state for Alice. An entangled pair and two ordinary "
        "measurement bits let Bob reconstruct that state. Compare Bob's result "
        "with and without the corrections those bits tell him to apply."
    )

    controls = st.columns(3, gap="medium")
    with controls[0]:
        theta = st.slider("State angle θ (degrees)", 0, 180, 60, 15)
    with controls[1]:
        phi = st.slider("Phase φ (degrees)", 0, 360, 45, 15)
    with controls[2]:
        shots = st.select_slider("Measurements", options=[100, 500, 1000, 2000], value=1000)

    result = simulate_teleportation(theta, phi, shots, 7)
    without = result["without_corrections"]
    with_corrections = result["with_corrections"]
    metrics = st.columns(2)
    metrics[0].metric("Bob matches without corrections", f'{without["rate"]:.1%}')
    metrics[1].metric("Bob matches with corrections", f'{with_corrections["rate"]:.1%}')
    st.bar_chart(
        {"Run": ["Without correction", "With correction"],
         "Bob's match rate": [without["rate"], with_corrections["rate"]]},
        x="Run", y="Bob's match rate",
    )
    st.write(
        "The verification step undoes Alice's state preparation on Bob's "
        "qubit. A zero result means it matched the chosen state."
    )
    st.subheader("Circuit map")
    render_mermaid(teleportation_diagram(theta, phi), height=340)
    st.caption("Mermaid shows the flow between Alice and Bob. The exact three-qubit Qiskit circuit is below.")
    with st.expander("Show the Qiskit circuit"):
        st.code(str(with_corrections["circuit"].draw(output="text", fold=80)), language="text")
    st.info(
        "Quantum teleportation transfers a quantum state, not a person or "
        "matter. Bob needs Alice's two classical bits, so this cannot send "
        "information faster than light. These results use an ideal simulator."
    )
    st.markdown(
        "[IBM's quantum teleportation lesson]"
        "(https://quantum.cloud.ibm.com/learning/en/modules/computer-science/quantum-teleportation)"
    )


view = st.query_params.get("view")
if view == "entanglement":
    entanglement()
elif view == "bb84":
    bb84()
elif view == "teleportation":
    teleportation()
else:
    landing()

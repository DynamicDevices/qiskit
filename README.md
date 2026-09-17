# Qiskit | Dynamic Devices

A DD-branded landing page for six interactive Qiskit experiments: entanglement, BB84 eavesdropping, quantum teleportation, Grover search, a three-qubit bit-flip repetition code, and four-device channel allocation with QAOA. They run on local Qiskit statevector simulations and need no IBM account or API token.

Live app: https://qiskit.streamlit.app/

## Run locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publish

The app is deployed from the public `DynamicDevices/qiskit` GitHub repository, using `app.py` on the `main` branch as its entry point. The demos currently use local simulators and need no IBM credentials.

The Streamlit process runs each Qiskit calculation through `worker.py` in a fresh Python process. This keeps Qiskit's native circuit code isolated from Streamlit reruns on Community Cloud.

The simulator runs on the app server. The demonstrations use fixed seeds so settings can be compared fairly. Grover search shows exact ideal probabilities. The repetition code injects independent bit flips and compares majority-vote recovery with one physical bit. Channel allocation shows QAOA probabilities alongside exhaustive classical results for all 16 assignments; it makes no performance claim.

Each experiment includes a Mermaid flow diagram for the idea being demonstrated. The circuit-based pages also show Qiskit's exact text circuit drawing. Mermaid runs in a Streamlit iframe using the official Mermaid CDN.

The Dynamic Devices logo in `assets/dd-logo.svg` is the canonical original SVG from the DD marketing collateral brand library.

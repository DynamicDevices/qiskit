# Qiskit | Dynamic Devices

A DD-branded landing page for interactive Qiskit experiments. Three live demos cover entanglement, BB84 eavesdropping, and quantum teleportation. They run on local Qiskit simulators and need no IBM account or API token.

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

The simulator runs on the app server. Measurement counts vary between runs. The BB84 page has a trial seed so visitors can compare interception levels using the same generated bases and bits.

Each experiment includes a Mermaid flow diagram for the idea being demonstrated. The entanglement and teleportation pages also retain Qiskit's exact text circuit drawing. Mermaid runs in a Streamlit iframe using the official Mermaid CDN.

The Dynamic Devices logo in `assets/dd-logo.svg` is the canonical original SVG from the DD marketing collateral brand library.

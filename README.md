# Qiskit | Dynamic Devices

A DD-branded landing page for interactive Qiskit experiments. The first live demo explores two-qubit entanglement. It uses Qiskit Aer locally and needs no IBM account or API token.

Live app: https://qiskit.streamlit.app/

## Run locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publish

The app is deployed from the public `ajlennon/qiskit` GitHub repository with `app.py` as its entry point. Do not add IBM credentials: this demo does not use them.

The simulator runs on the app server. Measurement counts vary between runs, while the underlying ideal probabilities are fixed for each angle.

The Dynamic Devices lockup in `assets/dd-lockup.svg` comes from the DD marketing collateral brand library.

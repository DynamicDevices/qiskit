# Shareable Qiskit experiment

A two-qubit, interactive Qiskit demonstration. It uses Qiskit Aer locally and needs no IBM account or API token.

## Run locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publish

Push this directory to a GitHub repository, then create a Streamlit Community Cloud app with `app.py` as its entry point. Choose public visibility to give Andy a browser link. Do not add IBM credentials: this demo does not use them.

The simulator runs on the app server. Measurement counts vary between runs, while the underlying ideal probabilities are fixed for each angle.

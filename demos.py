"""Alternate Streamlit entry point for the Qiskit experiment collection."""

from pathlib import Path
import runpy

# Streamlit reruns this file for each interaction; execute the app on every run.
runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")

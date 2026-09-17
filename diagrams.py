"""Mermaid explanations for the Qiskit experiments."""

from html import escape

import streamlit as st


def render_mermaid(source: str, *, height: int) -> None:
    """Render our trusted diagram source inside an isolated Streamlit iframe."""
    st.iframe(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    html, body {{ margin: 0; background: #0B1C2C; color: #F3F6F9; }}
    body {{ padding: 12px 4px; font-family: 'IBM Plex Sans', sans-serif; }}
    .mermaid {{ display: flex; justify-content: center; margin: 0; }}
    .mermaid svg {{ max-width: 100%; height: auto; }}
  </style>
</head>
<body>
  <pre class="mermaid">{escape(source)}</pre>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@12/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{
      startOnLoad: true,
      securityLevel: 'strict',
      theme: 'base',
      themeVariables: {{
        background: '#0B1C2C',
        primaryColor: '#173247',
        primaryTextColor: '#F3F6F9',
        primaryBorderColor: '#6DB33F',
        lineColor: '#A9DC87',
        secondaryColor: '#26472E',
        tertiaryColor: '#12293C',
        fontFamily: 'IBM Plex Sans, sans-serif'
      }}
    }});
  </script>
</body>
</html>""",
        height=height,
    )


def entanglement_diagram(angle: int, entangled: bool) -> str:
    if entangled:
        return f"""flowchart LR
  q0["q0: start at 0"] --> ry["Ry({angle}°)"] --> control["CNOT control"] --> m0["Measure c0"]
  q1["q1: start at 0"] --> target["CNOT target"] --> m1["Measure c1"]
  control -.->|one two-qubit gate| target
  classDef qubit fill:#12293C,stroke:#70889A,color:#F3F6F9
  classDef gate fill:#26472E,stroke:#6DB33F,color:#F3F6F9
  classDef measure fill:#3A2A1D,stroke:#E88A3C,color:#F3F6F9
  class q0,q1 qubit
  class ry,control,target gate
  class m0,m1 measure"""
    return f"""flowchart LR
  q0["q0: start at 0"] --> ry["Ry({angle}°)"] --> m0["Measure c0"]
  q1["q1: start at 0"] --> m1["Measure c1"]
  classDef qubit fill:#12293C,stroke:#70889A,color:#F3F6F9
  classDef gate fill:#26472E,stroke:#6DB33F,color:#F3F6F9
  classDef measure fill:#3A2A1D,stroke:#E88A3C,color:#F3F6F9
  class q0,q1 qubit
  class ry gate
  class m0,m1 measure"""


BB84_DIAGRAM = """flowchart TB
  start["Initialize qubit at 0"] --> encode["Alice: X if bit is 1; H if basis is X"]
  encode --> eve{"Eve intercepts?"}
  eve -->|yes| resend["Eve measures in Z or X, then prepares and resends"]
  eve -->|no| bob["Bob: H if basis is X; then measure"]
  resend --> bob
  bob --> sift["Keep bits when Alice and Bob bases match"]
  classDef gate fill:#26472E,stroke:#6DB33F,color:#F3F6F9
  classDef measure fill:#3A2A1D,stroke:#E88A3C,color:#F3F6F9
  class encode,bob gate
  class resend,sift measure"""


def teleportation_diagram(theta: int, phi: int) -> str:
    return f"""flowchart LR
  state["q0: prepare state θ={theta}°, φ={phi}°"] --> alice["Alice: CNOT q0 to q1, then H on q0"]
  pair["q1 and q2: H on q1, then CNOT q1 to q2"] --> alice
  pair --> bob["Bob holds q2"]
  alice --> bits["Measure q0 to c0 and q1 to c1"]
  bits --> correct["Bob: X if c1=1; Z if c0=1"]
  bob --> correct
  correct --> verify["Undo preparation and measure q2"]
  classDef qubit fill:#12293C,stroke:#70889A,color:#F3F6F9
  classDef gate fill:#26472E,stroke:#6DB33F,color:#F3F6F9
  classDef measure fill:#3A2A1D,stroke:#E88A3C,color:#F3F6F9
  class state,pair,bob qubit
  class alice,correct gate
  class bits,verify measure"""

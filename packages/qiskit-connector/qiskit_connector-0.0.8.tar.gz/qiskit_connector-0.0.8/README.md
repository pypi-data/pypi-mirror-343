# qiskit-connector

**⚛️Qiskit 2.x Connector for IBM Quantum Backends in Realtime**

A Quantum helper package compatible with Qiskit v2.x which streamlines authentication, plan detection, and backend selection for Qiskit RuntimeService. This package performs the following:
- Loads environment variables from config file (e.g. `.env`) via `python-dotenv` to configure your IBM Quantum account and make the `backend` object available in your quantum code for reuse in real-time.
- Detects your active plan (Open, Standard, Premium, Dedicated) and sets up the correct channel/instance.
- Provides functions to save your account (`qiskit_save_connection`), verify QPU resources (`qpu_verify`, `is_verified`), and retrieve a ready-to-use backend (`connector()`).

###### 🐍 Package built and maintained by Dr. Jeffrey Chijioke-Uche, IBM Quantum Ambassador & Research Scientist.
###### 🐍 Package is globally available in Pypi: https://pypi.org/project/qiskit-connector
---

## 📋 Features & API

All of the following functions are available after you import the module:

```python
from qiskit_connector import (
    connector,
    plan_type,
    qpu_verify,
    is_verified
)
```

- **`qiskit_save_connection(plan_type: str)`**  
  Saves your IBM Quantum account into QiskitRuntimeService using the environment variables for the given plan (`"open"`, `"standard"`, `"premium"`, or `"dedicated"`).

- **`qpu_verify()`**  
  Lists available QPUs for your plan by querying `QiskitRuntimeService.backends()` or falling back to `paid_plans()` for paid plans.

- **`is_verified()`**  
  Verifies real‐time least-busy QPU for the active plan and prints details (name, qubit count, online date).

- **`connector() -> IBMBackend`**  
  **Main entry point**: Loads your saved account, picks the least busy QPU (or first available for open or paid plans), prints diagnostics, and returns an `IBMBackend` instance ready for circuit execution.

- **`plan_type() -> str`**  
  Returns either **"Open Plan"** or **"Paid Plan"** depending on your `.env` toggles.

---

## 🔧 Installation

```bash
pip install qiskit-connector
```

This will also pull in:

- `qiskit>=2.0.0`  
- `qiskit-ibm-runtime>=0.37.0`  
- `python-dotenv`  
- `requests`  

and any other Qiskit dependencies.

---

## 🗂️ Environment (.env) Setup
⚠️ Security Practice: Do not CHECK-IN `.env` into version control. Add it to your .gitignore.
During development, create a file named `.env` at your project root. The connector will automatically load it:

```dotenv

#------------------------------------------------------------------------------------------------
# This file is used to store environment variables for the Qiskit installation wizard: Update it.
# The "ibm_quantum" channel option is deprecated and will be sunset on 1 July 2025.
# After this date, ibm_cloud will be the only valid channel.
# For information on migrating to the new IBM Quantum Platform on the "ibm_cloud" channel,
# review the migration guide https://quantum.cloud.ibm.com/docs/migration-guides/classic-iqp-to-cloud-iqp .
#-----------------------------------------------------------------------------------------------------

# GENERAL PURPOSE USE:
#--------------------------------------------
IQP_API_TOKEN="<YOUR_API_TOKEN_OR_IBM_QUANTUM_API_KEY>"

# Default (Open plan) - free monthly 10mins Runtime.
OPEN_PLAN_CHANNEL="<PROVIDE CHANNEL NAME>"
OPEN_PLAN_INSTANCE="<PROVIDE INSTANCE AS CRN STRING>"   # Must be a CRN String.
OPEN_PLAN_NAME="open"

# Optional (Upgrade) - Standard Plan
STANDARD_PLAN_CHANNEL="<PROVIDE CHANNEL NAME>"
STANDARD_PLAN_INSTANCE="<PROVIDE INSTANCE NAME>"
STANDARD_PLAN_NAME="standard"
STANDARD_IQP_API_URL="https://auth.quantum-computing.ibm.com/api/users/loginWithToken"   #  Update URL
STANDARD_IQP_BACKEND_URL="https://api.quantum-computing.ibm.com/runtime/backends"        #  Update URL

# Optional (Upgrade) - Premium Plan
PREMIUM_PLAN_CHANNEL="<PROVIDE CHANNEL NAME>"
PREMIUM_PLAN_INSTANCE="<PROVIDE INSTANCE AS HUB/PROJECT/ASSET PATH>"
PREMIUM_PLAN_NAME="premium"
PREMIUM_IQP_API_URL="https://auth.quantum-computing.ibm.com/api/users/loginWithToken"  #  Update URL
PREMIUM_IQP_BACKEND_URL="https://api.quantum-computing.ibm.com/runtime/backends"       #  Update URL

# Optional (Upgrade) - Dedicated Plan
DEDICATED_PLAN_CHANNEL="<PROVIDE CHANNEL NAME>"
DEDICATED_PLAN_INSTANCE="<PROVIDE INSTANCE AS HUB/PROJECT/ASSET PATH>"
DEDICATED_PLAN_NAME="dedicated"
DEDICATED_IQP_API_URL="https://auth.quantum-computing.ibm.com/api/users/loginWithToken"  #  Update URL
DEDICATED_IQP_BACKEND_URL="https://api.quantum-computing.ibm.com/runtime/backends"       #  Update URL

# Toggle exactly one plan "on":
OPEN_PLAN="on"       # free plan
STANDARD_PLAN="off"
PREMIUM_PLAN="off"
DEDICATED_PLAN="off"
```

> **⚠️ Only one** of `OPEN_PLAN`, `STANDARD_PLAN`, `PREMIUM_PLAN`, or `DEDICATED_PLAN` may be set to **"on"** at a time.

---

## 📖 Quickstart Examples

### Open Plan (default free tier) and Paid Plan

```python

from qiskit_connector import connector, plan_type
from qiskit_ibm_runtime import SamplerV2 as Sampler, Session

# QPU execution mode by plan:
current = plan_type()
backend = connector()

if current == "Open Plan":  # session not supported
    sampler = Sampler(mode=backend)
    print("Your Plan:", current)
    print("Least Busy QPU:", backend.name)
elif current == "Paid Plan":  # supports session
    with Session(backend=backend.name) as session:
        sampler = Sampler(mode=session)
        print("Your Plan:", current)
        print("Least Busy QPU:", backend.name)
else:
    raise ValueError(f"Unknown plan type: {current}")

# --- do other things below with backend, quantum circuit, sampler & transpilation ------
```


---

## Authors and Citation

Qiskit Connector was inspired, authored and brought about by the research carried out by Dr. Jeffrey Chijioke-Uche(IBM Quantum Ambassador & Research Scientist). This software is expected to continues to grow with the help and work of existing research at different levels in the Information Technology industry. If you use Qiskit for Quantum, please cite as per the provided BibTeX file.

---

## 📜 Software Publisher
Dr. Jeffrey Chijioke-Uche, IBM Quantum Ambassador & Research Scientist (All Rights Reserved) 

---

## 📜 License

This project uses the MIT License



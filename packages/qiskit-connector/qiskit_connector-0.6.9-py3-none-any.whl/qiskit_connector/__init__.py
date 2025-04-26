# @Author: Dr. Jeffrey Chijioke-Uche, IBM Quantum Ambassador & Researcher Scientist.
# @Python package: Qiskit 2.x Connector for Quantum Processing Units (QPUs).
# @Description: This script connects to IBM Quantum QPUs using Qiskit Runtime Service.
# @License: Apache License 2.0
# @Date: 2025-04-01
# @Initial Version: 0.0.1
# @Dependencies: qiskit_ibm_runtime, requests, python-dotenv
# @Usage: python qiskit_alpha_connector.py
# @Description: This script connects to IBM Quantum QPUs using Qiskit Runtime Service.
# @Note: Ensure you have the required environment variables set in your .env file.
# @Environment: Python 3.8 or higher
# @Requirements: qiskit_ibm_runtime, requests, python-dotenv
# @Installation: pip install qiskit_ibm_runtime requests python-dotenv
# @Documentation: https://github.com/schijioke-uche/qiskit_connector  
# @Availability: In PyPI: https://pypi.org/project/qiskit-alpha-connector/
#__________________________________________________________________________________________

import os
import requests
import warnings
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService, IBMBackend

# ───────────────────────────────────────────────────────────────────────────────
# 1) Load .env file from project tree or home directory
# ───────────────────────────────────────────────────────────────────────────────
def load_environment():
    load_dotenv()  # load from current directory
    start_dir = Path(__file__).parent.parent
    for directory in [start_dir] + list(start_dir.parents):
        env_files = sorted(directory.rglob(".env*"),
                           key=lambda p: (p.name != ".env", str(p)))
        if env_files:
            load_dotenv(env_files[0], override=True)
            return
    home_env = Path.home() / ".env"
    if home_env.is_file():
        load_dotenv(home_env, override=True)
    else:
        raise FileNotFoundError(
            "No `.env*` found in project tree or home. Please create one."
        )

load_environment()

# ───────────────────────────────────────────────────────────────────────────────
# 2) Read plan flags and names
# ───────────────────────────────────────────────────────────────────────────────
flags = {
    "open":      os.getenv("OPEN_PLAN",      "off").strip().lower() == "on",
    "standard":  os.getenv("STANDARD_PLAN",  "off").strip().lower() == "on",
    "premium":   os.getenv("PREMIUM_PLAN",   "off").strip().lower() == "on",
    "dedicated": os.getenv("DEDICATED_PLAN", "off").strip().lower() == "on",
}
names = {
    key: os.getenv(f"{key.upper()}_PLAN_NAME", "").strip()
    for key in flags
}

if sum(flags.values()) != 1:
    raise ValueError(
        "⛔ Exactly one of OPEN_PLAN, STANDARD_PLAN, PREMIUM_PLAN or DEDICATED_PLAN "
        "must be set to 'on'."
    )

plan_key = next(k for k, v in flags.items() if v)
connect  = names[plan_key]
tag_map  = {
    "open":      "Open Plan",
    "standard":  "Standard Plan",
    "premium":   "Premium Plan",
    "dedicated": "Dedicated Plan",
}
tag = tag_map[plan_key]

if not connect:
    raise ValueError(f"⛔ {plan_key.upper()}_PLAN_NAME must be set when {plan_key.upper()}_PLAN is 'on'")

print(f"\n🔗 Quantum active plan: {tag} (connected to: {connect} plan)")

# ───────────────────────────────────────────────────────────────────────────────
# 3) Credentials mapping
# ───────────────────────────────────────────────────────────────────────────────
criteria_to_use = {
    key: {
        "name":     names[key],
        "channel":  os.getenv(f"{key.upper()}_PLAN_CHANNEL", "").strip(),
        "instance": os.getenv(f"{key.upper()}_PLAN_INSTANCE", "").strip(),
        "token":    os.getenv("IQP_API_TOKEN", "").strip(),
    }
    for key in flags
}

active_plan  = criteria_to_use[plan_key]
paid_plan_on = flags["premium"] or flags["standard"] or flags["dedicated"]
free_plan_on = flags["open"]

header_info = "\n⚛️ Quantum Plan Backend Connection IBMBackend QPUs Compute Resources Information:"
empty_notice = "⚛️ [QPU EMPTY RETURN NOTICE]:"

# ───────────────────────────────────────────────────────────────────────────────
# 4) Save account credentials
# ───────────────────────────────────────────────────────────────────────────────
def qiskit_smart(plan=plan_key):
    crit = criteria_to_use[plan]
    if not (crit["channel"] and crit["instance"] and crit["token"]):
        print(f"⛔ Missing credentials for {plan}.")
        return

    try:
        QiskitRuntimeService.save_account(
            channel       = crit["channel"],
            token         = crit["token"],
            instance      = crit["instance"],
            name          = crit["name"],
            set_as_default=True,
            overwrite     = True,
            verify        = True,
        )
        print("-" * 82)
        print("Quantum Processing Units (QPUs) Connection Status - Qiskit")
        print("-" * 82)
        print(f"⚛️ Saved {plan.capitalize()} Plan → instance {crit['instance']}\n")
    except Exception as e:
        print(f"⛔ Failed to save account for {plan}: {e}")

# ───────────────────────────────────────────────────────────────────────────────
# 5) Paid plan HTTP API fallback
# ───────────────────────────────────────────────────────────────────────────────
def paid_plans():
    token = os.getenv("IQP_API_TOKEN", "").strip()
    url   = os.getenv("IQP_API_URL",   "").strip()
    if not (token and url):
        print("⛔ Missing IQP_API_TOKEN or IQP_API_URL.")
        return

    try:
        resp = requests.post(url, json={"apiToken": token})
        resp.raise_for_status()
        auth_id = resp.json().get("id")
        if not auth_id:
            print("⚠️ 'id' field missing in auth response.")
            return

        backend_url = os.getenv("IQP_RUNTIME_BACKEND_URL", "").strip()
        r2 = requests.get(backend_url, headers={"x-access-token": auth_id})
        r2.raise_for_status()
        devices = r2.json().get("devices", [])[:5]

        print(f"\nTop {len(devices)} {tag} QPUs:")
        for d in devices:
            print(f"- {d}")
    except Exception as e:
        print(f"⛔ Paid Plan API error: {e}")

# ───────────────────────────────────────────────────────────────────────────────
# 6) Verify QPUs via RuntimeService
# ───────────────────────────────────────────────────────────────────────────────
def qpu_verify():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        service = QiskitRuntimeService()

    names = [b.name for b in service.backends()]
    if paid_plan_on and not names:
        print(header_info)
        print("⚛️ IBMBackend returned empty list; falling back to HTTP API.")
        paid_plans()
    else:
        print(f"⚛️ IBM Quantum {tag} QPUs:")
        for n in names:
            print(f"- {n}")
        if free_plan_on and names:
            preferred = "ibm_brisbane"
            choice    = preferred if preferred in names else names[0]
            backend   = service.backend(choice)
            print(f"🖥️ Preferred backend: {backend.name} (Qubits: {backend.num_qubits})")

# ───────────────────────────────────────────────────────────────────────────────
# 7) Choose and display least-busy QPU
# ───────────────────────────────────────────────────────────────────────────────
def is_verified():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        service = QiskitRuntimeService()

    if free_plan_on:
        backend = service.least_busy(
            simulator=True,  # or False if you want real hardware
            operational=True,
            min_num_qubits=5
        )
    else:
        backend = service.least_busy(
            simulator=False,
            operational=True,
            instance=active_plan["instance"],
            min_num_qubits=5
        )

    if not backend:
        print(f"⛔ No QPU found for {tag}")
        return

    print(f"\nChosen least-busy QPU Now: {backend.name}")
    print(f"  Version: {backend.version}")
    print(f"  Qubits:  {backend.num_qubits}")

# ───────────────────────────────────────────────────────────────────────────────
# 8) Connector → pretty print + return IBMBackend
# ───────────────────────────────────────────────────────────────────────────────
def connector() -> IBMBackend:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        service = QiskitRuntimeService()
    if free_plan_on:
        qpus    = service.backends(
            simulator=False, 
            operational=True
            )
        primary = service.least_busy(
            simulator=False, 
            operational=True, 
            min_num_qubits=5
            )
    else:
        qpus = service.backends(
            simulator=False, 
            operational=True, 
            instance=active_plan["instance"]
        )
        primary = service.least_busy(
            simulator=False, 
            operational=True,
            instance=active_plan["instance"], 
            min_num_qubits=5
        )

    if not primary:
        raise RuntimeError(f"⛔ No QPU available for {tag}")

    print("\n" + "=" * 80)
    print(f"⚛️ Available QPUs ({tag}):")
    for b in qpus:
        print(f"  • {b.name}")
    print(f"\n🖥️  Least Busy QPU Now: {primary.name}")
    print(f"🖥️  Version:       {primary.version}")
    print(f"🖥️  Qubits:        {primary.num_qubits}")
    print("=" * 80 + "\n")
    return primary

# ───────────────────────────────────────────────────────────────────────────────
# 9) Footer
# ───────────────────────────────────────────────────────────────────────────────
def footer():
    today = datetime.today().strftime("%Y")
    print(f"\nDesign by: Dr. Jeffrey Chijioke-Uche, IBM Quantum Ambassador")
    print(f"IBM Quantum Qiskit Software - All Rights Reserved ©{today}\n")

# ───────────────────────────────────────────────────────────────────────────────
# 10) Utility
# ───────────────────────────────────────────────────────────────────────────────
def plan_type() -> str:
    return tag

# ───────────────────────────────────────────────────────────────────────────────
# If executed as script, demonstrate full flow
# ───────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    qiskit_smart(plan_key)
    qpu_verify()
    print()
    is_verified()
    connector()
    footer()

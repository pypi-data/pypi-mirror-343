# @Software Author: Dr. Jeffrey Chijioke-Uche, IBM Quantum Ambassador & Research Scientist
# @Python package: IBM Quantum 2.x Qiskit Connector for QPUs
# @Availability:  In Pypi.org See: https://pypi.org/project/qiskit-connector/
# @Initial Version: 0.0.1
# @Date: 2025-4-01
# @Description: Qiskit 2.x Connector for IBM Quantum QPUs
#--------------------------------------------------------------------------

import requests
import warnings
from qiskit_ibm_runtime import QiskitRuntimeService, IBMBackend
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
import importlib.util
import subprocess
import sys

#───────────────────────────────────────────────────────────────────────────────
# 1.0) Load variable file from project tree or home directory
#───────────────────────────────────────────────────────────────────────────────
load_dotenv()  # Default.
def find_env_file_in_tree(root: Path):
    return [p for p in root.rglob(".env*") if p.is_file()]
start_dir = Path(__file__).parent.parent
env_file = None
for directory in [start_dir] + list(start_dir.parents):
    candidates = find_env_file_in_tree(directory)
    if candidates:
        candidates.sort(key=lambda p: (0 if p.name == ".env" else 1, str(p)))
        env_file = candidates[0]
        break
if env_file:
    load_dotenv(env_file, override=True)
else:
    home_env = Path.home() / ".env"
    if home_env.is_file():
        load_dotenv(home_env, override=True)
    else:
        raise FileNotFoundError(
            "No `.env*` file found in this project tree or any parent directories, "
            "and no `~/.env` exists. Please create one."
        )
print("") 


#───────────────────────────────────────────────────────────────────────────────
# 1.1) Load variable file from project tree or home directory
#───────────────────────────────────────────────────────────────────────────────
def ensure_load_dotenv():
    """
    Ensure python-dotenv is installed, import load_dotenv, and load environment variables.
    """
    # Check if python-dotenv is available
    if importlib.util.find_spec("dotenv") is None:
        print("`python-dotenv` not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    
    try:
        # Attempt to import load_dotenv
        from dotenv import load_dotenv
    except ImportError as e:
        # If import still fails after installation, raise an error
        raise ImportError("Failed to import `load_dotenv` even after installation.") from e
    
    # Load quantum environment variables
    load_dotenv()
    print("✅ Quantum environment variables loaded successfully!")



#───────────────────────────────────────────────────────────────────────────────
# 2) Global flags, plan name & tag determination (capsule)
#───────────────────────────────────────────────────────────────────────────────
load_dotenv
is_open      = os.getenv("OPEN_PLAN", "").strip().lower()
is_premium   = os.getenv("PREMIUM_PLAN", "").strip().lower()
is_standard  = os.getenv("STANDARD_PLAN", "").strip().lower()
is_dedicated = os.getenv("DEDICATED_PLAN", "").strip().lower()
#───────────────────────────────────────────────────────────────────────────────
# 3) Determine active plan type
#───────────────────────────────────────────────────────────────────────────────
tag = None
if is_open == "on":
    connect = os.getenv("OPEN_PLAN_NAME")
    tag = "Open Plan"
elif is_premium == "on":
    connect = os.getenv("PREMIUM_PLAN_NAME")
    tag = "Premium Plan"
elif is_standard == "on":
    connect = os.getenv("STANDARD_PLAN_NAME")
    tag = "Standard Plan"
elif is_dedicated == "on":
    connect = os.getenv("DEDICATED_PLAN_NAME")
    tag = "Dedicated Plan"
else:
    print(f"Active Plan:", tag)
    raise ValueError(f"⛔ No valid plan is activated. Set OPEN or any PAID Plan to 'on'.")

# -- Headers --
header_1 = "\n⚛️ Quantum Plan Backend Connection IBMBackend QPUs Compute Resources Information:"
empty_return_notice_header = "⚛️ [QPU EMPTY RETURN NOTICE]:"




#───────────────────────────────────────────────────────────────────────────────
# 4) Plan‐to‐credentials mapping
#───────────────────────────────────────────────────────────────────────────────
criteria_to_use = {
    "open": {
        "name": os.getenv("OPEN_PLAN_NAME"),
        "channel": os.getenv("OPEN_PLAN_CHANNEL"),
        "instance": os.getenv("OPEN_PLAN_INSTANCE"),
        "token": os.getenv("IQP_API_TOKEN")
    },
    "premium": {
        "name": os.getenv("PREMIUM_PLAN_NAME"),
        "channel": os.getenv("PAID_PLAN_CHANNEL"),
        "instance": os.getenv("PAID_PLAN_INSTANCE"),
        "token": os.getenv("IQP_API_TOKEN")
    },
    "standard": {
        "name": os.getenv("STANDARD_PLAN_NAME"),
        "channel": os.getenv("PAID_PLAN_CHANNEL"),
        "instance": os.getenv("PAID_PLAN_INSTANCE"),
        "token": os.getenv("IQP_API_TOKEN")
    },
    "dedicated": {
        "name": os.getenv("DEDICATED_PLAN_NAME"),
        "channel": os.getenv("PAID_PLAN_CHANNEL"),
        "instance": os.getenv("PAID_PLAN_INSTANCE"),
        "token": os.getenv("IQP_API_TOKEN")
    }
}
is_open_on    = is_open
is_premium_on = is_premium
is_standard_on = is_standard
is_dedicated_on = is_dedicated
active_plan = criteria_to_use[connect]
switched_on_plan = is_open_on or is_premium_on or is_dedicated_on or is_standard_on
paid_plan_on = is_premium_on or is_dedicated_on or is_standard_on
free_plan_on = is_open_on


#───────────────────────────────────────────────────────────────────────────────
# 5) Save account credentials to QiskitRuntimeService
#───────────────────────────────────────────────────────────────────────────────
def qiskit_smart(plan_type_on=connect):
    try:
        criterion = criteria_to_use[plan_type_on]
        QiskitRuntimeService.save_account(
            channel=criterion["channel"],
            token=criterion["token"],
            instance=criterion["instance"],
            name=criterion["name"],
            set_as_default=True,
            overwrite=True,
            verify=True
        )
        # -- Plan Instance ---
        open_focused_instance = os.getenv("OPEN_PLAN_INSTANCE", "")
        standard_focused_instance = os.getenv("PAID_PLAN_INSTANCE", "")
        premium_focused_instance = os.getenv("PAID_PLAN_INSTANCE", "")
        dedicated_focused_instance = os.getenv("PAID_PLAN_INSTANCE", "")

        if plan_type_on == "open":
            plan_instance = open_focused_instance
        elif plan_type_on == "standard":
            plan_instance = standard_focused_instance
        elif plan_type_on == "premium":
            plan_instance = premium_focused_instance
        elif plan_type_on == "dedicated":
            plan_instance = dedicated_focused_instance
        else:
            print("No Plan Specified")

        print("-" * 82 + "\n")
        print("\nQuantum Processing Units (QPUs) Connection Status - Qiskit v2.x")
        print("-" * 82 + "\n")
        # effective Juy 1 2025, removed the warning filter & use ibm_cloud as channel for Premium Plan.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            confirmation = QiskitRuntimeService()
        if confirmation: # Verify
            print(f"⚛️ Your Quantum Plan Type:  ✅ {plan_type_on.capitalize()} Plan")
            print(f"⚛️ {tag} Connection Status: ✅ QPU backend connection established successfully!")
            print(f"⚛️ {plan_type_on.capitalize()} Plan Instance: ✅ {plan_instance}\n\n")
        else:
            print(f'⛔ {tag} IBM Quantum Account Plan Backend Connection & Save Failed!')
    except Exception as e:
        print(f"ℹ️ Provider's message: {e}")



#───────────────────────────────────────────────────────────────────────────────
# 6) Optional: authenticate & list premium backends via HTTP
#───────────────────────────────────────────────────────────────────────────────
def paid_plans():
    """
    Authenticate to IBM Quantum Premium Plan and list available backend devices.
    Requires 'IQP_API_TOKEN', 'IQP_API_URL', and 'IQP_RUNTIME_BACKEND_URL' to be set.
    """
    try:
        token = os.environ.get("IQP_API_TOKEN", "").strip()
        url = os.environ.get("IQP_API_URL", "").strip()

        if not token or not url:
            print(f"⛔ Required environment variables 'IQP_API_TOKEN' or 'IQP_API_URL' are missing or empty.")
            return

        payload = {"apiToken": token}

        # Attempt authentication
        auth_response = requests.post(url, json=payload)
        auth_response.raise_for_status()

        json_data = auth_response.json()
        auth_id = json_data.get('id')

        if auth_id:
            print("-" * 82 + "\n")
            print(f"⚛️ Your Quantum Plan Type: {tag}")
            print(f'✅ {tag} Plan IBM Quantum Account Plan Backend Connection Established Successfully!')
            print(f"✅ Authentication Successful & Premium Connection ID: {auth_id}")
        else:
            print("⚠️ 'id' field not found in the authentication response.")
            return

    except requests.exceptions.RequestException as e:
        print(f"⛔ Network or HTTP error occurred during authentication: {e}")
        return
    except ValueError:
        print("⛔ Failed to parse authentication JSON response.")
        return
    except Exception as e:
        print(f"⛔ Unexpected authentication error: {e}")
        return

    # Fetch premium backend computing resources
    try:
        backend_url = os.environ.get("IQP_RUNTIME_BACKEND_URL", "").strip()
        if not backend_url:
            print("⚠️ Environment variable 'IQP_RUNTIME_BACKEND_URL' is missing or empty.")
            return

        headers = {
            'Content-Type': 'application/json',
            'x-access-token': auth_id
        }

        backends_response = requests.get(backend_url, headers=headers)
        backends_response.raise_for_status()

        devices = backends_response.json().get('devices', [])
        if devices:
            devices = devices[:5]
            preferred_qpu = "ibm_brisbane" if "ibm_brisbane" in devices else None

            print("🔧 Your Top 5 available premium plan IBMBackend QPUs:")
            for device in devices:
                print(f"- {device}")

            if preferred_qpu:
                print(f"🎯 Preferred QPU backend: {preferred_qpu}")
            else:
                print("\n⚠️ 'ibm_brisbane' not found — no preferred QPU selected.")
        else:
            print("⚠️ No backend devices returned in response.")

    except requests.exceptions.RequestException as e:
        print(f"⛔ Error retrieving backend devices: {e}")
    except ValueError:
        print("⛔ Failed to parse backend devices JSON response.")
    except Exception as e:
        print(f"⛔ Unexpected error while fetching backend list: {e}")



#───────────────────────────────────────────────────────────────────────────────
# 7) Verify QPUs available via QiskitRuntimeService
#───────────────────────────────────────────────────────────────────────────────
def qpu_verify():
    try:
        # effective Juy 1 2025, removed the warning filter & use ibm_cloud as channel for Premium Plan.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            service = QiskitRuntimeService()
            qpus = service.backends()
            qpu_names = [qpu.name for qpu in qpus]
            preferred_qpu = "ibm_brisbane"

        if paid_plan_on == "on" and not qpu_names:
            print(header_1)
            print("⚛️ IBMBackend retuned empty List[] of QPU backends - P98903.")
            return

        elif paid_plan_on == "on" and qpu_names:
            print(header_1)
            paid_plans()  # [PAID PLAN API VERIFICATION SINCE IBMBACKEND FAILED]

        elif free_plan_on == "on" and not qpu_names:
            print(header_1)
            print("⚛️ IBMBackend retuned empty List[] of QPU backends - F98903.")
            return

        elif free_plan_on == "on" and qpu_names:
            print(f"⚛️ IBM Quantum {switched_on_plan} IBMBackend Compute Resources With Preferred QPU:")
            for name in qpu_names:
                print(f"- {name}")
        
            backend_name = preferred_qpu if preferred_qpu in qpu_names else qpu_names[0]
            if backend_name != preferred_qpu:
                print(f"ℹ️ Preferred backend '{preferred_qpu}' not found. Falling back to '{backend_name}'")
        
            backend = service.backend(backend_name)
            print(
                f"🖥️ Preferred QPU backend: {backend.name}\n"
                f"🖥️ Version: {getattr(backend, 'version', 'N/A')}\n"
                f"🖥️ Number of Qubits: {getattr(backend, 'num_qubits', 'N/A')}\n"
            )
        else:
            print("⚛️ Switched On Plan is Unknown - Contact your administrator")
    except Exception as e:
        print(f"ℹ️ Quantum hardware Provider's Message: {e}")



#───────────────────────────────────────────────────────────────────────────────
# 8) Quick realtime check:
#───────────────────────────────────────────────────────────────────────────────
def is_verified():
    """
    Quantum backend connected device criteria verification & listing.
    """
    #1️⃣ Quantum backend connection (live QPU only): Realtime.
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            service = QiskitRuntimeService()

        if is_open_on == "on" and is_premium_on == "off" and is_standard_on == "off" and is_dedicated_on == "off":
            switched_on_plan = "Open Plan"
            backend = service.least_busy(
                simulator=False,
                operational=True,
                min_num_qubits=5
            )
            if backend:
                print(f"⚛️ IBM Quantum {switched_on_plan} Backend Compute Resources With Least Busy QPU:")
                qpus = service.backends()
                qpu_names = [qpu.name for qpu in qpus]
                for device in qpu_names:
                    print(f"- {device}")
                print(
                    f"🖥️ Least Busy QPU backend device: {backend.name}\n"
                    f"🖥️ Version: {getattr(backend, 'version', 'N/A')}\n"
                    f"🖥️ Number of Qubits: {getattr(backend, 'num_qubits', 'N/A')}\n"
                    f"🖥️ Online Since: {getattr(backend, 'online_date', 'N/A')}\n"
                    )
                footer()
            else:
                print(f"⛔ {switched_on_plan}: Backend QPU device not accessible - E1033.")
                return
        elif is_premium_on == "on" or is_standard_on == "on" or is_dedicated_on == "on" and is_open_on == "off":
            switched_on_plan = "Premium Plan"
            instance = os.getenv("PAID_PLAN_INSTANCE", "") 
            channel = os.getenv("PAID_PLAN_CHANNEL", "") 
            url = os.getenv("IBM_QUANTUM_API_URL", "") 
            token = os.getenv("IQP_API_TOKEN", "") 
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                service = QiskitRuntimeService(
                    instance=instance, 
                    channel=channel, 
                    url=url,
                    token=token,
                    verify=True
                    )
                # Try filter by instance first…
                IBMBackends = service.backends(
                    simulator=False,
                    operational=True,
                    instance=instance,
                    min_num_qubits=5
                    )
                #...if the IBMBackend list is Not Empty:
                if IBMBackends:
                    print("Raw premium backend list:", IBMBackends)
                    # Print just the names one‑per‑line:
                    print("Available premium filetered backends:")
                    for b in IBMBackends:
                        print(f"- {b.name}")
                        backend = IBMBackends[0]
                        print(f"⚛️ IBM Quantum {switched_on_plan} backend Compute Resources With Available QPUs:")
                        IBMBackend_names = [qpu.name for qpu in IBMBackends]
                        for device in IBMBackend_names:
                            print(f"- {device}")
                            print(
                                f"🖥️ First Available QPU backend device: {backend.name}\n"
                                f"🖥️ Version: {getattr(backend, 'version', 'N/A')}\n"
                                f"🖥️ Number of Qubits: {getattr(backend, 'num_qubits', 'N/A')}\n"
                                f"🖥️ Online Since: {getattr(backend, 'online_date', 'N/A')}\n"
                                ) 
                            footer()
                # …but if it’s empty,
                else:
                    print(empty_return_notice_header)
                    print("-" * 28 + "\n")
                    print(f"🔔 {switched_on_plan} Instance:", {instance})
                    print(f"🔔 Returned empty QPU IBMBackend list :", IBMBackends)
                    print(f"🔔 You do not have access to this {switched_on_plan} QPUs in {instance}.\n🔔 Contact your administrator for additional help.\n ")    
                    footer()
       #-----         
        else:
            print(f"⛔ Plan error: please activate exactly one of OPEN_PLAN or PREMIUM_PLAN (value='on').")
            return
    except Exception as e:
        print(f'⚛️ Open Plan is: {is_open_on}')
        print(f'⚛️ Premium Plan is: {is_premium_on}')
        print(f"⛔ Quantum {switched_on_plan}: Connected but could not retrieve quantum backend QPU device: {e}")
        footer()
        return


#───────────────────────────────────────────────────────────────────────────────
# 9) Author's Footer
#───────────────────────────────────────────────────────────────────────────────
def footer():
    today = datetime.today().strftime("%Y")
    print(f"\nDesign by: Dr. Jeffrey Chijioke-Uche, IBM Quantum Ambassador\nIBM Quantum Qiskit Software - All Rights Reserved ©{today}\n")
    print("-" * 82 + "\n")


#───────────────────────────────────────────────────────────────────────────────
# 10) Pypi.org Package Object
#───────────────────────────────────────────────────────────────────────────────
def connector() -> IBMBackend:
    """Save your account, list QPUs, pick one, and return it backend."""
    ensure_load_dotenv()
    if paid_plan_on:
        instance = os.getenv("PAID_PLAN_INSTANCE", "").strip().lower()
    else:
        instance = os.getenv("OPEN_PLAN_INSTANCE", "").strip().lower() 
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            service = QiskitRuntimeService() 
    except Exception as e:
        print(f"⛔ Failed to initialize QiskitRuntimeService: {e}")
        return None

    # Choose the right QPU:
    if is_open_on == "on" and is_premium_on == "off" and is_dedicated == "off" and is_standard == "off":
        plan = "Open Plan"
        try:
            backend = service.least_busy(
                simulator=False,
                operational=True,
                min_num_qubits=5
            )
        except Exception as e:
            print(f"⛔ {plan}: no least‐busy QPU found: {e}")
            return None

    elif is_premium_on == "on" or is_standard == "on" or is_dedicated == "on" and is_open_on == "off":
        plan = "Paid Plan"
        available = service.backends(
            simulator=False,
            operational=True,
            instance=instance,
            min_num_qubits=5,
            filters=lambda x: ("rz" in x.basis_gates )
        )
        if not available:
            print(f"⛔ {plan}: returned empty QPU list for instance '{instance}'")
            return None
        backend = available[0]
    else:
        print("⛔ Plan error: set exactly one of OPEN_PLAN or PREMIUM_PLAN = 'on'")
        return None

    # 4) Diagnostics / Confirmation:
    print("\n" + "-" * 82)
    print(f"⚛️  Connected [{plan}]  →  Realtime Least Busy QPU: {backend.name}")
    print("-" * 82)

    # list all available QPUs under this plan
    qpus = service.backends(
        simulator=False,
        operational=True,
        instance=(instance if plan == switched_on_plan else None)
    )
    print(f"⚛️ Available QPUs ({plan}):")
    for q in qpus:
        print(f"- {q.name}")
    print(f"🖥️  Default QPU: {backend.name}")
    print(f"🖥️  Qubit Version: {backend.version}")
    print(f"🖥️  Number of Qubits: {backend.num_qubits}")
    print("-" * 82 + "\n")
    #footer()  # Footer is deactivated in this version.
    print("-" * 82 + "\n")

    return backend



#───────────────────────────────────────────────────────────────────────────────
# 11) Plan Type
#───────────────────────────────────────────────────────────────────────────────
def plan_type():
    """
    Decide which execution plan is active.
    Exactly one of [OPEN_PLAN] vs. [PREMIUM_PLAN, STANDARD_PLAN, DEDICATED_PLAN]
    must be 'on'. Returns "Open Plan" or "Paid Plan", otherwise raises.

    Args:
        if paid_on == 'on' then plan is 'Paid Plan'
        if open_on == 'on' then plan is 'Open Plan'
    """
    # Already read from .env/vault above - No need to defined it again.
    open_on = is_open_on
    paid_on = is_premium_on or is_standard_on or is_dedicated_on
    

    if paid_on == "on" and not open_on:
        plan = "Paid Plan"
        return plan
    else:
        plan = "Open Plan"
        return plan


#───────────────────────────────────────────────────────────────────────────────
# 12) Main function
#───────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    qiskit_smart(connect) 
    qpu_verify()
    print('\n')
    is_verified()
    connector()
 
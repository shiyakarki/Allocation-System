import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Hospital Triage & Allocation",
    page_icon="🏥",
    layout="wide"
)

# --- 1. Session State Initialization (Persists data across clicks) ---
if "doctors" not in st.session_state:
    st.session_state.doctors = [
        {"name": "Dr. Sharma", "speciality": "Emergency", "available": True, "patient": None},
        {"name": "Dr. Verma", "speciality": "General Medicine", "available": True, "patient": None},
        {"name": "Dr. Singh", "speciality": "Cardiology", "available": True, "patient": None}
    ]

if "patients" not in st.session_state:
    st.session_state.patients = []

if "counter" not in st.session_state:
    st.session_state.counter = 101


# --- 2. Allocation & Discharge Logic ---
def allocate_doctors():
    waiting = [p for p in st.session_state.patients if p["status"] == "Waiting"]
    if not waiting:
        st.toast("No patients currently waiting in queue.", icon="ℹ️")
        return

    # Sort so priority 1 (Critical) is served first
    waiting.sort(key=lambda p: p["priority"])
    allocated_count = 0

    for patient in waiting:
        matched_doc = None

        # Exact match
        for doc in st.session_state.doctors:
            if doc["available"] and doc["speciality"] == patient["needed_speciality"]:
                matched_doc = doc
                break

        # Emergency fallback for Critical (Priority 1)
        if not matched_doc and patient["priority"] == 1:
            for doc in st.session_state.doctors:
                if doc["available"] and doc["speciality"] == "Emergency":
                    matched_doc = doc
                    break

        if matched_doc:
            patient["doctor"] = matched_doc["name"]
            patient["status"] = "Under Treatment"
            matched_doc["available"] = False
            matched_doc["patient"] = patient["name"]
            allocated_count += 1
            st.toast(f"Allocated {matched_doc['name']} to {patient['name']}", icon="🩺")

    if allocated_count == 0:
        st.warning("No matching doctors currently available.")


def discharge_doctor(doc_name: str):
    for doc in st.session_state.doctors:
        if doc["name"] == doc_name and not doc["available"]:
            patient_name = doc["patient"]
            # Mark patient as Discharged
            for p in st.session_state.patients:
                if p["name"] == patient_name and p["status"] == "Under Treatment":
                    p["status"] = "Discharged"
                    break
            # Free doctor
            doc["available"] = True
            doc["patient"] = None
            st.success(f"Discharged {patient_name}. {doc['name']} is now Available!")
            allocate_doctors()
            break


# --- 3. UI Layout ---

st.title("🏥 Hospital Triage & Allocation Dashboard")

# Top Metrics Row
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
total_waiting = len([p for p in st.session_state.patients if p["status"] == "Waiting"])
critical_count = len([p for p in st.session_state.patients if p["status"] == "Waiting" and p["priority"] == 1])
busy_docs = len([d for d in st.session_state.doctors if not d["available"]])
avail_docs = len([d for d in st.session_state.doctors if d["available"]])

col_m1.metric("Waiting Patients", total_waiting)
col_m2.metric("Critical in Queue", critical_count)
col_m3.metric("Available Doctors", avail_docs)
col_m4.metric("Doctors in Consultation", busy_docs)

st.divider()

# Sidebar: Patient Registration & Controls
with st.sidebar:
    st.header("📝 Register Patient")
    with st.form("patient_form", clear_on_submit=True):
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        condition = st.selectbox(
            "Condition / Severity",
            [
                "Critical - Unconscious or Severe Trauma",
                "Critical - Severe Chest Pain / Cardiac",
                "Urgent - High Fever or Severe Pain",
                "Routine - Mild Symptoms / Checkup"
            ]
        )
        submitted = st.form_submit_button("➕ Register & Triage")

        if submitted:
            if not name.strip():
                st.error("Please enter a valid name.")
            else:
                if "Cardiac" in condition:
                    severity, priority, spec = "Critical", 1, "Cardiology"
                elif "Critical" in condition:
                    severity, priority, spec = "Critical", 1, "Emergency"
                elif "Urgent" in condition:
                    severity, priority, spec = "Urgent", 2, "General Medicine"
                else:
                    severity, priority, spec = "Routine", 3, "General Medicine"

                p_id = f"P-{st.session_state.counter}"
                st.session_state.counter += 1

                st.session_state.patients.append({
                    "id": p_id,
                    "name": name,
                    "age": int(age),
                    "severity": severity,
                    "priority": priority,
                    "needed_speciality": spec,
                    "status": "Waiting",
                    "doctor": "Not Assigned"
                })
                st.success(f"Registered {name} ({p_id}) as {severity}")
                allocate_doctors()

    st.header("⚡ Actions")
    if st.button("🔄 Trigger Doctor Allocation", use_container_width=True):
        allocate_doctors()

    st.subheader("🚪 Discharge Patient")
    busy_list = [d["name"] for d in st.session_state.doctors if not d["available"]]
    if busy_list:
        selected_doc = st.selectbox("Select Doctor to Discharge", busy_list)
        if st.button("Complete Consultation", use_container_width=True):
            discharge_doctor(selected_doc)
    else:
        st.info("No doctors are currently treating patients.")

# Main Screen: Doctors & Patients Tables
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("👨‍⚕️ Doctor Roster")
    doc_df = pd.DataFrame(st.session_state.doctors)
    doc_df["Status"] = doc_df["available"].apply(lambda x: "🟢 Available" if x else "🔴 Busy")
    doc_df["Current Patient"] = doc_df["patient"].fillna("-")
    st.dataframe(
        doc_df[["name", "speciality", "Status", "Current Patient"]],
        use_container_width=True,
        hide_index=True
    )

with col_right:
    st.subheader("📋 Active Patients (Priority Ordered)")
    if st.session_state.patients:
        # Show waiting & in-treatment first, sorted by priority
        active_pts = [p for p in st.session_state.patients if p["status"] != "Discharged"]
        active_pts.sort(key=lambda x: x["priority"])
        if active_pts:
            pts_df = pd.DataFrame(active_pts)
            st.dataframe(
                pts_df[["id", "name", "age", "severity", "needed_speciality", "status", "doctor"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No active patients currently.")
    else:
        st.info("No patients registered yet.")

# Historical / Discharged Patients Table
with st.expander("📜 Discharged Patients History"):
    discharged_pts = [p for p in st.session_state.patients if p["status"] == "Discharged"]
    if discharged_pts:
        st.dataframe(pd.DataFrame(discharged_pts)[["id", "name", "age", "severity", "doctor"]], use_container_width=True, hide_index=True)
    else:
        st.write("No patients have been discharged yet.")

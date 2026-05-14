import streamlit as st
import sys
import os
import time

# ---------------- PATH FIX ----------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.ml_model import find_best_donors

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="LifeLink AI", layout="wide")

# ---------------- SESSION STATE ----------------
if "results" not in st.session_state:
    st.session_state.results = []

if "assigned" not in st.session_state:
    st.session_state.assigned = []

if "history" not in st.session_state:
    st.session_state.history = []

if "points" not in st.session_state:
    st.session_state.points = 0

# ---------------- UI HEADER ----------------
st.title("❤️ LifeLink AI - Smart Blood & Organ Donation Network")
st.caption("AI-powered, real-time donor matching system for emergencies")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "🚀 Navigation",
    ["🏠 Dashboard", "🩸 Blood Donation", "🫀 Organ Donation", "🤖 AI Matching", "📊 Analytics", "🔔 Alerts"]
)

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.subheader("📊 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🩸 Donors Assigned", len(st.session_state.assigned))
    col2.metric("🚨 Emergencies", len(st.session_state.results))
    col3.metric("🏅 Reward Points", st.session_state.points)
    col4.metric("🤖 AI Status", "ACTIVE")

    st.info("LifeLink AI is monitoring emergency donation requests in real-time")

# ---------------- BLOOD DONATION ----------------
elif menu == "🩸 Blood Donation":
    st.subheader("🩸 Donor Registration")

    name = st.text_input("Full Name")
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    phone = st.text_input("Mobile Number")

    if st.button("Register Donor"):
        st.success("Donor Registered Successfully")
        st.session_state.points += 10

# ---------------- ORGAN DONATION ----------------
elif menu == "🫀 Organ Donation":
    st.subheader("🫀 Organ Donation Consent")

    organs = st.multiselect(
        "Select Organs",
        ["Heart", "Kidney", "Liver", "Lungs", "Corneas", "Skin", "Bone"]
    )

    if st.button("Submit Consent"):
        st.success("Organ Consent Submitted")
        st.session_state.points += 20

# ---------------- AI MATCHING ----------------
elif menu == "🤖 AI Matching":
    st.subheader("🚨 Emergency AI Matching Engine")

    blood_group = st.selectbox(
        "Required Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

    urgency = st.selectbox("Urgency Level", ["normal", "critical"])

    emergency = {
        "blood_group": blood_group,
        "lat": 21.1458,
        "lon": 79.0882,
        "urgency": urgency
    }

    donors = [
        {"name": "Rahul", "blood_group": "A+", "lat": 21.15, "lon": 79.09, "trust_score": 80},
        {"name": "Amit", "blood_group": "O+", "lat": 21.17, "lon": 79.08, "trust_score": 90},
        {"name": "Neha", "blood_group": "B+", "lat": 21.20, "lon": 79.05, "trust_score": 70},
        {"name": "Karan", "blood_group": "A+", "lat": 21.16, "lon": 79.10, "trust_score": 85},
        {"name": "Sahil", "blood_group": "O-", "lat": 21.14, "lon": 79.07, "trust_score": 95},
    ]

    if st.button("🚨 Trigger Emergency Matching"):
        with st.spinner("AI is analyzing donors..."):
            time.sleep(2)

        results = find_best_donors(donors, emergency)

        st.session_state.results = results
        st.session_state.history.append(results)

        st.success("Top Matching Donors Found")

        for i, r in enumerate(results, 1):

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"### 👤 {r['name']}")
                st.write(f"🩸 Blood Group: {r['blood_group']}")

            with col2:
                st.markdown(f"### ⭐ Score: {r['score']}")

            with col3:
                if st.button(f"Assign {r['name']}"):
                    st.session_state.assigned.append(r['name'])
                    st.session_state.points += 50
                    st.success(f"{r['name']} Assigned 🚑")

        st.info("""
🧠 AI Explanation:
- Blood group compatibility check
- Distance-based ranking
- Trust score evaluation
- Urgency boost applied
""")

# ---------------- ANALYTICS ----------------
elif menu == "📊 Analytics":
    st.subheader("📊 System Analytics")

    st.metric("Total Assignments", len(st.session_state.assigned))
    st.metric("Total Emergencies", len(st.session_state.results))
    st.metric("Reward Points", st.session_state.points)

    st.bar_chart({
        "Assignments": [len(st.session_state.assigned)],
        "Emergencies": [len(st.session_state.results)]
    })

# ---------------- ALERTS ----------------
elif menu == "🔔 Alerts":
    st.subheader("🔔 Emergency Alerts System")

    if not st.session_state.results:
        st.warning("No active emergencies")
    else:
        for r in st.session_state.results:
            st.markdown(f"""
            ### 🚨 {r['name']}
            - Score: {r['score']}
            - Status: Pending / Assigned
            """)
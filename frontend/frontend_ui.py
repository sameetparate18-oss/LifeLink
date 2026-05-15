import streamlit as st
import sys
import os
import time
import requests

# ---------------- PATH FIX ----------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="LifeLink AI",
    layout="wide",
    page_icon="❤️"
)

# ---------------- GLOBAL STYLES ----------------

st.markdown("""
<style>

.main {
    background-color: #0b1220;
}

/* TITLE */

.title {
    font-size: 40px;
    font-weight: 800;
    color: white;
}

.accent {
    color: #ff4b4b;
}

/* KPI CARD */

.kpi {
    background: #111827;
    border: 1px solid #1f2937;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    height: 120px;

    display: flex;
    flex-direction: column;
    justify-content: center;
}

.kpi h3 {
    font-size: 14px;
    color: #9ca3af;
    margin: 0;
}

.kpi h2 {
    font-size: 28px;
    color: white;
    margin: 0;
}

/* CARD */

.card {
    background: #111827;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    margin-bottom: 10px;
}

/* STATUS */

.status {
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
}

.good {
    background: #14532d;
    color: #4ade80;
}

.mid {
    background: #78350f;
    color: #fbbf24;
}

.bad {
    background: #7f1d1d;
    color: #f87171;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

if "results" not in st.session_state:
    st.session_state.results = []

if "assigned" not in st.session_state:
    st.session_state.assigned = []

if "points" not in st.session_state:
    st.session_state.points = 0

# ---------------- HEADER ----------------

st.markdown(
    '<div class="title">❤️ LifeLink <span class="accent">AI</span></div>',
    unsafe_allow_html=True
)

st.caption(
    "Real-time Emergency Blood & Organ Matching System"
)

st.write("---")

# ---------------- SIDEBAR ----------------

menu = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Blood Donation",
        "Organ Donation",
        "AI Matching",
        "Disease Prediction",
        "Analytics",
        "Alerts"
    ]
)

# ================= DASHBOARD =================

if menu == "Dashboard":

    st.subheader("📊 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="kpi">
            <h3>🩸 Assigned</h3>
            <h2>{len(st.session_state.assigned)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="kpi">
            <h3>🚨 Emergencies</h3>
            <h2>{len(st.session_state.results)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="kpi">
            <h3>🏅 Points</h3>
            <h2>{st.session_state.points}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown("""
        <div class="kpi">
            <h3>🤖 AI Status</h3>
            <h2>ACTIVE</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    st.success(
        "System actively monitoring donor network in real-time 🚑"
    )

# ================= BLOOD DONATION =================

elif menu == "Blood Donation":

    st.subheader("🩸 Donor Registration")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Full Name")
        phone = st.text_input("Mobile Number")

    with col2:

        blood_group = st.selectbox(
            "Blood Group",
            ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        )

    if st.button("Register Donor"):

        if name and phone:

            st.success("Donor Registered Successfully")

            st.session_state.points += 10

        else:

            st.warning("Please fill all fields")

# ================= ORGAN DONATION =================

elif menu == "Organ Donation":

    st.subheader("🫀 Organ Donation Consent")

    organs = st.multiselect(
        "Select Organs",
        [
            "Heart",
            "Kidney",
            "Liver",
            "Lungs",
            "Corneas",
            "Skin",
            "Bone"
        ]
    )

    if st.button("Submit Consent"):

        st.success("Consent Submitted Successfully")

        st.session_state.points += 20

# ================= AI MATCHING =================

elif menu == "AI Matching":

    st.subheader("🚨 Emergency AI Matching Engine")

    st.info("AI matching module active")

# ================= DISEASE PREDICTION =================

elif menu == "Disease Prediction":

    st.subheader("🩺 AI Disease Prediction")

    st.write(
        "Enter symptom values as 0 and 1 separated by commas"
    )

    symptom_input = st.text_input(
        "Symptoms",
        placeholder="Example: 1,0,1"
    )

    if st.button("Predict Disease"):

        try:

            symptoms = [
                int(x.strip())
                for x in symptom_input.split(",")
            ]

            with st.spinner("AI analyzing symptoms..."):

                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json={
                        "symptoms": symptoms
                    }
                )

                data = response.json()

                time.sleep(1)

            st.success("Prediction Completed ✅")

            st.markdown(f"""
            <div class="card">
                <h2>🧠 Predicted Disease</h2>
                <h1 style="color:#4ade80;">
                    {data['prediction']}
                </h1>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:

            st.error(str(e))

# ================= ANALYTICS =================

elif menu == "Analytics":

    st.subheader("📊 System Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Assignments",
        len(st.session_state.assigned)
    )

    col2.metric(
        "Emergencies",
        len(st.session_state.results)
    )

    col3.metric(
        "Points",
        st.session_state.points
    )

    st.write("---")

    st.bar_chart({
        "Assignments": [
            len(st.session_state.assigned)
        ],

        "Emergencies": [
            len(st.session_state.results)
        ]
    })

# ================= ALERTS =================

elif menu == "Alerts":

    st.subheader("🔔 Emergency Alerts")

    if not st.session_state.results:

        st.info("No active emergencies right now")

    else:

        for r in st.session_state.results:

            st.error(
                f"🚨 {r['name']} - Score {r['score']}"
            )
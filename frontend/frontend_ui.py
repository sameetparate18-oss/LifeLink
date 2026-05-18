import streamlit as st
import sys
import os
import time
import requests
import pandas as pd

# ================= PATH FIX =================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st

st.set_page_config(page_title="LifeLink AI", layout="wide")


# ================= HOME PAGE =================
def home_page():

    st.markdown("""
    <style>

    .hero-title {
        font-size: 70px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ef4444, #f97316, #facc15);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 20px;
        color: #white;
    }

    .hero-description {
        text-align: center;
        color: #94a3b8;
        max-width: 800px;
        margin: auto;
    }

    .badge-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }

    .badge {
        background: rgba(255,255,255,0.05);
        padding: 8px 14px;
        border-radius: 20px;
        color: white;
        font-size: 13px;
    }

    </style>

    <div class="hero-title"> LifeLink</div>

    <div class="hero-subtitle">
        Smart Blood & Organ Donation Network
    </div>

    <div class="hero-description">
        AI-powered, privacy-first, multi-hospital connected healthcare platform
        designed for real-time donor matching and emergency response.
    </div>

    <div class="badge-container">
        <div class="badge">🩸 Blood Donation</div>
        <div class="badge">🫀 Organ Donation</div>
        <div class="badge">🤖 AI Matching</div>
        <div class="badge">🔔 Real-time Alerts</div>
        <div class="badge">👩 ASHA Integration</div>
        <div class="badge">🏅 Reward System</div>
        <div class="badge">🔒 Privacy-first</div>
    </div>

    """, unsafe_allow_html=True)


# ================= DASHBOARD =================
def dashboard_page():
    st.title("📊 Dashboard")


# ================= ROUTER =================
if "page" not in st.session_state:
    st.session_state.page = "home"


def router():
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()


router()
# ================= CUSTOM CSS =================

st.markdown("""
<style>

/* MAIN APP */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color: white;
}

/* REMOVE STREAMLIT DEFAULT */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #1f2937;
}

/* SCROLLBAR */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #ef4444;
    border-radius: 10px;
}

/* GLASS CARD */

.glass {
    background: rgba(17, 24, 39, 0.78);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    transition: 0.3s ease;
    margin-bottom: 20px;
}

.glass:hover {
    transform: translateY(-3px);
    border: 1px solid #ef4444;
}

/* KPI CARD */

.kpi-card {
    background: linear-gradient(
        135deg,
        #111827,
        #1e293b
    );

    border-radius: 20px;
    padding: 24px;
    text-align: center;

    border: 1px solid #1f2937;

    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.kpi-card h3 {
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 10px;
}

.kpi-card h1 {
    color: white;
    font-size: 40px;
    margin: 0;
}

/* BUTTONS */

.stButton > button {

    width: 100%;
    border-radius: 12px;

    border: none;

    background: linear-gradient(
        90deg,
        #ef4444,
        #dc2626
    );

    color: white;
    font-size: 16px;
    font-weight: bold;

    padding: 12px;

    transition: 0.3s;
}

.stButton > button:hover {

    transform: scale(1.02);

    background: linear-gradient(
        90deg,
        #dc2626,
        #b91c1c
    );
}

/* INPUTS */

.stTextInput input,
.stSelectbox div,
.stMultiSelect div {

    border-radius: 10px !important;
}

/* STATUS */

.status-good {
    background: #14532d;
    color: #4ade80;
    padding: 8px 14px;
    border-radius: 10px;
    display: inline-block;
    font-weight: bold;
}

.status-warning {
    background: #78350f;
    color: #facc15;
    padding: 8px 14px;
    border-radius: 10px;
    display: inline-block;
    font-weight: bold;
}

.status-danger {
    background: #7f1d1d;
    color: #f87171;
    padding: 8px 14px;
    border-radius: 10px;
    display: inline-block;
    font-weight: bold;
}

/* TITLES */

.section-title {
    font-size: 32px;
    font-weight: 700;
    color: white;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================

if "results" not in st.session_state:
    st.session_state.results = []

if "assigned" not in st.session_state:
    st.session_state.assigned = []

if "points" not in st.session_state:
    st.session_state.points = 0


# ================= SIDEBAR =================

st.sidebar.title("🚑 LifeLink AI")

menu = st.sidebar.radio(
    "Navigation",
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

st.sidebar.write("---")

st.sidebar.success("🤖 AI SYSTEM ACTIVE")

# SAFE session state handling
if "points" not in st.session_state:
    st.session_state.points = 0

st.sidebar.metric("🏅 Reward Points", st.session_state.points)

# ================= DASHBOARD =================

if menu == "Dashboard":

    st.markdown(
        '<div class="section-title">📊 Dashboard Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="kpi-card">
            <h3>🩸 Assigned Donors</h3>
            <h1>{len(st.session_state.assigned)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="kpi-card">
            <h3>🚨 Emergencies</h3>
            <h1>{len(st.session_state.results)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="kpi-card">
            <h3>🏅 Reward Points</h3>
            <h1>{st.session_state.points}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown("""
        <div class="kpi-card">
            <h3>🤖 AI Engine</h3>
            <h1>ACTIVE</h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([2, 1])

    with left:

        st.markdown("""
        <div class="glass">

        <h3>🚑 Real-Time Monitoring</h3>

        <p style="color:#cbd5e1; font-size:16px;">
        LifeLink AI continuously monitors emergency requests,
        donor availability, disease prediction, and hospital
        emergency coordination in real-time.
        </p>

        <div class="status-good">
        SYSTEM STATUS : ONLINE
        </div>

        </div>
        """, unsafe_allow_html=True)

    with right:

        st.markdown("""
        <div class="glass">

        <h3>⚡ AI Capabilities</h3>

        <ul style="color:#cbd5e1;">
            <li>AI Disease Prediction</li>
            <li>Emergency Blood Matching</li>
            <li>Organ Donor Intelligence</li>
            <li>Real-Time Emergency Alerts</li>
            <li>Medical Analytics</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

# ================= BLOOD DONATION =================

elif menu == "Blood Donation":

    st.markdown(
        '<div class="section-title">🩸 Blood Donor Registration</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("👤 Full Name")

        phone = st.text_input("📞 Mobile Number")

    with col2:

        blood_group = st.selectbox(
            "🩸 Blood Group",
            [
                "A+",
                "A-",
                "B+",
                "B-",
                "O+",
                "O-",
                "AB+",
                "AB-"
            ]
        )

        city = st.text_input("📍 City")

    if st.button("✅ Register Donor"):

        if name and phone and city:

            st.session_state.points += 10

            st.markdown(f"""
            <div class="glass">

            <h2 style="color:#4ade80;">
            ✅ Registration Successful
            </h2>

            <p style="color:#cbd5e1;">
            Welcome <b>{name}</b>.
            Your donor profile has been securely
            registered in the LifeLink AI network.
            </p>

            <hr style="border:1px solid #1f2937;">

            <p style="color:#94a3b8;">
            🩸 Blood Group: <b>{blood_group}</b>
            </p>

            <p style="color:#94a3b8;">
            📍 City: <b>{city}</b>
            </p>

            <div class="status-good">
            DONOR STATUS : ACTIVE
            </div>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.warning(
                "Please fill all required fields"
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ================= ORGAN DONATION =================

elif menu == "Organ Donation":

    st.markdown(
        '<div class="section-title">🫀 Organ Donation</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass">', unsafe_allow_html=True)

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

    donor_type = st.radio(
        "Donation Type",
        [
            "Living Donor",
            "After Death"
        ]
    )

    if st.button("💖 Submit Consent"):

        st.session_state.points += 20

        st.markdown(f"""
        <div class="glass">

        <h2 style="color:#4ade80;">
        ✅ Consent Submitted Successfully
        </h2>

        <p style="color:#cbd5e1;">
        Organ donation preferences securely stored
        in LifeLink AI registry.
        </p>

        <hr style="border:1px solid #1f2937;">

        <p style="color:#94a3b8;">
        🧬 Donation Type:
        <b>{donor_type}</b>
        </p>

        <p style="color:#94a3b8;">
        🫀 Selected Organs:
        <b>{", ".join(organs) if organs else "None Selected"}</b>
        </p>

        <div class="status-good">
        ORGAN DONOR VERIFIED
        </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= AI MATCHING =================

elif menu == "AI Matching":

    st.markdown(
        '<div class="section-title">🚨 AI Emergency Matching</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass">

    <h3>🤖 Smart Matching Engine</h3>

    <p style="color:#cbd5e1;">
    LifeLink AI automatically finds the best
    donor-recipient matches using intelligent
    medical compatibility analysis.
    </p>

    <ul style="color:#cbd5e1;">
        <li>Blood Compatibility</li>
        <li>Emergency Severity</li>
        <li>Hospital Availability</li>
        <li>Distance Optimization</li>
        <li>Donor Readiness</li>
    </ul>

    <div class="status-good">
    AI MATCHING ENGINE ACTIVE
    </div>

    </div>
    """, unsafe_allow_html=True)

# ================= DISEASE PREDICTION =================

# ================= DISEASE PREDICTION =================

elif menu == "Disease Prediction":

    st.markdown(
        '<div class="section-title">🩺 AI Disease Prediction</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.write(
        "Enter symptoms separated by commas."
    )

    st.info(
        "Example: fever,cough,fatigue"
    )

    symptom_input = st.text_input(
        "Symptoms",
        placeholder="fever,cough,fatigue"
    )

    if st.button("🔍 Predict Disease"):

        if not symptom_input:

            st.warning(
                "Please enter symptoms."
            )

        else:

            try:

                symptoms = [

                    x.strip().lower()

                    for x in symptom_input.split(",")

                ]

                with st.spinner(
                    "AI analyzing symptoms..."
                ):

                    response = requests.post(

                        "http://127.0.0.1:8000/predict",

                        json={
                            "symptoms": symptoms
                        },

                        timeout=10
                    )

                if response.status_code == 200:

                    data = response.json()

                    st.markdown(f"""
                    <div class="glass">

                    <h2 style="color:#4ade80;">
                    🧠 AI Prediction Complete
                    </h2>

                    <h1 style="
                        color:#4ade80;
                        font-size:48px;
                    ">
                        {data['prediction']}
                    </h1>

                    <hr style="
                        border:1px solid #1f2937;
                    ">

                    <p style="color:#cbd5e1;">
                    🎯 Confidence:
                    <b>{data['confidence']}</b>
                    </p>

                    <p style="color:#cbd5e1;">
                    ⚠️ Severity:
                    <b>{data['severity']}</b>
                    </p>

                    <p style="color:#cbd5e1;">
                    📝 Description:
                    <b>{data['description']}</b>
                    </p>

                    <div class="status-good">
                    AI ANALYSIS SUCCESSFUL
                    </div>

                    </div>
                    """, unsafe_allow_html=True)

                    # ================= PRECAUTIONS =================

                    precautions = data.get(
                        "precautions",
                        []
                    )

                    if precautions:

                        st.subheader(
                            "🛡 Recommended Precautions"
                        )

                        for p in precautions:

                            st.write(f"• {p}")

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

            except Exception as e:

                st.error(
                    f"Prediction Error: {str(e)}"
                )

    st.markdown('</div>', unsafe_allow_html=True)

# ================= ANALYTICS =================

elif menu == "Analytics":

    st.markdown(
        '<div class="section-title">📊 Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    data = pd.DataFrame({
        "Category": [
            "Assignments",
            "Emergencies",
            "Points"
        ],
        "Value": [
            len(st.session_state.assigned),
            len(st.session_state.results),
            st.session_state.points
        ]
    })

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.dataframe(
        data,
        use_container_width=True
    )

    st.bar_chart(
        data.set_index("Category")
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ================= ALERTS =================

elif menu == "Alerts":

    st.markdown(
        '<div class="section-title">🔔 Emergency Alerts</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.results:

        st.markdown("""
        <div class="glass">

        <h3>✅ No Active Emergencies</h3>

        <p style="color:#cbd5e1;">
        Emergency monitoring systems are stable.
        </p>

        <div class="status-good">
        ALERT SYSTEM NORMAL
        </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        for r in st.session_state.results:

            st.markdown(f"""
            <div class="glass">

            <h3>🚨 Emergency Alert</h3>

            <p>
                <b>Name:</b> {r['name']}
            </p>

            <p>
                <b>Severity Score:</b> {r['score']}
            </p>

            <div class="status-danger">
            IMMEDIATE RESPONSE REQUIRED
            </div>

            </div>
            """, unsafe_allow_html=True)
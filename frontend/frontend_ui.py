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

st.set_page_config(
    page_title="LifeLink AI",
    layout="wide",
    initial_sidebar_state="expanded"
)


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

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

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

    # ================= HEADER =================

    st.markdown("""
    <style>

    .blood-main-card{
        background: linear-gradient(
            135deg,
            rgba(15,23,42,0.95),
            rgba(30,41,59,0.95)
        );
        padding: 35px;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        backdrop-filter: blur(18px);
        margin-top: 20px;
    }

    .blood-title{
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
    }

    .blood-subtitle{
        color: #cbd5e1;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .blood-badge{
        display:inline-block;
        background: linear-gradient(90deg,#ef4444,#dc2626);
        color:white;
        padding:10px 20px;
        border-radius:50px;
        font-weight:700;
        margin-bottom:20px;
        box-shadow:0 4px 20px rgba(239,68,68,0.4);
    }

    .success-card{
        background: linear-gradient(
            135deg,
            rgba(16,185,129,0.15),
            rgba(5,150,105,0.10)
        );
        border:1px solid rgba(16,185,129,0.4);
        padding:30px;
        border-radius:20px;
        margin-top:25px;
        animation: fadeIn 0.5s ease;
    }

    .info-box{
        background: rgba(255,255,255,0.03);
        border-radius: 18px;
        padding: 20px;
        margin-top: 20px;
        border:1px solid rgba(255,255,255,0.06);
    }

    .status-active{
        background:#22c55e;
        color:white;
        display:inline-block;
        padding:10px 18px;
        border-radius:30px;
        margin-top:15px;
        font-weight:700;
    }

    div[data-testid="stTextInput"] input {
        background-color: rgba(255,255,255,0.04);
        border:1px solid rgba(255,255,255,0.08);
        color:white;
        border-radius:14px;
        padding:12px;
    }

    div[data-testid="stSelectbox"] {
        border-radius:14px;
    }

    .stats-card{
        background: rgba(255,255,255,0.04);
        border:1px solid rgba(255,255,255,0.05);
        border-radius:18px;
        padding:20px;
        text-align:center;
    }

    .stats-number{
        font-size:32px;
        font-weight:800;
        color:#ef4444;
    }

    .stats-label{
        color:#cbd5e1;
        font-size:14px;
    }

    @keyframes fadeIn {
        from {
            opacity:0;
            transform: translateY(20px);
        }
        to {
            opacity:1;
            transform: translateY(0px);
        }
    }

    </style>
    """, unsafe_allow_html=True)


    # ================= LIVE STATS =================

    st.markdown("<br>", unsafe_allow_html=True)

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">12K+</div>
            <div class="stats-label">Registered Donors</div>
        </div>
        """, unsafe_allow_html=True)

    with stat2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">8K+</div>
            <div class="stats-label">Lives Saved</div>
        </div>
        """, unsafe_allow_html=True)

    with stat3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">24/7</div>
            <div class="stats-label">Emergency Support</div>
        </div>
        """, unsafe_allow_html=True)

    with stat4:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">AI</div>
            <div class="stats-label">Smart Matching</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= REGISTRATION FORM =================

    st.markdown('<div class="blood-main-card">', unsafe_allow_html=True)

    st.subheader("📝 Donor Registration Form")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "👤 Full Name",
            placeholder="Enter your full name"
        )

        phone = st.text_input(
            "📞 Mobile Number",
            placeholder="Enter mobile number"
        )

        age = st.number_input(
            "🎂 Age",
            min_value=18,
            max_value=65,
            value=21
        )

    with col2:

        blood_group = st.selectbox(
            "🩸 Blood Group",
            [
                "A+", "A-", "B+", "B-",
                "O+", "O-", "AB+", "AB-"
            ]
        )

        city = st.text_input(
            "📍 City",
            placeholder="Enter your city"
        )

        availability = st.selectbox(
            "🚨 Emergency Availability",
            [
                "Available Anytime",
                "Available During Day",
                "Available During Night",
                "Weekends Only"
            ]
        )

    st.markdown("<br>", unsafe_allow_html=True)


# ================= ORGAN DONATION =================

elif menu == "Organ Donation":

    # ================= CUSTOM CSS =================

    st.markdown("""
    <style>

    .organ-card{
        background: linear-gradient(
            135deg,
            rgba(15,23,42,0.95),
            rgba(30,41,59,0.95)
        );
        padding:35px;
        border-radius:25px;
        border:1px solid rgba(255,255,255,0.08);
        box-shadow:0 8px 32px rgba(0,0,0,0.35);
        margin-top:20px;
    }

    .organ-title{
        font-size:42px;
        font-weight:800;
        color:white;
        margin-bottom:10px;
    }

    .organ-subtitle{
        color:#cbd5e1;
        font-size:17px;
        margin-bottom:25px;
    }

    .top-badge{
        display:inline-block;
        background:linear-gradient(90deg,#ec4899,#db2777);
        color:white;
        padding:10px 20px;
        border-radius:50px;
        font-weight:700;
        margin-bottom:20px;
    }

    .stats-card{
        background:rgba(255,255,255,0.04);
        border-radius:18px;
        padding:20px;
        text-align:center;
        border:1px solid rgba(255,255,255,0.05);
    }

    .stats-number{
        font-size:32px;
        font-weight:800;
        color:#ec4899;
    }

    .stats-label{
        color:#cbd5e1;
        font-size:14px;
    }

    .success-box{
        background:rgba(34,197,94,0.12);
        border:1px solid rgba(34,197,94,0.3);
        padding:25px;
        border-radius:20px;
        margin-top:20px;
    }

    </style>
    """, unsafe_allow_html=True)


    # ================= STATS =================

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">50K+</div>
            <div class="stats-label">Registered Donors</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">12K+</div>
            <div class="stats-label">Lives Saved</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">24/7</div>
            <div class="stats-label">Emergency Support</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">AI</div>
            <div class="stats-label">Smart Matching</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= FORM =================

    with st.container(border=True):

        st.subheader("📝 Organ Donor Registration")

        col1, col2 = st.columns(2)

        with col1:

            donor_name = st.text_input(
                "👤 Full Name",
                placeholder="Enter full name"
            )

            age = st.number_input(
                "🎂 Age",
                min_value=18,
                max_value=80,
                value=21
            )

            city = st.text_input(
                "📍 City",
                placeholder="Enter city"
            )

            donor_type = st.selectbox(
                "🧬 Donation Type",
                [
                    "Living Donor",
                    "After Death"
                ]
            )

        with col2:

            organs = st.multiselect(
                "🫀 Select Organs/Tissues",
                [
                    "Heart",
                    "Kidneys",
                    "Liver",
                    "Lungs",
                    "Pancreas",
                    "Intestines",
                    "Corneas",
                    "Skin",
                    "Bone",
                    "Bone Marrow",
                    "Heart Valves",
                    "Blood Vessels",
                    "Tendons",
                    "Middle Ear",
                    "Hands",
                    "Face Tissue"
                ]
            )

            emergency = st.selectbox(
                "🚨 Emergency Availability",
                [
                    "Available Anytime",
                    "Available During Day",
                    "Available During Night",
                    "Weekends Only"
                ]
            )

            blood_group = st.selectbox(
                "🩸 Blood Group",
                [
                    "A+","A-","B+","B-",
                    "O+","O-","AB+","AB-"
                ]
            )

        consent = st.checkbox(
            "I voluntarily consent to organ donation registration."
        )

        st.markdown("<br>", unsafe_allow_html=True)

        submit = st.button(
            "💖 Submit Organ Donation Consent",
            use_container_width=True
        )

    # ================= SUCCESS =================

    if submit:

        if donor_name and city and organs and consent:

            st.session_state.points += 20

            with st.container(border=True):

                st.success(
                    "✅ Organ Donation Consent Submitted Successfully"
                )

                st.markdown(f"""
                ### 👤 {donor_name}

                🧬 **Donation Type:** {donor_type}

                🩸 **Blood Group:** {blood_group}

                📍 **City:** {city}

                🚨 **Availability:** {emergency}

                🫀 **Selected Organs:** {", ".join(organs)}

                🏅 **Reward Points Earned:** +20
                """)

        else:

            st.error(
                "⚠ Please complete all required fields and consent."
            )

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
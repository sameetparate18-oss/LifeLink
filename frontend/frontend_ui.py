import streamlit as st
import requests

st.title("LifeLink 🚀")

API_URL = "http://127.0.0.1:8000"

# ---------------- LOGIN FORM ----------------
st.subheader("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = requests.post(
        f"{API_URL}/login",
        json={"email": email, "password": password}
    )

    if response.status_code == 200:
        st.success("Login successful!")
        st.json(response.json())
    else:
        st.error("Login failed")
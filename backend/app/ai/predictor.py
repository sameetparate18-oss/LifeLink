import streamlit as st
import google.generativeai as genai

# ================= GEMINI CONFIG =================

genai.configure(
    api_key="AIzaSyDx1lrEg5_Ldryo3LZ0zgI12nHMdK7i0LA"
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# ================= PAGE =================

st.set_page_config(
    page_title="LifeLink AI",
    layout="wide"
)

st.title("🏥 LifeLink AI Assistant")

st.write(
    "Ask anything about health, diseases, symptoms, medicines, fitness, or wellness."
)

# ================= CHAT HISTORY =================

if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY OLD MESSAGES

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= USER INPUT =================

user_input = st.chat_input(
    "Describe symptoms or ask anything..."
)

# ================= AI RESPONSE =================

if user_input:

    # SHOW USER MESSAGE
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI RESPONSE
    with st.chat_message("assistant"):

        with st.spinner("🧠 LifeLink AI Thinking..."):

            prompt = f"""
            You are LifeLink AI Healthcare Assistant.

            Rules:
            - Give professional medical guidance.
            - Do not claim guaranteed diagnosis.
            - Keep responses clear and modern.
            - Suggest doctor consultation when needed.
            - Answer conversationally.

            User Query:
            {user_input}
            """

            response = model.generate_content(prompt)

            ai_reply = response.text

            st.markdown(ai_reply)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_reply
                }
            )
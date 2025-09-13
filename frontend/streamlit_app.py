# frontend/streamlit_app.py
import streamlit as st
import requests, os

API_URL = "http://127.0.0.1:8000/chat"
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
LOGO_PATH = os.path.join(STATIC_DIR, "logo.png")
MASCOT_PATH = os.path.join(STATIC_DIR, "mascot.png")

st.set_page_config(page_title="Aegis — Mascot Chatbot", layout="wide")

# header with logo
cols = st.columns([1,6,1])
with cols[1]:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=220)
    else:
        st.markdown("### Aegis — Mascot Chatbot")

st.write("---")
if "history" not in st.session_state:
    st.session_state.history = []

# Input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")
if submitted and user_input.strip():
    st.session_state.history.append(("You", user_input))
    try:
        r = requests.post(API_URL, json={"message": user_input}, timeout=60)
        j = r.json()
        assistant_msg = j.get("reply", "<no reply>")
        st.session_state.history.append(("Aegis", assistant_msg))
    except Exception as e:
        st.session_state.history.append(("Aegis", f"Error: {e}"))

# Display messages
for who, text in st.session_state.history[::-1]:
    if who == "Aegis":
        c1, c2 = st.columns([1, 8])
        with c1:
            if os.path.exists(MASCOT_PATH):
                st.image(MASCOT_PATH, width=80)
            else:
                st.write("🤖")
        with c2:
            st.markdown(f"**{who}:**")
            st.write(text)
    else:
        st.markdown(f"**{who}:** {text}")

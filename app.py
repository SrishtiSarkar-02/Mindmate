import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# Load environment
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    GROQ_API_KEY = "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"

# Initialize client
client = Groq(api_key=GROQ_API_KEY)

# --- UI Header with Logo ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=80)  # <-- put your logo file in same folder
with col2:
    st.title("🤖 Mindmate")

st.markdown("---")

# --- Mascot Image on Sidebar ---
st.sidebar.image("mascot.png", width=180)  # <-- put your mascot file in same folder
st.sidebar.markdown("### Your friendly AI Mindmate 🤝")

# --- Chat Section ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )
        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

    except Exception as e:
        st.error(f"Error: {str(e)}")

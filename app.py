# app.py - English Version with Conversation History

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import base64
from PIL import Image
import os

# --- API Configuration ---
API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=API_KEY)

# --- Page Config & Styling ---
st.set_page_config(page_title="SHIBRA AI", page_icon="🎙️", layout="centered")

st.markdown("""
<style>
.main { background-color: #0e1117; }
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: #1a1c24;
    border-radius: 10px;
    color: white;
    font-weight: bold;
}
.stTabs [aria-selected="true"] { background-color: #00d4ff; color: black; }
h1 { color: #00d4ff; text-align: center; font-family: 'Segoe UI'; border-bottom: 2px solid #00d4ff; padding-bottom: 10px; }
.stInfo { background-color: #1a1c24; color: #00d4ff; border: 1px solid #00d4ff; }
.chat-container { max-height: 400px; overflow-y: auto; border: 1px solid #00d4ff; padding: 10px; border-radius: 10px; }
.user-msg { color: #00d4ff; font-weight: bold; }
.ai-msg { color: white; margin-left: 10px; }
</style>
""", unsafe_allow_html=True)

# --- Text to Speech Function ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        b64 = base64.b64encode(audio_bytes.read()).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    except:
        pass

# --- Load AI Model ---
@st.cache_resource
def load_model():
    models_to_try = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=m_name,
                system_instruction=(
                    "You are Shahid Mehmood's personal assistant 'Shibra'. "
                    "You speak in polite English and assist with every task."
                )
            )
            model.generate_content("hi")
            return model
        except:
            continue
    return genai.GenerativeModel(model_name='gemini-pro')

shibra = load_model()

# --- App UI ---
st.markdown("<h1>🎙️ SHIBRA ADVANCED AI</h1>", unsafe_allow_html=True)

# Initial Welcome
if "greeted" not in st.session_state:
    welcome_msg = "Hello Sir Shahid Mehmood, I am Shibra and ready to assist you!"
    st.session_state.greeted = True
    speak(welcome_msg)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tabs: Vision & Expert Mode
tab1, tab2 = st.tabs(["📷 Vision (Snapshot)", "💻 Expert Mode"])

# --- TAB 1: Live Vision (Snapshot) ---
with tab1:
    st.subheader("Camera Analysis")
    img_file = st.camera_input("Take a snapshot from your camera")

    if img_file:
        img = Image.open(img_file)
        if st.button("Analyze Image"):
            with st.spinner("Analyzing..."):
                try:
                    img_bytes = img_file.read()
                    res = shibra.generate_content([
                        "Analyze this image and provide a detailed English report.",
                        {"mime_type": "image/png", "data": img_bytes}
                    ])
                    st.success(res.text)
                    speak(res.text)
                except Exception as e:
                    st.error(f"Vision Error: {e}")

# --- TAB 2: Expert Mode with Conversation History ---
with tab2:
    st.subheader("Coding and Writing")
    st.write("Type Python, Pine Script, YouTube script, or any other command below:")

    user_query = st.chat_input("Enter your command here...")

    if user_query:
        with st.spinner("Generating..."):
            try:
                res = shibra.generate_content(user_query)
                st.session_state.chat_history.append({"user": user_query, "ai": res.text})
                speak("Sir, your task has been completed.")
            except Exception as e:
                st.error(f"Expert Mode Error: {e}")

    # Display Conversation History
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            st.markdown(f'<div class="user-msg">You: {chat["user"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ai-msg">Shibra: {chat["ai"]}</div><br>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Status: Connected to Shibra Cloud | User: Shahid Mehmood")

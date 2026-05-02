import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import os
from PIL import Image

# --- API Config ---
API_KEY = "AIzaSyC3Ypk4fhJgI-P2cl9WoUio7j2CgiJ25BI"
genai.configure(api_key=API_KEY)

# --- Modern UI Theme (Free CSS) ---
st.set_page_config(page_title="SHIBRA AI", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1c24;
        border-radius: 10px;
        color: white;
    }
    .stTabs [aria-selected="true"] { background-color: #00d4ff; color: black; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Segoe UI'; }
    </style>
    """, unsafe_allow_html=True)

# --- Voice Function ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='ur')
        tts.save("shibra.mp3")
        with open("shibra.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        os.remove("shibra.mp3")
    except: pass

# --- Welcome Logic ---
if "greeted" not in st.session_state:
    salam = "Assalamu Alaikum sir Shahid Mehmood, main Shibra hazir hoon. Hukum karein!"
    st.session_state.greeted = True
    speak(salam)

st.markdown("<h1>🎙️ SHIBRA AI ASSISTANT</h1>", unsafe_allow_html=True)

# --- Features Tabs ---
tab1, tab2, tab3 = st.tabs(["🎤 وائس چیٹ", "📷 لائیو ویژن", "💻 ایکسپرٹ موڈ"])

model = genai.GenerativeModel('gemini-1.5-flash-latest', 
    system_instruction="Aap Shahid Mehmood ki assistant 'Shibra' hain. Aapka lehja Pakistani Urdu accent wala hai.")

# 1. Voice Chat Tab
with tab1:
    st.info("Sir Shahid, main sun rahi hoon. Bolne ke liye mic button dabayein.")
    audio = mic_recorder(start_prompt="Bolna shuru karein 🎤", stop_prompt="Rokein ⏹️", key='shibra_mic')
    
    if audio:
        with st.spinner("Shibra is thinking..."):
            res = model.generate_content([
                "Aap Shahid Mehmood ki assistant Shibra hain. Is awaz ka jawab Urdu mein dein.",
                {"mime_type": "audio/wav", "data": audio['bytes']}
            ])
            st.write(f"**شیبرا:** {res.text}")
            speak(res.text)

# 2. Live Vision Tab
with tab2:
    st.subheader("شیبرا کی آنکھیں (Live Camera)")
    cam_file = st.camera_input("کیمرہ آن کریں")
    if cam_file:
        img = Image.open(cam_file)
        if st.button("اسے دیکھو شیبرا"):
            with st.spinner("Analyzing..."):
                res = model.generate_content(["Is tasveer ko dekhein aur Shahid sir ko Urdu mein batayein ye kya hai.", img])
                st.success(res.text)
                speak(res.text)

# 3. Expert Mode (Coding & Writing)
with tab3:
    st.subheader("ایکسپرٹ کوڈنگ اور رائٹنگ")
    user_input = st.chat_input("Write Python code, Forex strategy or YouTube script...")
    if user_input:
        with st.spinner("Generating..."):
            res = model.generate_content(user_input)
            st.code(res.text)
            speak("Sir, aapka kaam ho gaya hai.")

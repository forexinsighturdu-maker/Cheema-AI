# app.py

import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from io import BytesIO
import base64
from PIL import Image
import os

# --- API Configuration ---
# Set your API Key via environment variable for security
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
</style>
""", unsafe_allow_html=True)

# --- Voice Function ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='ur')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        b64 = base64.b64encode(audio_bytes.read()).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Voice Error: {e}")

# --- Load AI Model ---
@st.cache_resource
def load_model():
    models_to_try = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=m_name,
                system_instruction=(
                    "Aap Shahid Mehmood ki personal assistant 'Shibra' hain. "
                    "Aapka lehja intehayi sharif aur Pakistani Urdu accent wala hai. "
                    "Aap har kaam mein unki madad karti hain."
                )
            )
            # Test generation
            model.generate_content("hi")
            return model
        except:
            continue
    # Fallback
    return genai.GenerativeModel(model_name='gemini-pro')

shibra = load_model()

# --- App UI ---
st.markdown("<h1>🎙️ SHIBRA ADVANCED AI</h1>", unsafe_allow_html=True)

# Initial Welcome
if "greeted" not in st.session_state:
    welcome_msg = "Assalamu Alaikum sir Shahid Mehmood, main Shibra hazir hoon. Hukum karein!"
    st.session_state.greeted = True
    speak(welcome_msg)

# Tabs
tab1, tab2, tab3 = st.tabs(["🎤 وائس چیٹ (Voice)", "📷 لائیو ویژن (Vision)", "💻 ایکسپرٹ موڈ (Expert)"])

# --- TAB 1: Voice Chat ---
with tab1:
    st.info("Sir Shahid, main sun rahi hoon. Bolne ke liye neechay button dabayein.")
    audio = mic_recorder(
        start_prompt="ریکارڈنگ شروع 🎤", 
        stop_prompt="روک دیں ⏹️", 
        key='shibra_mic_final'
    )
    
    if audio:
        with st.spinner("شیبرا سوچ رہی ہے..."):
            try:
                # Audio input handling
                response = shibra.generate_content([
                    "Sir Shahid Mehmood ne ye kaha hai, iska jawab Urdu mein dein.",
                    {"mime_type": "audio/wav", "data": audio['bytes']}
                ])
                st.markdown(f"**شیبرا:** {response.text}")
                speak(response.text)
            except Exception as e:
                st.error(f"Maazrat sir, kuch technical masla hai. Dobara koshish karein.\n{e}")

# --- TAB 2: Live Vision ---
with tab2:
    st.subheader("کیمرہ رپورٹ")
    img_file = st.camera_input("کیمرہ سے تصویر لیں")
    
    if img_file:
        img = Image.open(img_file)
        if st.button("اسے دیکھو شیبرا"):
            with st.spinner("تجزیہ ہو رہا ہے..."):
                try:
                    img_bytes = img_file.read()
                    res = shibra.generate_content([
                        "Is tasveer ko dekhein aur Shahid sir ko Urdu mein report dein ye kya hai.",
                        {"mime_type": "image/png", "data": img_bytes}
                    ])
                    st.success(res.text)
                    speak(res.text)
                except Exception as e:
                    st.error(f"Vision Error: {e}")

# --- TAB 3: Expert Mode ---
with tab3:
    st.subheader("کوڈنگ اور رائٹنگ")
    st.write("Python, Pine Script, ya YouTube script ke liye likhein:")
    user_query = st.chat_input("Apni command yahan likhein...")
    
    if user_query:
        with st.spinner("Generating..."):
            try:
                res = shibra.generate_content(user_query)
                st.code(res.text)
                speak("Sir, aapka kaam mukammal ho gaya hai.")
            except Exception as e:
                st.error(f"Expert Mode Error: {e}")

# Footer
st.markdown("---")
st.caption("Status: Connected to Shibra Cloud | User: Shahid Mehmood")

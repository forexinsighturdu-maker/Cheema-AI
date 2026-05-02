import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import os

# --- API Setup ---
API_KEY = "AIzaSyC3Ypk4fhJgI-P2cl9WoUio7j2CgiJ25BI"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Miyan Voice-Video AI", layout="centered")

# آواز نکالنے کا فنکشن
def speak_urdu(text):
    try:
        tts = gTTS(text=text, lang='ur')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        os.remove("response.mp3")
    except: pass

# --- Welcome Greeting ---
if "greeted" not in st.session_state:
    welcome = "Assalamu Alaikum sir Shahid Mehmood, main Miyan AI hazir hoon. Voice ya Video chat shuru karein!"
    st.session_state.greeted = True
    speak_urdu(welcome)

st.title("🎙️ میاں وائس اور ویڈیو چیٹ")

# مینیو
choice = st.sidebar.radio("آپشن منتخب کریں:", ["🎤 وائس چیٹ (Voice)", "📷 ویڈیو چیٹ (Live Vision)"])

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 1. وائس چیٹ ---
if choice == "🎤 وائس چیٹ (Voice)":
    st.subheader("مجھ سے بات کریں")
    # مائیکروفون ریکارڈنگ
    audio = mic_recorder(start_prompt="بولنے کے لیے کلک کریں 🎤", stop_prompt="روک دیں ⏹️", key='recorder')
    
    if audio:
        with st.spinner("میاں سن رہی ہے..."):
            res = model.generate_content([
                "Aap Shahid Mehmood ki assistant Miyan hain. Is awaz ka jawab Urdu accent mein dein.",
                {"mime_type": "audio/wav", "data": audio['bytes']}
            ])
            st.info(f"میاں: {res.text}")
            speak_urdu(res.text)

# --- 2. ویڈیو چیٹ ---
elif choice == "📷 ویڈیو چیٹ (Live Vision)":
    st.subheader("ویڈیو/کیمرہ سے بات کریں")
    img_file = st.camera_input("اپنا کیمرہ آن کریں")
    
    if img_file:
        with st.spinner("میاں دیکھ رہی ہے..."):
            from PIL import Image
            img = Image.open(img_file)
            res = model.generate_content(["اس منظر کو دیکھیں اور شاہد صاحب کو اردو میں بتائیں کیا ہو رہا ہے۔", img])
            st.success(res.text)
            speak_urdu(res.text)
          

import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import os
from PIL import Image

# --- API Configuration ---
API_KEY = "AIzaSyC3Ypk4fhJgI-P2cl9WoUio7j2CgiJ25BI"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Miyan AI Assistant", layout="centered")

# آواز نکالنے کا فنکشن
def speak(text):
    try:
        tts = gTTS(text=text, lang='ur')
        tts.save("reply.mp3")
        with open("reply.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        os.remove("reply.mp3")
    except: pass

# --- Initial Greeting ---
if "greeted" not in st.session_state:
    msg = "Assalamu Alaikum sir Shahid Mehmood, main Miyan hazir hoon. Hukum karein!"
    st.session_state.greeted = True
    speak(msg)

st.title("🎙️ میاں ایڈوانس AI")

# ماڈل کا وہ نام جو 100% کام کرے گا
MODEL_NAME = 'gemini-1.5-flash-latest'

# --- Tabs ---
tab1, tab2 = st.tabs(["🎤 وائس چیٹ", "📷 لائیو ویژن"])

with tab1:
    st.subheader("مجھ سے بات کریں")
    # مائیک ریکارڈر
    audio = mic_recorder(start_prompt="بولیں 🎤", stop_prompt="روک دیں ⏹️", key='voice_recorder')
    
    if audio:
        with st.spinner("میاں سن رہی ہے..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                # آواز کو براہ راست ماڈل کو بھیجنا
                res = model.generate_content([
                    "Aap Shahid Mehmood ki assistant Miyan hain. Is awaz ka jawab Urdu accent mein dein.",
                    {"mime_type": "audio/wav", "data": audio['bytes']}
                ])
                st.info(f"میاں: {res.text}")
                speak(res.text)
            except Exception as e:
                st.error("Model Name Issue! Main purana model try karti hoon...")
                # متبادل ماڈل اگر پہلا کام نہ کرے
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(["Sunaai de raha hai? Urdu mein jawab dein.", {"mime_type": "audio/wav", "data": audio['bytes']}])
                st.write(res.text)

with tab2:
    st.subheader("ویڈیو/تصویر چیٹ")
    img_file = st.camera_input("کیمرہ آن کریں")
    if img_file:
        img = Image.open(img_file)
        if st.button("اسے دیکھو میاں"):
            with st.spinner("تجزیہ ہو رہا ہے..."):
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(["Is tasveer ko dekhein aur Shahid sir ko Urdu mein batayein kya hai.", img])
                st.success(res.text)
                speak(res.text)
              

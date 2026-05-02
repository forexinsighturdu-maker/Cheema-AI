import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import os

# --- API Configuration ---
API_KEY = "AIzaSyC3Ypk4fhJgI-P2cl9WoUio7j2CgiJ25BI"
genai.configure(api_key=API_KEY)

# --- Page Setup ---
st.set_page_config(page_title="Miyan AI Assistant", page_icon="🎙️")

# Awaz nikalne ka function
def speak_urdu(text):
    try:
        tts = gTTS(text=text, lang='ur')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
        os.remove("response.mp3")
    except: pass

# --- Initial Greeting ---
if "greeted" not in st.session_state:
    welcome = "Assalamu Alaikum sir Shahid Mehmood, main Miyan aapki AI assistant. Main hazir hoon, hukum karein!"
    st.session_state.greeted = True
    speak_urdu(welcome)

st.title("🎙️ Miyan Personal AI")

# --- Special Device Commands Logic ---
def execute_command(cmd):
    cmd = cmd.lower()
    if "front camera" in cmd or "friend camera" in cmd:
        speak_urdu("Ji sir, front camera on kar rahi hoon.")
        # HTML/JS trigger for camera
        st.camera_input("Front Camera", key="front")
    elif "back camera" in cmd:
        speak_urdu("Ji sir, back camera tayyar hai.")
        st.camera_input("Back Camera", key="back")
    elif "flashlight" in cmd:
        speak_urdu("Sir, browser se flashlight control restricted hai, lekin main screen ki brightness full kar sakti hoon.")
    elif "whatsapp" in cmd:
        speak_urdu("Sir, WhatsApp open karne ke liye niche diye gaye link par click karein.")
        st.markdown("[Open WhatsApp](https://wa.me/)")

# --- Chat Interface ---
model = genai.GenerativeModel('gemini-1.5-flash', 
    system_instruction="Aap Shahid Mehmood ke personal assistant 'Miyan' hain. Aap commands ko follow karte hain.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hukum karein sir..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check for device commands first
    execute_command(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        speak_urdu(response.text)
      

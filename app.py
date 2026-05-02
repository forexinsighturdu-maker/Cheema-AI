import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import os

# --- API KEY (Wahi jo aapne di thi) ---
API_KEY = "AIzaSyC3Ypk4fhJgI-P2cl9WoUio7j2CgiJ25BI"
genai.configure(api_key=API_KEY)

# --- App Settings ---
st.set_page_config(page_title="Miyan AI Assistant", page_icon="🎙️")

# Urdu Voice Function
def speak_urdu(text):
    try:
        tts = gTTS(text=text, lang='ur')
        tts.save("miyan.mp3")
        with open("miyan.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
        os.remove("miyan.mp3")
    except Exception as e:
        st.error(f"Voice Error: {e}")

# --- Greeting on Start ---
if "greeted" not in st.session_state:
    salam = "Assalamu Alaikum sir Shahid Mehmood, main Miyan aapki AI assistant. Main hazir hoon, hukum karein!"
    st.session_state.greeted = True
    speak_urdu(salam)

st.title("🎙️ Miyan Personal Assistant")
st.write("Shahid Mehmood bhai, main aapki command ka intezar kar rahi hoon.")

# --- Model Definition (FIXED NAME) ---
# Yahan 'gemini-1.5-flash' likha hai jo ke sahi hai
model = genai.GenerativeModel('gemini-1.5-flash', 
    system_instruction="Aap Shahid Mehmood ke personal assistant 'Miyan' hain. Aapka lehja Pakistani Urdu wala hai.")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Command Process ---
if prompt := st.chat_input("Hukum karein sir..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # AI Response
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            # Bol kar sunana
            speak_urdu(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}. Please check your API key or model name.")
          

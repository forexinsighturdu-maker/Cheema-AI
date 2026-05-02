import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import os

# --- API Configuration ---
API_KEY = "AIzaSyC3Ypk4fhJgI-P2cl9WoUio7j2CgiJ25BI"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Miyan AI Assistant", page_icon="🎙️")

# آواز نکالنے کا فنکشن
def speak(text):
    tts = gTTS(text=text, lang='ur')
    tts.save("miyan.mp3")
    with open("miyan.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    os.remove("miyan.mp3")

# --- UI Layout ---
st.title("🎙️ میاں ایڈوانس AI اسسٹنٹ")

# مینیو میں آپشنز
choice = st.sidebar.selectbox("موڈ منتخب کریں", ["وائس چیٹ", "ویڈیو تجزیہ"])

model = genai.GenerativeModel('gemini-1.5-flash-latest')

if choice == "وائس چیٹ":
    st.subheader("مجھ سے بات کریں (Urdu Voice)")
    
    # وائس ریکارڈنگ بٹن
    audio = mic_recorder(start_prompt="بولنا شروع کریں 🎤", stop_prompt="روک دیں ⏹️", key='recorder')
    
    if audio:
        st.audio(audio['bytes'])
        with st.spinner("میاں سن رہی ہے..."):
            # وائس کو ٹیکسٹ میں بدلنے اور جواب دینے کا عمل
            response = model.generate_content([
                "Aap Shahid Mehmood ke assistant Miyan hain. Is awaz ka jawab Urdu accent mein dein.",
                {"mime_type": "audio/wav", "data": audio['bytes']}
            ])
            st.markdown(f"**میاں کا جواب:** {response.text}")
            speak(response.text)

elif choice == "ویڈیو تجزیہ":
    st.subheader("ویڈیو چیٹ / اینالائسز")
    video_file = st.file_uploader("کوئی ویڈیو اپ لوڈ کریں", type=['mp4', 'mov', 'avi'])
    
    if video_file:
        st.video(video_file)
        user_msg = st.text_input("ویڈیو کے بارے میں کیا پوچھنا ہے؟", "اس ویڈیو میں کیا ہو رہا ہے؟")
        
        if st.button("تجزیہ کریں"):
            with st.spinner("میاں ویڈیو دیکھ رہی ہے..."):
                res = model.generate_content([user_msg, {"mime_type": "video/mp4", "data": video_file.getvalue()}])
                st.write(res.text)
                speak(res.text)
              

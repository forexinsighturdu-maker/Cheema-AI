import streamlit as st
import google.generativeai as genai
from PIL import Image

# API Key
API_KEY = "AIzaSyC3Ypk4fhJgI-P2cl9WoUio7j2CgiJ25BI"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Shahid AI Mobile", layout="centered")

st.title("📱 Shahid AI Tool")
choice = st.sidebar.selectbox("Menu", ["Chat", "Vision", "Writer"])

if choice == "Chat":
    prompt = st.chat_input("Ask anything...")
    if prompt:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.write(response.text)

elif choice == "Vision":
    file = st.file_uploader("Upload Image", type=['jpg', 'png'])
    if file:
        img = Image.open(file)
        st.image(img)
        if st.button("Analyze"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(["Describe this", img])
            st.write(res.text)

elif choice == "Writer":
    topic = st.text_input("Topic name")
    if st.button("Generate"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Write details about {topic}")
        st.write(res.text)
      

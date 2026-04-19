import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI vs Real Detector")
st.markdown("<h1 style='text-align: center;'>🔍 AI vs Real Detector</h1>", unsafe_allow_html=True)

# API Key সেটিংস
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def detect(img):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(["Is this photo real or AI? Answer in Bengali", img])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

uploaded_file = st.file_uploader("ছবি আপলোড করো...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    if st.button("বিশ্লেষণ শুরু করো"):
        with st.spinner("পরীক্ষা চলছে..."):
            result = detect(image)
            st.write(result)


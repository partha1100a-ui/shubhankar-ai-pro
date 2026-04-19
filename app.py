import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজ সেটআপ
st.set_page_config(page_title="AI Detector")
st.title("🔍 AI vs Real Detector")

# ২. এপিআই কি সেটআপ
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def analyze(img):
    # আমরা এখানে মডেলের নামের ২-৩টি ভার্সন ট্রাই করব যাতে কোনোভাবেই 404 না আসে
    try:
        # ট্রাই ১: সবথেকে লেটেস্ট পদ্ধতি
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(["Is this a real photo or AI? Answer in Bengali", img])
        return response.text
    except:
        try:
            # ট্রাই ২: পুরনো ভার্সন পদ্ধতি (যাতে ৪-০-৪ না আসে)
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content(["Is this photo real or AI? Answer in Bengali", img])
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

# ৩. ইউজার ইন্টারফেস
file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    if st.button("বিশ্লেষণ শুরু করো"):
        with st.spinner("চেক করা হচ্ছে..."):
            result = analyze(img)
            st.write(result)

import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI vs Real Detector")
st.title("🔍 AI vs Real Image Detector")

# এপিআই কি কানেক্ট করা
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def analyze_image(img):
    try:
        # আমরা কোনো নাম দেব না, সিস্টেমকে বলব ছবি চেনার যোগ্য মডেল খুঁজে নিতে
        model_list = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # সবথেকে লেটেস্ট মডেলটি বেছে নেবে যা ৪-০-৪ দেবে না
        final_model_name = ""
        for m in model_list:
            if "1.5-flash" in m.name:
                final_model_name = m.name
                break
        
        if not final_model_name:
            final_model_name = "models/gemini-pro-vision" # ব্যাকআপ

        model = genai.GenerativeModel(final_model_name)
        response = model.generate_content(["এটি কি এআই দিয়ে তৈরি নাকি আসল ছবি? কারণসহ বাংলায় উত্তর দাও।", img])
        return response.text
    except Exception as e:
        return f"দুঃখিত, গুগল সার্ভার থেকে এই সমস্যাটি হচ্ছে: {str(e)}"

# ইউজার ইন্টারফেস
file = st.file_uploader("ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    if st.button("বিশ্লেষণ শুরু করো"):
        with st.spinner("এআই পরীক্ষা করছে..."):
            result = analyze_image(img)
            st.write(result)

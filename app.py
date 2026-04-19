import streamlit as st
import google.generativeai as genai
from PIL import Image

# সেটিংস ও ডিজাইন
st.set_page_config(page_title="AI vs Real Detector", page_icon="🔍")
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🔍 AI vs Real Image Detector</h1>", unsafe_allow_html=True)
st.write("---")

# API Key কানেক্ট করার নিরাপদ পদ্ধতি
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("Secrets-এ 'GOOGLE_API_KEY' খুঁজে পাওয়া যায়নি।")
except Exception as e:
    st.error(f"API কানেকশনে সমস্যা: {e}")

# মেইন ফাংশন
def check_image(img):
    try:
        # আমরা এখানে সবথেকে স্টেবল মডেলটি ব্যবহার করছি
        model = genai.GenerativeModel('gemini-pro-vision')
        prompt = "Analyze this image. Is it a real photograph or AI-generated? Give reasons in Bengali."
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"দুঃখিত, একটি সমস্যা হয়েছে: {str(e)}"

# ইউজার ইন্টারফেস
uploaded_file = st.file_uploader("যেকোনো ছবি আপলোড করো...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="আপনার আপলোড করা ছবি", use_container_width=True)
        
        if st.button("বিশ্লেষণ শুরু করো"):
            with st.spinner("এআই ছবিটি পরীক্ষা করছে..."):
                result = check_image(image)
                st.subheader("ফলাফল:")
                st.write(result)
    except Exception as e:
        st.error(f"ছবি প্রসেস করতে সমস্যা হয়েছে: {e}")

st.write("---")
st.caption("Created by Shubhankar | Cyber Security Student")

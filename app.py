import streamlit as st
import google.generativeai as genai
from PIL import Image

# সেটিংস ও ডিজাইন
st.set_page_config(page_title="AI vs Real Detector", page_icon="🔍")
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🔍 AI vs Real Image Detector</h1>", unsafe_allow_html=True)
st.write("---")

# API Key কানেক্ট করা
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("দয়া করে Settings > Secrets-এ গিয়ে API Key যোগ করুন।")

# মেইন ফাংশন (যা ছবি পরীক্ষা করবে)
def check_image(img):
    # এটি ছবি চেনার জন্য সবথেকে নির্ভরযোগ্য মডেল
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt = """
    এই ছবিটি খুব ভালো করে পরীক্ষা করো। এটি কি আসল ক্যামেরা দিয়ে তোলা নাকি এআই (AI) দিয়ে বানানো? 
    একটি কনফিডেন্স পারসেন্টেজ (%) দাও এবং ৩টি যুক্তি দাও কেন তোমার এমন মনে হচ্ছে। 
    সম্পূর্ণ উত্তরটি বাংলায় দাও।
    """
    response = model.generate_content([prompt, img])
    return response.text

# ছবি আপলোড করার জায়গা
uploaded_file = st.file_uploader("যেকোনো ছবি আপলোড করো...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="আপনার আপলোড করা ছবি", use_container_width=True)
    
    if st.button("বিশ্লেষণ শুরু করো"):
        with st.spinner("এআই ছবিটি পরীক্ষা করছে..."):
            result = check_image(image)
            st.subheader("ফলাফল:")
            st.write(result)
            st.success("পরীক্ষা সম্পন্ন হয়েছে!")

st.write("---")
st.caption("Created by Shubhankar | AI Security Project 2026")

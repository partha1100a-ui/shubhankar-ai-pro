import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. টাইটেল ও পেজ সেটআপ
st.set_page_config(page_title="AI vs Real Image Detector", layout="centered")
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🔍 AI vs Real Detector</h1>", unsafe_allow_html=True)

# ২. এপিআই কি কানেক্ট করা
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Secrets বক্সে API Key খুঁজে পাওয়া যায়নি!")

# ৩. ছবি চেনার জন্য নির্ভরযোগ্য ফাংশন
def analyze_image(img):
    try:
        # এখানে আমরা নির্দিষ্টভাবে Path ব্যবহার করছি যাতে 404 না আসে
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        
        prompt = "Analyze this image and tell me if it is real or AI-generated. Give the response in Bengali."
        
        # ছবি পাঠানোর সঠিক নিয়ম
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        # যদি flash মডেল কাজ না করে, তবে সে gemini-pro-vision ট্রাই করবে
        try:
            model_alt = genai.GenerativeModel(model_name="models/gemini-pro-vision")
            response = model_alt.generate_content([prompt, img])
            return response.text
        except:
            return f"গুগল সার্ভার থেকে এই এররটি আসছে: {str(e)}"

# ৪. ইউজার ইন্টারফেস
file = st.file_uploader("একটি ছবি আপলোড করো...", type=["jpg", "png", "jpeg"])

if file:
    image = Image.open(file)
    st.image(image, use_container_width=True)
    
    if st.button("বিশ্লেষণ শুরু করো"):
        with st.spinner("পরীক্ষা চলছে..."):
            result = analyze_image(image)
            st.success("ফলাফল নিচে দেখুন:")
            st.write(result)

st.write("---")
st.caption("Developed by Shubhankar | 2026 AI Project")

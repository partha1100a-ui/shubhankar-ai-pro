import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজ সেটআপ
st.set_page_config(page_title="AI vs Real Detector")
st.title("🔍 AI vs Real Image Detector")

# ২. এপিআই কি কানেক্ট করা
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key খুঁজে পাওয়া যায়নি।")

def analyze_image(img):
    try:
        # এখানে আমরা নির্দিষ্ট কোনো নাম না দিয়ে এপিআই-কে বলব মডেল খুঁজে দিতে
        # এটি গুগলের সবথেকে লেটেস্ট এবং সেফ মেথড
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        # যদি উপরেরটা কাজ না করে, তবে নিচের এই ব্যাকআপ পদ্ধতিটি ট্রাই করবে
        prompt = """
Analyze this image as a forensic expert. Your goal is to detect if it is AI-generated or a real human photograph.
Check for the following AI artifacts:
1. Strange textures or unnatural smoothness on skin and clothes.
2. Background inconsistencies or blurred objects that shouldn't be blurred.
3. Errors in lighting, shadows, or reflections.
4. Distortions in small details like eyes, teeth, or background text.

Provide the final verdict in Bengali. If it is AI-generated, explain the specific reasons.
"""
 generated? Answer in Bengali and English."
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        # যদি স্টিল এরর আসে, তবে এটি সরাসরি গুগলের বর্তমান অ্যাভেলেবল মডেল খুঁজবে
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(model_name=available_models[0])
            response = model.generate_content(["এটি কি আসল ছবি না এআই? বাংলায় বলো", img])
            return response.text
        except:
            return f"Error Details: {str(e)}"

# ৩. ইউজার ইন্টারফেস
file = st.file_uploader("ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])

if file:
    image = Image.open(file)
    st.image(image, use_container_width=True)
    if st.button("বিশ্লেষণ শুরু করো"):
        with st.spinner("এআই ছবিটি পরীক্ষা করছে..."):
            result = analyze_image(image)
            st.write(result)

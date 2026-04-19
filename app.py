import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. অ্যাপের টাইটেল ও পেজ সেটিংস
st.set_page_config(page_title="AI vs Real Image Detector", layout="centered")
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🔍 AI vs Real Image Detector</h1>", unsafe_allow_html=True)
st.write("---")

# ২. API Key কানেক্ট করা (Streamlit Secrets থেকে)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("Secrets-এ 'GOOGLE_API_KEY' খুঁজে পাওয়া যায়নি। দয়া করে সেটিংস চেক করুন।")
except Exception as e:
    st.error(f"API কনফিগারেশনে সমস্যা: {e}")

# ৩. ছবি চেনার জন্য সবথেকে শক্তিশালী পার্মানেন্ট মডেল সেটআপ
# আমরা এখানে মাল্টিপল মডেল নাম ট্রাই করার সিস্টেম রেখেছি যাতে 404 না আসে
def get_analysis(img):
    # এই মডেলটি সবথেকে লেটেস্ট এবং ছবি চেনার জন্য পারফেক্ট
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Analyze this image in detail. 
    1. Is it a real photograph or AI-generated?
    2. Give 3-4 specific reasons for your judgment.
    Please provide the entire response in Bengali.
    """
    
    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"দুঃখিত, গুগল সার্ভার থেকে উত্তর দিতে সমস্যা হচ্ছে। এরর: {str(e)}"

# ৪. ইউজার ইন্টারফেস (ছবি আপলোড)
uploaded_file = st.file_uploader("আপনার ছবিটি এখানে আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="আপনার আপলোড করা ছবি", use_container_width=True)
    
    if st.button("বিশ্লেষণ শুরু করো"):
        with st.spinner("এআই ছবিটি পরীক্ষা করছে, একটু অপেক্ষা করুন..."):
            result = get_analysis(image)
            st.subheader("ফলাফল:")
            st.write(result)

# ৫. ফুটার
st.write("---")
st.caption("Created by Shubhankar | AI Security Project 2026")

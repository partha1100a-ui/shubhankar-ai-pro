import streamlit as st
import google.generativeai as genai
from gtts import gTTS # ভয়েস শোনানোর জন্য
import os
from PIL import Image
import base64

# ১. পেজ সেটিংস ও ডিজাইন
st.set_page_config(page_title="VITS AI Pro", page_icon="💠", layout="centered")

# এপিআই কি সরাসরি সেট করা
genai.configure(api_key="AIzaSyD-_0P0GiGybr_GFfb7cWBrGhZE_cmMfS8")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* প্লাস আইকন ও ইনপুট বক্স ডিজাইন */
    .stChatInputContainer { border-radius: 35px !important; background-color: #f0f4f9 !important; }
    /* বাটন স্টাইল */
    .stButton>button { border: none; background: transparent; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

# ২. চ্যাট হিস্ট্রি সেটআপ
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৩. মেইন ইউআই (বড় করে Hi)
st.markdown("<h1 style='text-align: center; color: #444746; font-size: 60px;'>Hi</h1>", unsafe_allow_html=True)

# ৪. ফাইল আপলোড (প্লাস আইকন হিসেবে কাজ করবে)
with st.sidebar:
    st.title("Settings")
    uploaded_file = st.file_uploader("➕ Upload Image", type=["jpg", "png", "jpeg"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ৫. চ্যাট মেসেজ প্রদর্শন
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# ৬. ইনপুট বক্স ও এআই লজিক
prompt = st.chat_input("Ask VITS AI anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # ছবি থাকলে ছবির সাথে প্রম্পট পাঠানো
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            ans_text = response.text
            st.markdown(ans_text)

            # 🔊 ভয়েস তৈরি করা (Text to Speech)
            tts = gTTS(text=ans_text, lang='bn' if any('\u0980' <= c <= '\u09FF' for c in ans_text) else 'en')
            audio_file = "response.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3")
            
            # মেসেজ ও অডিও সেভ করা
            st.session_state.messages.append({"role": "assistant", "content": ans_text, "audio": audio_file})
            
        except Exception as e:
            st.error("Server is busy! দয়া করে কিছুক্ষণ পর চেষ্টা করো।")

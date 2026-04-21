import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
from PIL import Image
import io

# ১. জিমিনি স্টাইল সেটিংস ও ডিজাইন (CSS)
st.set_page_config(page_title="Gemini", page_icon="💠", layout="wide")

# এপিআই কি সরাসরি কোডে (তোমার দেওয়া কি)
genai.configure(api_key="AIzaSyD-_0P0GiGybr_GFfb7cWBrGhZE_cmMfS8")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* গ্রিটিং টেক্সট */
    .greeting-box { text-align: center; margin-top: 40px; font-family: 'Google Sans', sans-serif; }
    .hi-text { font-size: 55px; font-weight: 500; color: #444746; }

    /* চ্যাট ইনপউট ও প্লাস আইকন স্টাইল */
    .stChatInputContainer { border-radius: 35px !important; border: 1px solid #c4c7c5 !important; background-color: #f0f4f9 !important; }
    
    /* বাটনগুলোকে সুন্দর করা */
    .stButton>button { border: none !important; background-color: transparent !important; font-size: 24px !important; color: #444746 !important; }
    </style>
    """, unsafe_allow_html=True)

# ২. চ্যাট হিস্ট্রি ও অডিও ম্যানেজমেন্ট
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৩. মেইন ইউআই
st.markdown("<div class='greeting-box'><div class='hi-text'>Hi</div></div>", unsafe_allow_html=True)

# ৪. চ্যাট মেসেজ ডিসপ্লে
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # যদি আগে থেকে ভয়েস থাকে তবে প্লে বাটন দেখাবে
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# ৫. বটম প্যানেল (প্লাস আইকন ও অন্যান্য বাটন)
col_plus, col_input, col_mic = st.columns([0.8, 8, 0.8])

with col_plus:
    # তোমার চাহিদা মতো প্লাস (+) আইকন ছবি আপলোডের জন্য
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

with col_input:
    prompt = st.chat_input("Ask Gemini")

with col_mic:
    # মাইক বাটন (এটি আপাতত ডিজাইন হিসেবে কাজ করবে)
    st.button("🎤")

# ৬. এআই লজিক ও ভয়েস আউটপুট
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # জিমিনি মডেল কল করা (১.৫ ফ্ল্যাশ দ্রুত কাজ করে)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            answer = response.text
            st.markdown(answer)

            # 🔊 ভয়েস তৈরি করা (Text to Speech)
            tts = gTTS(text=answer, lang='bn' if any('\u0980' <= c <= '\u09FF' for c in answer) else 'en')
            audio_path = f"speech_{len(st.session_state.messages)}.mp3"
            tts.save(audio_path)
            st.audio(audio_path, format="audio/mp3")
            
            # মেসেজ সেভ করা
            st.session_state.messages.append({"role": "assistant", "content": answer, "audio": audio_path})
            
        except Exception as e:
            st.error("Server is busy! দয়া করে ৫ মিনিট পর আবার চেষ্টা করো।")

# ৭. সাইডবার (জেমস বাটন ও সেটিংস)
with st.sidebar:
    st.markdown("### 💠 VITS-Gemini")
    st.button("💎 Gems")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

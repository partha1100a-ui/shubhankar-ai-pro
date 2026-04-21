import streamlit as st
import google.generativeai as genai
import time

# ১. জিমিনি স্টাইল প্রিমিয়াম লুক
st.set_page_config(page_title="VITS AI Pro", page_icon="💠", layout="centered")

# তোমার নতুন এপিআই কি সরাসরি এখানে বসিয়ে দিলাম
genai.configure(api_key="AIzaSyD-_0P0GiGybr_GFfb7cWBrGhZE_cmMfS8")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .hi-box { text-align: center; margin-top: 50px; }
    .hi-main { font-size: 52px; font-weight: 500; color: #444746; font-family: 'Google Sans'; }
    .stChatInputContainer { border-radius: 35px !important; background-color: #f0f4f9 !important; }
    </style>
    """, unsafe_allow_html=True)

# ২. মেইন স্ক্রিন
st.markdown("<div class='hi-box'><div class='hi-main'>Hi</div></div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৩. জিমিনির মগজ ব্যবহার করে উত্তর দেওয়া
prompt = st.chat_input("Ask VITS AI anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            # এখানে আমরা জিমিনিকে ইনস্ট্রাকশন দিচ্ছি নিজের নাম ভোলার জন্য
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction="Your name is VITS AI. You are a highly advanced AI developed by Shubhankar. Never mention Google or Gemini. Answer every question like a pro."
            )
            
            response = model.generate_content(prompt)
            full_response = response.text
            
            # টাইপিং এনিমেশন যাতে মনে হয় এআই ভাবছে
            displayed_text = ""
            for char in full_response:
                displayed_text += char
                response_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.005) # খুব দ্রুত টাইপ হবে
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Server is busy! Please try again in a moment.")

# ৪. সাইডবার
with st.sidebar:
    st.title("💠 VITS AI Settings")
    st.write("Version: 2.0 (Pro)")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

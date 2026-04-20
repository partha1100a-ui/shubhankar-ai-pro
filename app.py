import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime

# ১. গোল্ডেন ও ব্ল্যাক প্রিমিয়াম ইন্টারফেস সেটিংস
st.set_page_config(page_title="Universal AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #d4af37; }
    .stChatInputContainer { border-radius: 30px !important; border: 1px solid #d4af37 !important; background-color: #0a0a0a !important; }
    .title-text { color: #d4af37; text-align: center; font-size: 35px; font-weight: bold; text-shadow: 0 0 10px #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# ২. এপিআই কানেকশন
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing! Please check Streamlit Secrets.")

# ৩. সাইডবার ও হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>Universal AI</h2>", unsafe_allow_html=True)
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("### Scheduler")
    st.date_input("Schedule Date", datetime.date.today())
    st.button("Schedule Now")

# ৪. মেইন ইন্টারফেস
st.markdown("<div class='title-text'>Universal AI Pro</div>", unsafe_allow_html=True)

# প্লাস আইকনের কাজ করার জন্য ফাইল আপলোডার
uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. চ্যাট ইনপুট
prompt = st.chat_input("Ask Universal AI")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            sys_msg = "You are 'Universal AI', created by Shubhankar. Always be 100% accurate."
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([f"{sys_msg}\nUser: {prompt}", img])
            else:
                response = model.generate_content(f"{sys_msg}\nUser: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Error connecting to AI. Please try again.")

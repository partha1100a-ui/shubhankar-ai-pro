import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. জিমিনি স্টাইল সেটিংস (ক্লিন ও সিম্পল)
st.set_page_config(page_title="Universal AI", page_icon="✨", layout="wide")

# সিএসএস দিয়ে জিমিনির মতো লুক তৈরি
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }
    
    /* জিমিনি স্টাইল চ্যাট ইনপুট বক্স */
    .stChatInputContainer {
        border-radius: 50px !important;
        border: 1px solid #e0e0e0 !important;
        background-color: #f0f4f9 !important;
    }
    
    /* লোগো ও টাইটেল স্টাইল */
    .logo-text {
        font-family: 'Google Sans', sans-serif;
        font-size: 30px;
        font-weight: 500;
        color: #1a73e8; /* নীল কালার */
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ২. এপিআই কানেকশন (সহজ পদ্ধতি)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets-এ GOOGLE_API_KEY যোগ করো।")

# ৩. সাইডবার (শুধু নতুন চ্যাট অপশন)
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("<h2 style='color:#1a73e8;'>Universal AI</h2>", unsafe_allow_html=True)
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ৪. মেইন স্ক্রিন (নীল স্টারের লোগো ও নাম)
# এখানে জিমিনির স্টারের বদলে তোমার জন্য একটি সুন্দর নীল স্টারের লোগো দেওয়া হয়েছে
st.markdown("""
    <div class='logo-text'>
        <span style='font-size: 40px;'>💠</span> Universal AI
    </div>
    <p style='color: #5f6368; font-size: 18px;'>How can I help you today?</p>
    """, unsafe_allow_html=True)

# ৫. চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৬. প্লাস বাটন ও চ্যাট ইনপুট (একদম সিম্পল)
# জিমিনির মতো বাম দিকে প্লাস বাটন রাখা হয়েছে ফাইল আপলোড করার জন্য
with st.container():
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

prompt = st.chat_input("Ask Universal AI...")

if prompt:
    # ইউজারের মেসেজ সেভ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর রেসপন্স (পৃথিবীর যেকোনো প্রশ্নের উত্তর দিতে সক্ষম)
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                # সিস্টেম ইনস্ট্রাকশন যেখানে তোমাকে মেকার হিসেবে চেনে
                sys_prompt = "You are 'Universal AI', an advanced knowledge engine built by Shubhankar. Answer accurately like Gemini."
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([f"{sys_prompt}\nUser: {prompt}", img])
                else:
                    response = model.generate_content(f"{sys_prompt}\nUser: {prompt}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Connection Error! তোমার ইন্টারনেট অথবা এপিআই কি চেক করো।")

st.markdown("---")
st.caption("<center>© 2026 Developed by Shubhankar | Powered by Universal AI</center>", unsafe_allow_html=True)

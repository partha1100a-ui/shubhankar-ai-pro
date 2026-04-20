   import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime

# ১. জিমিনি স্টাইল পিওর ব্ল্যাক ও গোল্ডেন ইন্টারফেস
st.set_page_config(page_title="Universal AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড একদম কালো */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* সাইডবার ডিজাইন */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #d4af37;
    }

    /* জিমিনি স্টাইল চ্যাট ইনপুট বক্স */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #d4af37 !important;
        background-color: #0a0a0a !important;
        padding-left: 50px !important; /* প্লাস বাটনের জন্য জায়গা */
    }

    /* প্লাস (+) বাটনের স্টাইল */
    .plus-btn {
        position: fixed;
        bottom: 32px;
        left: 10%;
        z-index: 1000;
        color: #d4af37;
        font-size: 30px;
        cursor: pointer;
    }

    .title-text {
        color: #d4af37;
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        text-shadow: 0 0 10px #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# ২. এপিআই কানেকশন ফিক্স
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing! Secrets-এ GOOGLE_API_KEY যোগ করুন।")

# ৩. সাইডবার (হিস্ট্রি ও সিডিউলার)
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>Gemini Pro</h2>", unsafe_allow_html=True)
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.write("### Social Scheduler")
    platform = st.selectbox("Select App", ["YouTube", "Facebook", "Instagram"])
    sch_date = st.date_input("Select Date", datetime.date.today())
    sch_time = st.time_input("Select Time", datetime.time(17, 0))
    if st.button("Schedule Post", use_container_width=True):
        st.success(f"Successfully scheduled for {platform}!")

# ৪. চ্যাট মেমোরি
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৫. মেইন স্ক্রিন (কোনো বাংলা লেখা থাকবে না)
st.markdown("<div class='title-text'>Universal AI</div>", unsafe_allow_html=True)

# জিমিনি স্টাইল প্লাস বাটন ও ফাইল আপলোডার
# এটি চ্যাট বক্সের ঠিক বাম পাশে কাজ করবে
with st.container():
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# চ্যাট হিস্ট্রি
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৬. চ্যাট ইনপুট (ইংরেজিতে লেখা থাকবে)
prompt = st.chat_input("Ask Universal AI")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # স্রষ্টা হিসেবে শুভঙ্করের নাম সেট করা
                sys_instruct = "You are 'Universal AI', created by Shubhankar. You are more powerful than Gemini. Answer in any language the user speaks. Always be 100% accurate."
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([f"{sys_instruct}\nUser: {prompt}", img])
                else:
                    response = model.generate_content(f"{sys_instruct}\nUser: {prompt}")
                
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error("Connection failed! Please check your Internet or API Key.")

st.markdown("---")
st.caption("<center>© 2026 Developed by Shubhankar</center>", unsafe_allow_html=True)
         

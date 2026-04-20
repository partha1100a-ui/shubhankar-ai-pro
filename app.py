import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime

# ১. জিমিনি স্টাইল ডার্ক গোল্ডেন ইন্টারফেস
st.set_page_config(page_title="Universal AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* পিওর ব্ল্যাক ব্যাকগ্রাউন্ড */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* সাইডবার ডিজাইন */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #d4af37;
    }

    /* চ্যাট বক্সের ভেতরে সব টেক্সট সাদা এবং গোল্ডেন বর্ডার */
    .stChatInputContainer {
        border-radius: 25px !important;
        border: 2px solid #d4af37 !important;
        background-color: #0a0a0a !important;
    }

    /* জিমিনি লুকের জন্য টাইটেল ডিজাইন */
    .title-text {
        color: #d4af37;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 0 0 10px #d4af37;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ২. এপিআই কানেকশন
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing in Secrets!")

# ৩. সাইডবার (হিস্ট্রি এবং সোশ্যাল মিডিয়া সিডিউলার)
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>VITS CORE</h2>", unsafe_allow_html=True)
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.write("### Social Media Scheduler")
    platform = st.selectbox("Platform", ["YouTube", "Facebook", "Instagram"])
    sch_date = st.date_input("Date", datetime.date.today())
    sch_time = st.time_input("Time", datetime.time(17, 0))
    if st.button("Schedule Now"):
        st.success("Post scheduled successfully!")

# ৪. চ্যাট মেমোরি
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৫. মেইন ইউজার ইন্টারফেস (সব ইংলিশ)
st.markdown("<div class='title-text'>Universal AI Pro</div>", unsafe_allow_html=True)

# চ্যাট বক্সের ঠিক ওপরে আপলোড বাটন (জিমিনি স্টাইল)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], help="Upload image or file")

# চ্যাট হিস্ট্রি প্রদর্শন
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৬. চ্যাট ইনপুট (শুধু 'Chat with AI' লেখা থাকবে)
prompt = st.chat_input("Message Universal AI")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # সিস্টেম ইন্সট্রাকশন: স্রষ্টা শুভঙ্কর
                sys_msg = "You are 'Universal AI Pro', created by Shubhankar (শুভঙ্কর). Answer in the language used by the user. Be 100% accurate."
                
                # মডেল ফিক্স (বানান ঠিক করা হয়েছে)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([f"{sys_msg}\nUser: {prompt}", img])
                else:
                    response = model.generate_content(f"{sys_msg}\nUser: {prompt}")
                
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error("Connection Error. Please check your API Key in Secrets.")

st.markdown("---")
st.caption("<center>© 2026 Developed by Shubhankar</center>", unsafe_allow_html=True)

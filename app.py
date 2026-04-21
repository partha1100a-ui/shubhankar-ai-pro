import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. জিমিনি স্টাইল সেটিংস
st.set_page_config(page_title="Gemini", page_icon="💠", layout="wide")

# এপিআই কি সরাসরি কোডে সেট করা হলো
genai.configure(api_key="AIzaSyAlK9KDydACqvDM9iS3sr57RxuLbO-6PBw")

# ২. জিমিনির মতো ক্লিন এবং সাদা ওয়ালপেপার ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1f1f1f; }
    
    /* জিমিনি স্টাইল বড় গ্রিটিং টেক্সট */
    .greeting-box {
        text-align: center;
        margin-top: 100px;
        font-family: 'Google Sans', sans-serif;
    }
    .hi-text { font-size: 56px; font-weight: 500; color: #444746; }
    .start-text { font-size: 56px; font-weight: 500; color: #d0d0d0; margin-top: -15px; }

    /* চ্যাট ইনপুট বক্স জিমিনি স্টাইল */
    .stChatInputContainer {
        border-radius: 35px !important;
        border: 1px solid #c4c7c5 !important;
        background-color: #f0f4f9 !important;
    }
    
    /* সাইডবার হাইড বা মডিফাই */
    [data-testid="stSidebar"] { background-color: #f0f4f8; }
    </style>
    """, unsafe_allow_html=True)

# ৩. জিমিনি হোম স্ক্রিন (শুধু 'Hi' থাকবে)
st.markdown("""
    <div class='greeting-box'>
        <div class='hi-text'>Hi</div>
        <div class='start-text'>Where should we start?</div>
    </div>
    """, unsafe_allow_html=True)

# ৪. সেশন স্টেট (মেসেজ সেভ রাখা)
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট স্ক্রিনে আগের মেসেজগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. জিমিনি বাটন লেআউট (ইনপুট বক্সের বাম ও ডান পাশে)
col_plus, col_gems, col_space, col_mic, col_cam = st.columns([0.5, 0.5, 7, 0.5, 0.5])

with col_plus:
    # প্লাস (+) বাটন দিয়ে ফাইল আপলোড
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
with col_gems:
    st.button("💎") # জিমিনির জেমস বাটন

with col_mic:
    st.button("🎤") # মাইক

with col_cam:
    st.button("📷") # ক্যামেরা

# ৬. চ্যাট ইনপুট
prompt = st.chat_input("Ask Gemini")

if prompt:
    # ইউজার মেসেজ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর উত্তর (গুগল জেমিনি মডেল)
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Connection Error! দয়া করে ইন্টারনেট কানেকশন চেক করো।")

# সাইডবার সেটিংস
with st.sidebar:
    st.markdown("### Recent")
    st.button("➕ New chat", use_container_width=True)

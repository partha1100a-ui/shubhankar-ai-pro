import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. জিমিনি স্টাইল সেটিংস
st.set_page_config(page_title="Gemini", page_icon="💠", layout="centered")

# তোমার নতুন এপিআই কি সরাসরি সেট করা হলো
genai.configure(api_key="AIzaSyD-_0P0GiGybr_GFfb7cWBrGhZE_cmMfS8")

# ২. জিমিনি লুকের জন্য প্রিমিয়াম CSS (বাটনগুলো এক লাইনে রাখার জন্য)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* গ্রিটিং বক্স */
    .hi-box { text-align: center; margin-top: 60px; font-family: 'Google Sans', sans-serif; }
    .hi-main { font-size: 52px; font-weight: 500; color: #444746; }
    .hi-sub { font-size: 52px; font-weight: 500; color: #d0d0d0; margin-top: -15px; }

    /* চ্যাট ইনপুট বক্স জিমিনি স্টাইল */
    .stChatInputContainer {
        border-radius: 35px !important;
        border: 1px solid #c4c7c5 !important;
        background-color: #f0f4f9 !important;
    }
    
    /* বাটনগুলোকে ছোট ও ক্লিন করা */
    .stButton>button {
        border: none !important;
        background-color: transparent !important;
        font-size: 22px !important;
        color: #444746 !important;
        padding: 0px !important;
    }
    
    /* কলামের অ্যালাইনমেন্ট ঠিক করা */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. মেইন স্ক্রিন গ্রিটিং
st.markdown("<div class='hi-box'><div class='hi-main'>Hi</div><div class='hi-sub'>Where should we start?</div></div>", unsafe_allow_html=True)

# ৪. বাটন প্যানেল (৫টি কলামে সাজানো যাতে এক লাইনে থাকে)
c1, c2, c3, c4, c5 = st.columns([0.6, 0.6, 7, 0.6, 0.6])

with c1:
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
with c2:
    st.button("💎")

# সেশন স্টেট (মেসেজ স্টোর করা)
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট স্ক্রিন প্রদর্শন
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with c3:
    prompt = st.chat_input("Ask Gemini")

with c4:
    st.button("🎤")
with c5:
    st.button("📷")

# ৫. এআই রেসপন্স লজিক
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
        except Exception as e:
            st.error("API-তে সমস্যা হচ্ছে। অনুগ্রহ করে কি-টি আবার চেক করো।")

# সাইডবার
with st.sidebar:
    st.markdown("### Recent")
    st.button("➕ New chat", use_container_width=True)

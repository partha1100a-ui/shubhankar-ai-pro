import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. অরিজিনাল জিমিনি লুকের জন্য সেটিংস
st.set_page_config(page_title="Gemini", page_icon="💠", layout="wide")

# এপিআই কি সরাসরি সেট করা (তোমার দেওয়া কি)
genai.configure(api_key="AIzaSyAlK9KDydACqvDM9iS3sr57RxuLbO-6PBw")

# CSS দিয়ে বাটন এবং টেক্সট একদম জিমিনির মতো সাজানো
st.markdown("""
    <style>
    /* ব্যাকগ্রাউন্ড সাদা এবং টেক্সট জিমিনি স্টাইল */
    .stApp { background-color: #ffffff; color: #1f1f1f; }
    
    /* গ্রিটিং টেক্সট (Hi) */
    .hi-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 30vh;
        font-family: 'Google Sans', sans-serif;
    }
    .hi-text { font-size: 56px; font-weight: 500; color: #444746; }
    .sub-text { font-size: 56px; font-weight: 500; color: #b7b7b7; margin-top: -15px; }

    /* চ্যাট ইনপুট বক্স ও বাটন (Fixed at bottom) */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #c4c7c5 !important;
        background-color: #f0f4f9 !important;
        padding-left: 10px !important;
    }
    
    /* সাইডবার সেটিংস */
    [data-testid="stSidebar"] { background-color: #f0f4f8; }
    
    /* লুকানোর জন্য বাড়তি কিছু জিনিস */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ২. মেইন স্ক্রিন গ্রিটিং (Screenshot 4 অনুযায়ী)
st.markdown("""
    <div class='hi-container'>
        <div class='hi-text'>Hi</div>
        <div class='sub-text'>Where should we start?</div>
    </div>
    """, unsafe_allow_html=True)

# ৩. বাটন লেআউট (Screenshot 6 অনুযায়ী - ইনপুটের ঠিক পাশে)
# এখানে কলাম ব্যবহার করে বাটনগুলো এক সারিতে আনা হয়েছে
col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 7, 0.5, 0.5])

with col1:
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
with col2:
    st.button("💎", help="Gems", key="gems")

# ৪. চ্যাট সেশন
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. চ্যাট ইনপুট এবং ডানদিকের বাটন
with col3:
    prompt = st.chat_input("Ask Gemini")

with col4:
    st.button("🎤", help="Voice", key="mic")
with col5:
    st.button("📷", help="Camera", key="cam")

# ৬. এআই লজিক
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
        except:
            st.error("Connection Error! API Key বা ইন্টারনেট চেক করো।")

# ৭. সাইডবার (Screenshot 5 অনুযায়ী)
with st.sidebar:
    st.markdown("### Recent")
    st.button("➕ New chat", use_container_width=True)
    st.markdown("---")
    st.caption("✨ Developed by Shubhankar")

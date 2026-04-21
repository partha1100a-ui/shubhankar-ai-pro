import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. জিমিনি UI থিম সেটিংস
st.set_page_config(page_title="Gemini", page_icon="🌐", layout="wide")

# এপিআই কি কনফিগারেশন (Secrets থেকে সরাসরি)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Please add GOOGLE_API_KEY to your Streamlit Secrets.")

# ২. ডিকশনারি বাটন এবং জিমিনি ইন্টারফেসের জন্য CSS
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp { background-color: #f8fafd; color: #1f1f1f; }
    
    /* টাইটেল এবং গ্রিটিং */
    .greeting-container { text-align: center; margin-top: 80px; }
    .hi-text { font-size: 40px; font-weight: 500; color: #444746; }
    .sub-text { font-size: 40px; font-weight: 500; color: #b7b7b7; margin-top: -10px; }

    /* চ্যাট বক্স ডিজাইন */
    .stChatInputContainer { border-radius: 30px !important; border: 1px solid #c4c7c5 !important; background-color: #ffffff !important; }
    
    /* জিমিনি আইকন বাটন লেআউট */
    .icon-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }
    .left-icons { display: flex; gap: 10px; }
    .right-icons { display: flex; gap: 15px; align-items: center; }
    
    /* সাইডবার লুক */
    [data-testid="stSidebar"] { background-color: #f0f4f8; }
    </style>
    """, unsafe_allow_html=True)

# ৩. ডায়নামিক গ্রিটিং (শুধু "Hi" থাকবে)
st.markdown("""
    <div class='greeting-container'>
        <div class='hi-text'>Hi</div>
        <div class='sub-text'>Where should we start?</div>
    </div>
    """, unsafe_allow_html=True)

# ৪. চ্যাট সেশন হ্যান্ডলিং
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট স্ক্রিন প্রদর্শন
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. বাটন ইন্টারফেস (জিমিনি ডিটো লেআউট)
# কলাম দিয়ে বাটনগুলো সাজানো হয়েছে (প্লাস, সেটিংস, ফাস্ট, মাইক, ওয়েভ)
col_l1, col_l2, col_space, col_r1, col_r2, col_r3 = st.columns([0.5, 0.5, 5, 1, 0.5, 0.5])

with col_l1:
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
with col_l2:
    st.button("⚙️", help="Settings")

with col_r1:
    st.markdown("<span style='background:#eef2f6; padding:5px 12px; border-radius:15px; font-size:14px;'>⚡ Fast</span>", unsafe_allow_html=True)
with col_r2:
    st.button("🎤", help="Voice Input")
with col_r3:
    st.button("📊", help="Audio Analysis")

# ৬. প্রম্পট এবং এআই রেসপন্স
prompt = st.chat_input("Ask Gemini")

if prompt:
    # ইউজারের মেসেজ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর উত্তর
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
            st.error("Connection Error! তোমার ইন্টারনেট অথবা এপিআই কি চেক করো।")

# ৭. সাইডবার (রিসেন্ট চ্যাট লিস্ট)
with st.sidebar:
    st.markdown("### Recent")
    st.button("➕ New chat", use_container_width=True)
    st.markdown("---")
    st.caption("✨ Developed by Shubhankar")

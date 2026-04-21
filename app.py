import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ১. জিমিনি স্টাইল পিওর ব্ল্যাক ইন্টারফেস সেটিংস
st.set_page_config(page_title="Gemini", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* পিওর ব্ল্যাক ব্যাকগ্রাউন্ড এবং হোয়াইট টেক্সট */
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Google Sans', sans-serif; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #333; }
    
    /* জিমিনি স্টাইল টাইটেল ও হেডার */
    .stHeader { color: #ffffff !important; }
    
    /* স্মার্ট চ্যাট ইনপুট বক্স (জিমিনি স্টাইল) */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #444 !important;
        background-color: #0a0a0a !important;
        padding: 5px 15px !important;
    }
    .stChatInputContainer textarea { color: #ffffff !important; }

    /* মেসেজ বাব্বলস (ডার্ক থিম) */
    .stChatMessage.user { background-color: #004a77 !important; border-radius: 15px; }
    .stChatMessage.assistant { background-color: #1a1a1a !important; border-radius: 15px; }
    
    /* গোল আইকন */
    .stAvatar { border-radius: 50%; }
    
    /* আইকন কালার */
    .stIcon { color: #aaa !important; }
    </style>
    """, unsafe_allow_html=True)

# ২. এপিআই কানেকশন
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except:
        st.error("API configuration error.")
else:
    st.error("Missing GOOGLE_API_KEY in Secrets.")

# ৩. সাইডবার (স্ক্রিনশট ১১ অনুযায়ী হিস্ট্রি ও সেটিংস)
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.write("## 📄 Chats")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    
    st.write("### Recent Conversations")
    for msg in st.session_state.messages[-6:]:
        if msg["role"] == "user":
            st.caption(f"💬 {msg['content'][:25]}...")
    st.markdown("---")
    st.write("Settings | Help")

# ৪. মেইন চ্যাট ইন্টারফেস (পুরো জিমিনি লুক)
col1, col2, col3 = st.columns([1,8,1])
with col2:
    st.markdown("<h1 style='text-align:center; font-weight:800; font-size:40px; color:#ffffff;'>Gemini</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>How can I help you today?</p>", unsafe_allow_html=True)

# আগের চ্যাটগুলো দেখানো
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# ৫. জিমিনি স্টাইল চ্যাট ইনপুট ও বাটন লেআউট (স্ক্রিনশট ১০ অনুযায়ী)
# বাম দিকে প্লাস (+) বাটন, ডান দিকে ক্যামেরা এবং মাইক
col1, col2, col3, col4 = st.columns([1,7,1,1])

with col1:
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed", help="Upload image/file")

with col2:
    prompt = st.chat_input("Ask Gemini")

with col3:
    if st.button("📷", help="Camera"):
        st.toast("ক্যামেরা ওপেন হচ্ছে... (এই ফিচারটি ব্রাউজারের অনুমতি সাপেক্ষ)")

with col4:
    if st.button("🎤", help="Voice input"):
        st.toast("মাইক্রোফোন অন হচ্ছে... (কথা বলা শুরু করুন)")

# ৬. চ্যাট প্রসেসিং
if prompt:
    # ইউজারের প্রশ্ন
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই উত্তর জেনারেশন (জিমিনির মতো নিখুঁত)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # মডার্ন জেমিনি ১.৫ ফ্ল্যাশ মডেল ব্যবহার
                model = genai.GenerativeModel('gemini-1.5-flash')
                sys_msg = "You are 'Gemini', developed by Shubhankar. Provide accurate, professional, and detailed answers like a world-class expert. Answer in any language used by the user."
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([f"{sys_msg}\nUser: {prompt}", img])
                else:
                    response = model.generate_content(f"{sys_msg}\nUser: {prompt}")
                
                final_res = response.text
                st.markdown(final_res)
                st.session_state.messages.append({"role": "assistant", "content": final_res})
            except:
                st.error("AI কানেক্ট হতে পারছে না। তোমার এপিআই কি (API Key) বা ইন্টারনেট কানেকশন চেক করো।")

st.markdown("---")
st.caption("<center>© 2026 Developed by Shubhankar</center>", unsafe_allow_html=True)

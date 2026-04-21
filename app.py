import streamlit as st
import google.generativeai as genai

# ১. জিমিনি অরিজিনাল লুক সেটআপ
st.set_page_config(page_title="Gemini", page_icon="🌐", layout="wide")

# তোমার দেওয়া এপিআই কি সরাসরি সেট করা হলো
genai.configure(api_key="AIzaSyAlK9KDydACqvDM9iS3sr57RxuLbO-6PBw")

# CSS দিয়ে জিমিনির মতো বাটন ও ইন্টারফেস তৈরি
st.markdown("""
    <style>
    .stApp { background-color: #f8fafd; color: #1f1f1f; }
    
    /* জিমিনি স্টাইল হেডার */
    .header-text { font-family: 'Google Sans', sans-serif; font-size: 24px; color: #444746; text-align: center; margin-top: 20px; }
    
    /* চ্যাট ইনপুট বক্সের বাটনগুলোর ডিজাইন */
    .stChatInputContainer { border-radius: 28px !important; border: 1px solid #c4c7c5 !important; background-color: #ffffff !important; }
    
    /* নিচের বাটন প্যানেল জিমিনির মতো */
    .button-container { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background-color: #ffffff; border-radius: 30px; margin-top: -60px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# ২. মেইন স্ক্রিন টাইটেল (স্ক্রিনশট ৪ অনুযায়ী)
st.markdown("<div class='header-text'>Gemini</div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; font-weight:400; margin-top:50px;'>Hi Shubhankar</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; font-weight:500; margin-top:-10px; color:#444746;'>Where should we start?</h1>", unsafe_allow_html=True)

# চ্যাট হিস্ট্রি রাখার জন্য সেশন স্টেট
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট মেসেজগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৩. জিমিনি স্টাইল বাটন লেআউট (স্ক্রিনশট ৬ অনুযায়ী)
# এখানে আমরা কলাম ব্যবহার করে বাটনগুলো সাজাবো
col_left_1, col_left_2, col_mid, col_right_1, col_right_2, col_right_3 = st.columns([0.5, 0.5, 5, 1, 0.5, 0.5])

with col_left_1:
    st.button("➕", help="Upload Files")

with col_left_2:
    st.button("🎨", help="Gems")

with col_right_1:
    st.button("⚡ Fast", type="secondary")

with col_right_2:
    st.button("🎤", help="Voice Input")

with col_right_3:
    st.button("📊", help="Audio Wave")

# ৪. চ্যাট ইনপুট
prompt = st.chat_input("Ask Gemini")

if prompt:
    # ইউজারের প্রশ্ন দেখানো
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর উত্তর জেনারেশন
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("সার্ভারে সমস্যা হচ্ছে। অনুগ্রহ করে একটু পর চেষ্টা করো।")

# সাইডবার সেটিংস (স্ক্রিনশট ৫ অনুযায়ী)
with st.sidebar:
    st.markdown("### Recent Chats")
    st.write("✨ তোমাকে কোন কোম্পানি বানিয়েছে...")
    st.write("🚁 এরকম দুটো মোটর দিয়ে কি ড্রোন...")
    st.markdown("---")
    st.button("➕ New chat", use_container_width=True)

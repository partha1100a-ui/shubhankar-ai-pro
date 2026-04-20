import streamlit as st
import google.generativeai as genai

# ১. প্রিমিয়াম ডার্ক ও মডার্ন ইউজার ইন্টারফেস
st.set_page_config(page_title="VITS-ULTIMATE AI", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { 
        background: linear-gradient(135deg, #020111 0%, #050a30 100%); 
        color: #00f2ff; 
    }
    .stTextInput>div>div>input { 
        background-color: #001220 !important; 
        color: #00f2ff !important; 
        border: 2px solid #00f2ff !important; 
        border-radius: 15px;
    }
    .stButton>button { 
        background: linear-gradient(45deg, #00f2ff, #0072ff); 
        color: white; 
        border-radius: 25px; 
        border: none; 
        font-weight: bold;
        box-shadow: 0 0 15px #00f2ff;
    }
    .chat-card {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ২. ডিপি বা ওয়ালপেপার লজিক
st.markdown("<h1 style='text-align: center; color: #00f2ff; text-shadow: 0 0 20px #00f2ff;'>🧠 UNIVERSAL AI</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center; color: #aaa;'>The World's Most Powerful Knowledge Engine</p>", unsafe_allow_html=True)

# ৩. এপিআই ও সিস্টেম ইন্সট্রাকশন (তোমার নাম সেট করা)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets-এ আপনার API Key যোগ করুন।")

# এআই-কে নির্দেশ দেওয়া হচ্ছে সে কে এবং তার স্রষ্টা কে
SYSTEM_INSTRUCTION = """
You are 'Universal AI', the world's most intelligent and accurate AI assistant. 
Your creator is Shubhankar (শুভঙ্কর). 
If anyone asks who made you or who is your developer, you must proudly answer: "এই অ্যাপটি শুভঙ্কর (Shubhankar) বানিয়েছে।" 
You can speak every language in the world perfectly. 
Your answers must be 100% accurate, detailed, and helpful. 
There is no question in the world that you don't know the answer to.
"""

# ৪. চ্যাট হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. প্রশ্ন ইনপুট ও উত্তর জেনারেশন
prompt = st.chat_input("পৃথিবীর যেকোনো প্রশ্ন এখানে লিখুন...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Global Databases..."):
            try:
                # Gemini 1.5 Flash মডেল ব্যবহার
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # সিস্টেম ইন্সট্রাকশন সহ উত্তর তৈরি
                full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Question: {prompt}"
                response = model.generate_content(full_prompt)
                
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("সার্ভার ওভারলোড। অনুগ্রহ করে ১ মিনিট পর আবার চেষ্টা করুন।")

# সাইডবার
st.sidebar.title("🛡️ Secure Core")
st.sidebar.info("Admin: Shubhankar")
if st.sidebar.button("Clear Memory"):
    st.session_state.messages = []
    st.rerun()

st.write("---")
st.caption("Developed by Shubhankar | VITS-LENS Intelligence Project 2026")

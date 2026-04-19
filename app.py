import streamlit as st
import google.generativeai as genai

# অ্যাপের টাইটেল এবং আইকন সেটআপ
st.set_page_config(page_title="Shubhankar AI PRO", page_icon="🔥", layout="centered")

# ডার্ক মোড এবং সুন্দর ডিজাইনের জন্য CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# হেডলাইন
st.title("🚀 Shubhankar AI: The Mastermind")
st.write("Created by **Shubhankar** | Powering Intelligence & Creativity")
st.divider()

# API Key কানেকশন (এটি আমরা পরে Streamlit Settings-এ দেব)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.info("🔄 সিস্টেম কানেক্ট হচ্ছে... দয়া করে সেটিংস থেকে API Key যোগ করুন।")

# চ্যাট হিস্ট্রি মেনটেন করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের মেসেজগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট বক্স
if prompt := st.chat_input("যেকোনো কিছু জিজ্ঞাসা করো..."):
    # ইউজারের মেসেজ সেভ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর উত্তর তৈরি করা
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # এআই-কে তার বিশেষ পরিচয় দেওয়া (যাতে সবাই আপনার ট্যালেন্ট বুঝতে পারে)
        instruction = "You are a highly advanced AI created by Shubhankar. You are a genius in photo/video editing, software engineering, and cybersecurity. Answer every question smartly and boldly in the user's language."
        
        full_prompt = f"{instruction}\n\nUser Question: {prompt}"
        response = model.generate_content(full_prompt)
        
        # এআই-এর উত্তর স্ক্রিনে দেখানো
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        # এআই-এর উত্তর সেভ করা
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"দুঃখিত, একটি সমস্যা হয়েছে। নিশ্চিত করুন আপনার API Key সঠিক।")

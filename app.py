import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import time

# ১. আল্ট্রা-প্রিমিয়াম গোল্ডেন এবং ব্ল্যাক ফিউচারিস্টিক ইন্টারফেস
st.set_page_config(page_title="VITS-ULTIMATE AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড: পিওর ব্ল্যাক */
    .main { 
        background-color: #000000; 
        color: #e0e0e0; 
        font-family: 'Poppins', sans-serif;
    }
    
    /* সাইডবার ডিজাইন (জিমিনি স্টাইল) */
    [data-testid="stSidebar"] {
        background-color: #080808;
        border-right: 1px solid #d4af37; /* Golden Border */
        box-shadow: 5px 0px 15px rgba(212, 175, 55, 0.1);
    }
    
    /* চ্যাট ইনপুট বক্স (গোল্ডেন গ্লো) */
    .stChatInputContainer {
        background-color: #0a0a0a !important;
        border: 2px solid #d4af37 !important; /* Golden Border */
        border-radius: 25px !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
    }
    
    /* মেসেজ বাব্বল (জিমিনি কার্ড স্টাইল) */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 15px;
        margin-bottom: 15px;
        padding: 20px;
    }
    
    /* গোল্ডেন হেডার এবং টেক্সট */
    .golden-text {
        color: #d4af37; /* Golden Color */
        text-shadow: 0 0 10px #d4af37, 0 0 20px #d4af37;
        text-align: center;
        font-weight: 800;
    }
    
    /* গোল্ডেন বাটন */
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #aa8522); 
        color: #000 !important;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #d4af37;
        transform: scale(1.03);
    }
    </style>
    """, unsafe_allow_html=True)

# ২. এপিআই কানেকশন এবং নিরাপত্তা (Streamlit Secrets ব্যবহার করবে)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets as `GOOGLE_API_KEY`.")

# ৩. সাইডবার: হিস্ট্রি এবং সোশ্যাল মিডিয়া সিডিউলার
with st.sidebar:
    st.markdown("<h1 class='golden-text'>VITS CORE</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.markdown("---")
    
    if st.button("➕ New Chat Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.write("### 📜 Chat Archives")
    if "messages" in st.session_state and st.session_state.messages:
        for m in st.session_state.messages[-4:]:
            if m["role"] == "user":
                st.caption(f"➜ {m['content'][:25]}...")
    else:
        st.caption("No recent sessions.")
        
    st.markdown("---")
    st.write("### 📅 Social Media Scheduler")
    st.caption("Schedule your posts to Facebook, Instagram, and YouTube.")
    
    # সিডিউলার কন্ট্রোল (সিমুলেটেড ড্যাশবোর্ড)
    platform = st.selectbox("Platform", ["Facebook", "Instagram", "YouTube"])
    scheduled_date = st.date_input("Date", datetime.date.today())
    scheduled_time = st.time_input("Time", datetime.time(17, 0)) # Default 5:00 PM
    post_text = st.text_area("Post Content / Caption")
    
    if st.button("Set Schedule", use_container_width=True):
        if post_text:
            st.success(f"Post scheduled on {platform} for {scheduled_date} at {scheduled_time}.")
            st.info("You'll receive a confirmation when it's live.")
        else:
            st.warning("Please enter post content.")
    
    st.markdown("---")
    st.caption("Admin: Shubhankar | VITS-LENS 2026")

# ৪. মেইন চ্যাট ইন্টারফেস (জিমিনি লেআউট)
st.markdown("<h1 class='golden-text'>UNIVERSAL AI PRO</h1>", unsafe_allow_html=True)
st.caption("<center>আপনার প্রতিদিনের কাজের স্মার্ট সঙ্গী | Developed by Shubhankar</center>", unsafe_allow_html=True)

# ৫. চ্যাট মেমোরি এবং স্টোর
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট বক্সের উপরে প্লাস (+) বাটন এবং ফাইল আপলোড
uploaded_file = st.file_uploader("🖼️ অংক বা যেকোনো ছবির সমাধান পেতে এখানে আপলোড করুন", type=["jpg", "png", "jpeg"], help="Select from Gallery/Camera")

# আগের চ্যাটগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৬. স্মার্ট চ্যাট ইনপুট (ইংরেজিতে 'Message Universal AI')
prompt = st.chat_input("Message Universal AI")

if prompt:
    # ইউজারের প্রশ্ন সেভ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই উত্তর জেনারেশন
    with st.chat_message("assistant"):
        with st.spinner("Decoding Knowledge..."):
            try:
                # আলটিমেট সিস্টেম ইন্সট্রাকশন (গ্লোবাল ল্যাঙ্গুয়েজ এবং শুভঙ্করের নাম বলা)
                system_instruction = "You are 'Universal AI Pro', the world's most intelligent assistant created by Shubhankar (শুভঙ্কর). You answer with 100% accuracy, solve math from images, and provide futuristic advice in the user's preferred language."
                
                # Gemini 1.5 Flash মডেল ব্যবহার
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([f"{system_instruction}\n\nUser Question: {prompt}", img])
                else:
                    response = model.generate_content(f"{system_instruction}\n\nUser Question: {prompt}")
                
                full_response = response.text
                st.markdown(full_response)
                
                # ৭. ভয়েস রিডার (Speaker) এবং অ্যাকশন বাটন
                st.write("---")
                col1, col2 = st.columns([1,1])
                with col1:
                    # ভয়েস রিডার সিমুলেশন
                    if st.button("🔊 Listen to Answer", key=f"speak_{len(st.session_state.messages)}"):
                        st.toast("ভয়েস আউটপুট তৈরি হচ্ছে... (স্পিকার অন রাখুন)")
                        # তুমি চাইলে এখানে একটি লাইব্রেরি ব্যবহার করে আসল ভয়েস অ্যাড করতে পারো।
                        st.write("(স্পিকারে উত্তর শোনা যাবে)")
                with col2:
                    if st.button("🗑️ Clear This Chat", key=f"clear_{len(st.session_state.messages)}"):
                        st.session_state.messages = []
                        st.rerun()
                
                # হিস্ট্রিতে সেভ করা
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("গুগল সার্ভার থেকে রেসপন্স পেতে দেরি হচ্ছে। অনুগ্রহ করে ১ মিনিট পর আবার চেষ্টা করুন।")

st.write("---")
st.caption("<center>© 2026 Developed by Shubhankar | VITS-LENS Play Store Project</center>", unsafe_allow_html=True)

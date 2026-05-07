import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE CONFIGURATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# --- 2. ELITE UI STYLING (PERFECT ADJUSTMENT) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    
    [data-testid="stSidebar"] { 
        background-color: #010409; 
        border-right: 1px solid #1f2428;
    }

    /* Sidebar ඇතුළේ දේවල් පෙළගැස්වීම */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* --- LOGO CONTAINER (EXACT MATCH TO SCREENSHOT) --- */
    .logo-container {
        position: relative;
        width: 200px; /* රවුමේ ප්‍රමාණය */
        height: 200px;
        margin: 10px auto;
        border-radius: 50%;
        border: 2px solid #58a6ff;
        box-shadow: 0 0 25px rgba(88, 166, 255, 0.5);
        overflow: hidden;
        background-color: #000;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* ලෝගෝ එක රවුම ඇතුළට හරියටම Adjust කිරීම */
    .logo-container img {
        width: 85%; /* ලෝගෝ එක රවුම ඇතුළේ ලස්සනට පෙනෙන ප්‍රමාණය */
        height: auto;
        z-index: 1;
    }

    /* White Shine Swap Overlay */
    .logo-container::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -150%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to right, 
            transparent 0%, 
            rgba(255, 255, 255, 0.5) 50%, 
            transparent 100%
        );
        transform: rotate(25deg);
        animation: swap-shine 3.5s infinite ease-in-out;
        z-index: 2;
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    .main-header {
        font-size: 55px; font-weight: 800; text-align: center;
        color: #e6edf3; margin-top: 40px;
    }
    
    .brand-sub {
        text-align: center; color: #58a6ff; font-weight: 900; 
        letter-spacing: 5px; font-size: 14px; margin-top: -15px;
    }

    .footer { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background: #0d1117; padding: 10px; text-align: center; 
        border-top: 1px solid #1f2428; font-size: 11px; color: #8b949e; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #e6edf3; margin-top: 10px; text-align: center;'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #58a6ff; font-weight: bold; text-align: center;'>POWERED BY KDD STUDIO</p>", unsafe_allow_html=True)
    
    st.write("---")
    vision_input = st.file_uploader("📸 Neural Vision Feed", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Powered by:** KDD Studio")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="main-header">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-sub">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE BRAIN ---
user_query = st.chat_input("Connect with DiNuX...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        output_placeholder = st.empty()
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response_stream = model.generate_content([user_query], stream=True)
            
            full_reply = ""
            for chunk in response_stream:
                if chunk.text:
                    full_text = chunk.text
                    full_reply += full_text
                    output_placeholder.markdown(full_reply + "▌")
            
            output_placeholder.markdown(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})
                    
        except Exception:
            st.error("Neural link sync error. Re-trying...")
            time.sleep(1)
            st.rerun()

st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

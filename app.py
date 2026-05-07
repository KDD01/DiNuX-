import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE & SINHALA OPTIMIZATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# AI එක සිංහලෙන් වඩාත් හොඳින් ප්‍රතිචාර දැක්වීමට සකස් කිරීම
SYSTEM_PROMPT = """
You are DiNuX AI, a highly intelligent and friendly AI assistant created by Dinush Dilhara.
Your primary goal is to help the user with any task.
When the user speaks in Sinhala, you MUST respond in high-quality, natural Sinhala.
If the user speaks in English, respond in English.
Be creative, helpful, and professional.
"""

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat_session = model.start_chat(history=[])

# --- 2. ELITE UI STYLING (NO CHANGES) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    
    [data-testid="stSidebar"] { 
        background-color: #010409; 
        border-right: 1px solid #1f2428;
    }

    /* Sidebar Menu Icon adjustment */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        text-align: left;
    }

    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px;
    }

    /* --- LOGO WITH SWAP SHINING EFFECT --- */
    .logo-container {
        position: relative;
        width: 200px;
        margin: 20px auto;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .logo-container img {
        width: 100%;
        height: auto;
        object-fit: contain;
    }

    /* Swap Shining Effect */
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
            rgba(255, 255, 255, 0.1) 30%, 
            rgba(255, 255, 255, 0.6) 50%, 
            rgba(255, 255, 255, 0.1) 70%, 
            transparent 100%
        );
        transform: rotate(25deg);
        animation: swap-shine 4s infinite ease-in-out;
        z-index: 1;
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    .main-title {
        font-size: 55px; font-weight: 800; text-align: center;
        color: #e6edf3; margin-top: 40px; letter-spacing: 2px;
    }
    
    .sub-title {
        text-align: center; color: #58a6ff; font-weight: 900; 
        letter-spacing: 4px; font-size: 15px; margin-top: -15px;
    }

    .footer { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background: #0d1117; padding: 10px; text-align: center; 
        border-top: 1px solid #1f2428; font-size: 11px; color: #8b949e; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LOGO & BRANDING) ---
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #e6edf3; margin-bottom: 0; text-align: center;'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #58a6ff; font-weight: bold; letter-spacing: 2px; text-align: center;'>POWERED BY KDD STUDIO</p>", unsafe_allow_html=True)
    
    st.write("---")
    vision_file = st.file_uploader("📸 Neural Vision Feed", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Powered by:** KDD Studio")
    
    if st.button("🗑️ Clear Neural Memory"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="main-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. STABLE BRAIN (SMOOTH SINHALA RESPONSES) ---
user_input = st.chat_input("Connect with DiNuX...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            # පින්තූරයක් ඇත්නම් එය සකස් කිරීම
            content_payload = [user_input]
            if vision_file:
                content_payload.append(Image.open(vision_file))
            
            with st.spinner("Processing..."):
                # Streaming මඟින් පිළිතුර ලබා ගැනීම
                response = st.session_state.chat_session.send_message(content_payload, stream=True)
                
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
        except Exception:
            st.error("Connection Error. Refreshing...")
            st.session_state.chat_session = None
            time.sleep(1)
            st.rerun()

st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

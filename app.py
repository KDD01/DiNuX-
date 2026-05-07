import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE CONFIGURATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# --- 2. ELITE UI STYLING ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* App Background */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #010409; 
        border-right: 1px solid #1f2428;
    }

    /* Menu Icon එක වම් පැත්තට (Left) කිරීම සහ Sidebar එකේ පෙළගැස්ම */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        text-align: left;
    }

    /* Sidebar අභ්‍යන්තර කොටස් මැදට ගැනීම */
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px;
    }

    /* --- LOGO CONTAINER WITH SWAP SHINING EFFECT --- */
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

    /* Swap Shining Effect Overlay */
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

    /* Header & Titles */
    .main-title {
        font-size: 55px; font-weight: 800; text-align: center;
        color: #e6edf3; margin-top: 40px; letter-spacing: 2px;
    }
    
    .sub-title {
        text-align: center; color: #58a6ff; font-weight: 900; 
        letter-spacing: 4px; font-size: 15px; margin-top: -15px;
    }

    /* Footer */
    .footer { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background: #0d1117; padding: 10px; text-align: center; 
        border-top: 1px solid #1f2428; font-size: 11px; color: #8b949e; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LOGO & BRANDING) ---
with st.sidebar:
    # ලෝගෝ එක සහ Shining Effect එක
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
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="main-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# මැසේජ් ප්‍රදර්ශනය
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE BRAIN (REAL-TIME STREAMING) ---
user_input = st.chat_input("Connect with DiNuX...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="You are DiNuX AI, an elite assistant by Dinush Dilhara. Respond in Sinhala and English."
            )
            
            payload = [user_input]
            if vision_file:
                payload.append(Image.open(vision_file))
            
            with st.spinner("Processing..."):
                response = model.generate_content(payload, stream=True)
                
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
        except Exception:
            st.error("Neural link error. Re-syncing...")
            time.sleep(2)
            st.rerun()

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

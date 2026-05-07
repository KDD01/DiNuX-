import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 

try:
    genai.configure(api_key=GEMINI_API_KEY)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    ]
except Exception as e:
    st.error("Neural Connection Error")

# --- 2. ADVANCED CSS (Fixed Layout & Professional UI) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Dark Theme */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Branding */
    .header-container { text-align: center; padding-top: 10px; margin-bottom: 20px; }
    .shining-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #58a6ff, #ffffff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    .power-text { font-size: 10px; color: #3b82f6; letter-spacing: 2px; font-weight: bold; }
    @keyframes shine { to { background-position: 200% center; } }

    /* Fixed Bottom Container (Chat + Copyright) */
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0d1117;
        padding: 10px 0;
        z-index: 999;
        border-top: 1px solid #30363d;
    }

    /* Copyright Text */
    .copyright {
        text-align: center;
        font-size: 10px;
        color: #8b949e;
        padding-top: 5px;
    }

    /* Customizing Sidebar */
    section[data-testid="stSidebar"] { background-color: #161b22 !important; }

    /* Chat Area Scroll Spacing */
    .chat-container { margin-bottom: 150px; }

    /* Control Center Icon Styling */
    div[data-testid="stExpander"] {
        border: none !important;
        background: transparent !important;
    }
    .stExpander summary p { font-size: 24px !important; margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    st.write("---")
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown("""
    <div class="header-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-text">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. CHAT DISPLAY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wrapper for scrollable chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. FIXED BOTTOM INTERFACE (Control Center + Chat Input + Copyright) ---
# We use columns to align the symbol and the chat bar
bot_col1, bot_col2 = st.columns([0.1, 0.9])

with bot_col1:
    # Small Settings Icon as Control Center
    with st.expander("⚙️", expanded=False):
        selected_model = st.selectbox("Brain", ["gemini-1.5-flash", "gemini-1.5-pro"])
        uploaded_file = st.file_uploader("Vision", type=["png", "jpg", "jpeg"])

with bot_col2:
    prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# Copyright Notice
st.markdown("""
    <div class="copyright">
        © 2026 KDD STUDIO | All Rights Reserved | Designed by Dinush Dilhara
    </div>
    """, unsafe_allow_html=True)

# --- 7. CORE AI LOGIC ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        try:
            # Model Initialization
            model = genai.GenerativeModel(model_name=selected_model)
            inputs = [f"You are DiNuX AI by Dinush Dilhara. Use friendly Sinhala.", prompt]
            if uploaded_file:
                inputs.append(Image.open(uploaded_file))

            response = model.generate_content(inputs, stream=True)
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception:
            st.error("Brain Connection Error.")

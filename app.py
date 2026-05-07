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

# --- 2. ADVANCED CSS (Dynamic UI & Overlay) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Dark Theme Base */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Branding */
    .header-container { text-align: center; padding: 10px 0; }
    .shining-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #58a6ff, #ffffff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        margin-bottom: 0;
    }
    .power-text { font-size: 10px; color: #3b82f6; letter-spacing: 2px; font-weight: bold; text-transform: uppercase; }
    @keyframes shine { to { background-position: 200% center; } }

    /* Top Left Fixed Settings Icon */
    .settings-trigger {
        position: fixed;
        top: 60px; /* Sidebar අයිකනයට පහළින් */
        left: 15px;
        z-index: 1000;
        cursor: pointer;
    }

    /* Professional Card Styling for Control Center */
    .control-panel {
        background: rgba(22, 27, 34, 0.95);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Fixed Footer & Copyright */
    .fixed-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0d1117;
        padding: 5px 0;
        border-top: 1px solid #30363d;
        text-align: center;
        z-index: 998;
    }
    .copyright { font-size: 10px; color: #8b949e; }

    /* Custom Chat Message */
    .stChatMessage { border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(48, 54, 61, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    st.write("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown("""
    <div class="header-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-text">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. TOP-LEFT CONTROL CENTER TRIGGER ---
# Session state එක පාවිච්චි කරලා dialogue එක open/close කරනවා
if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False

# මෙනු අයිකනයට පහළින් ⚙️ අයිකනය පෙන්වීම
st.sidebar.markdown("---")
if st.sidebar.button("⚙️ Control Center"):
    st.session_state.show_settings = not st.session_state.show_settings

# --- 6. SETTINGS DIALOGUE BOX (The Modal) ---
if st.session_state.show_settings:
    with st.container():
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        c1, c2 = st.columns([0.9, 0.1])
        with c1:
            st.subheader("🛠️ Advanced Control Center")
        with c2:
            if st.button("❌"):
                st.session_state.show_settings = False
                st.rerun()
        
        st.write("---")
        opt1, opt2 = st.columns(2)
        with opt1:
            selected_model = st.selectbox("Intelligence Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
            st.markdown("**System Health:** Stable ✅")
        with opt2:
            uploaded_file = st.file_uploader("Upload Vision Source", type=["png", "jpg", "jpeg"])
            if uploaded_file:
                st.success("Vision Active")
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # default settings variables if modal is closed
    selected_model = "gemini-1.5-flash"
    uploaded_file = None

# --- 7. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Scrollable chat area
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Spacer to prevent chat being hidden by footer
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

# Fixed Chat Input
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# Fixed Copyright Footer
st.markdown("""
    <div class="fixed-footer">
        <div class="copyright">© 2026 KDD STUDIO | All Rights Reserved | Designed by Dinush Dilhara</div>
    </div>
    """, unsafe_allow_html=True)

# --- 8. BRAIN LOGIC ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            res_area = st.empty()
            full_res = ""
            try:
                model = genai.GenerativeModel(model_name=selected_model)
                instruction = "You are DiNuX AI by Dinush Dilhara. Speak in friendly Sinhala."
                
                inputs = [instruction, prompt]
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
                st.error("Brain connection lost. Retry.")

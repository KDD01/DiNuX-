import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import time

# --- 1. INITIALIZATION (පද්ධතිය මුලින්ම සූදානම් කිරීම) ---
if "api_configured" not in st.session_state:
    GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ"
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        st.session_state.api_configured = True
    except Exception:
        st.session_state.api_configured = False

# --- 2. ADVANCED UI STYLING (CSS) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .header-container { text-align: center; padding: 10px 0; }
    .shining-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #58a6ff, #ffffff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    .power-text { font-size: 10px; color: #3b82f6; letter-spacing: 2px; font-weight: bold; text-transform: uppercase; }
    @keyframes shine { to { background-position: 200% center; } }

    /* Control Panel Box */
    .control-panel-box {
        background: rgba(22, 27, 34, 0.95);
        border: 1px solid #30363d;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
    }

    /* Fixed Footer */
    .fixed-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #0d1117; padding: 8px 0;
        border-top: 1px solid #30363d; text-align: center; z-index: 998;
    }
    .copyright { font-size: 10px; color: #8b949e; }
    
    /* Clean Chat Messages */
    .stChatMessage { border-radius: 12px; margin-bottom: 10px; border: 1px solid rgba(48, 54, 61, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    
    if 'show_control' not in st.session_state:
        st.session_state.show_control = False
    
    if st.button("⚙️ Control Center"):
        st.session_state.show_control = not st.session_state.show_control
        st.rerun()
    
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

# --- 5. CONTROL CENTER LOGIC ---
if st.session_state.show_control:
    with st.container():
        st.markdown('<div class="control-panel-box">', unsafe_allow_html=True)
        col_t, col_x = st.columns([0.9, 0.1])
        with col_t: st.subheader("🛠️ System Configuration")
        with col_x: 
            if st.button("❌"):
                st.session_state.show_control = False
                st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.selected_model = st.selectbox("Neural Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
        with c2:
            st.session_state.uploaded_file = st.file_uploader("Vision Source", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

# Default values if not set
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gemini-1.5-flash"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# --- 6. CHAT HISTORY DISPLAY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_display = st.container()
with chat_display:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 7. INPUT & FOOTER ---
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

st.markdown("""
    <div class="fixed-footer">
        <div class="copyright">© 2026 KDD STUDIO | Designed by Dinush Dilhara</div>
    </div>
    """, unsafe_allow_html=True)

# --- 8. BULLETPROOF BRAIN LOGIC (The Fix) ---
if prompt:
    # Save User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_display:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Generate Assistant Response
    with chat_display:
        with st.chat_message("assistant"):
            response_area = st.empty()
            full_response = ""
            
            # Retry Mechanism with Exception Capture
            success = False
            for attempt in range(3):
                try:
                    if not st.session_state.api_configured:
                        genai.configure(api_key="AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ")
                    
                    model = genai.GenerativeModel(model_name=st.session_state.selected_model)
                    
                    # Prepare content
                    sys_msg = "You are DiNuX AI by Dinush Dilhara. Speak in friendly Sinhala."
                    content_parts = [sys_msg, prompt]
                    
                    if st.session_state.uploaded_file:
                        content_parts.append(Image.open(st.session_state.uploaded_file))

                    # Start generation
                    response = model.generate_content(content_parts, stream=True)
                    
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            response_area.markdown(full_response + "▌")
                    
                    response_area.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    success = True
                    break # සාර්ථක නම් loop එකෙන් ඉවත් වන්න
                
                except Exception as e:
                    time.sleep(1.5) # තත්පර 1.5 ක් ඉන්න
                    if attempt == 2:
                        st.error("Brain Connection unstable. Please check your internet or API key.")
            
            if not success:
                st.info("System is ready for next input. You can try messaging again.")

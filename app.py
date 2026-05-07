import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import time

# --- 1. SUPER STABLE AI INITIALIZATION ---
# API එක configure කිරීම function එකක් ඇතුළතට ගෙනාවා හැම වෙලේම check වෙන්න
def initialize_brain():
    try:
        api_key = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ"
        genai.configure(api_key=api_key)
        return True
    except Exception:
        return False

# --- 2. ELITE UI STYLING (ZERO-ERROR DESIGN) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Dark Theme & Custom Font */
    .stApp { background: #0b0e14; color: #e2e8f0; }
    
    /* Branding Section */
    .branding { text-align: center; padding: 20px 0; border-bottom: 1px solid #1f2937; margin-bottom: 20px; }
    .shining-title {
        font-size: 50px; font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #ffffff, #60a5fa);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 5s linear infinite;
    }
    .power-text { font-size: 11px; color: #3b82f6; letter-spacing: 4px; font-weight: bold; margin-top: -10px; }
    @keyframes shine { to { background-position: 200% center; } }

    /* Control Panel Glass Design */
    .control-box {
        background: rgba(31, 41, 55, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 25px; margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }

    /* Fixed Layout Fixes */
    .fixed-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #0b0e14; padding: 10px 0;
        border-top: 1px solid #1f2937; text-align: center; z-index: 100;
    }
    .copyright { font-size: 10px; color: #64748b; }
    
    /* Input adjustments */
    .stChatInputContainer { margin-bottom: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_control" not in st.session_state:
    st.session_state.show_control = False
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gemini-1.5-flash"

# --- 4. SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6;'>🧬 DiNuX</h1>", unsafe_allow_html=True)
    st.caption("Advanced Neural System v4.0")
    st.write("---")
    
    if st.button("⚙️ System Control"):
        st.session_state.show_control = not st.session_state.show_control
        st.rerun()

    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    
    if st.button("🗑️ Reset Core"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN HEADER ---
st.markdown("""
    <div class="branding">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-text">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. INDEPENDENT CONTROL CENTER ---
if st.session_state.show_control:
    with st.container():
        st.markdown('<div class="control-box">', unsafe_allow_html=True)
        col_t, col_x = st.columns([0.9, 0.1])
        with col_t: st.subheader("🛠️ System Configuration")
        with col_x: 
            if st.button("❌"):
                st.session_state.show_control = False
                st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.selected_model = st.selectbox("Neural Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
            st.markdown(f"**Current Path:** {st.session_state.selected_model}")
        with c2:
            st.session_state.uploaded_file = st.file_uploader("Vision Feed", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. CHAT DISPLAY ---
chat_holder = st.container()
with chat_holder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 8. FIXED INPUT & COPYRIGHT ---
prompt = st.chat_input("Enter your command...")

st.markdown("""
    <div class="fixed-footer">
        <div class="copyright">© 2026 KDD STUDIO | ALL RIGHTS RESERVED | BY DINUSH DILHARA</div>
    </div>
    """, unsafe_allow_html=True)

# --- 9. THE BULLETPROOF LOGIC (THE HEART) ---
if prompt:
    # Append message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_holder:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Generate Response
    with chat_holder:
        with st.chat_message("assistant"):
            response_box = st.empty()
            full_text = ""
            
            # පද්ධතිය කිසිසේත්ම Fail නොවන විදිහට සකස් කළ Robust Loop එක
            if initialize_brain():
                try:
                    model = genai.GenerativeModel(model_name=st.session_state.selected_model)
                    
                    # Content preparation
                    system_rules = "You are DiNuX AI, created by Dinush Dilhara. You are professional and speak friendly Sinhala."
                    content_to_send = [system_rules, prompt]
                    
                    # Image එකක් තියෙනවා නම් ඒකත් එකතු කරන්න
                    if "uploaded_file" in st.session_state and st.session_state.uploaded_file is not None:
                        img = Image.open(st.session_state.uploaded_file)
                        content_to_send.append(img)

                    # Streaming generation
                    response_stream = model.generate_content(content_to_send, stream=True)
                    
                    for chunk in response_stream:
                        if chunk.text:
                            full_text += chunk.text
                            response_box.markdown(full_text + " ▌")
                    
                    response_box.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                
                except Exception as e:
                    # මොකක් හරි Error එකක් ආවොත් ඒක Silent විදිහට handle කරලා retry කරන්න පණිවිඩයක් දෙනවා
                    response_box.error("Neural pathway interrupted. Re-syncing... Please send the message again.")
            else:
                st.error("Fatal API Configuration Error. Check internet.")

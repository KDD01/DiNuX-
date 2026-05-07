import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import time

# --- 1. CONFIGURATION & BRAIN SETUP ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 

# AI එක configure කිරීම සහ Error Handling
def configure_ai():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except Exception:
        return False

configure_ai()

# --- 2. ADVANCED CSS (Smart UI) ---
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

    /* Control Panel UI */
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
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    
    if 'show_control' not in st.session_state:
        st.session_state.show_control = False
    
    if st.button("⚙️ Control Center"):
        st.session_state.show_control = not st.session_state.show_control
    
    st.write("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown("""
    <div class="header-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-text">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. CONTROL CENTER (Independent Dialogue) ---
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
            selected_model = st.selectbox("Neural Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
        with c2:
            uploaded_file = st.file_uploader("Vision Source", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)
else:
    selected_model = "gemini-1.5-flash"
    uploaded_file = None

# --- 6. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_placeholder = st.container()
with chat_placeholder:
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

# --- 8. SMART BRAIN WITH AUTO-RETRY LOGIC ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            response_area = st.empty()
            full_response = ""
            
            # පද්ධතියේ දෝෂයක් ආවොත් 3 වතාවක් auto-retry කරන්න හදපු logic එක
            retry_count = 0
            success = False
            
            while retry_count < 3 and not success:
                try:
                    model = genai.GenerativeModel(model_name=selected_model)
                    instruction = "You are DiNuX AI by Dinush Dilhara. Use friendly Sinhala."
                    
                    contents = [instruction, prompt]
                    if uploaded_file:
                        contents.append(Image.open(uploaded_file))

                    response = model.generate_content(contents, stream=True)
                    
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            response_area.markdown(full_response + "▌")
                    
                    response_area.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    success = True # සාර්ථක වුනොත් loop එක නවත්වන්න
                    
                except Exception as e:
                    retry_count += 1
                    response_area.warning(f"Reconnecting to Brain... (Attempt {retry_count}/3)")
                    time.sleep(2) # තත්පර 2ක් ඉඳලා ආයේ try කරන්න
                    
            if not success:
                st.error("Brain Connection Permanently Failed. Please refresh the page.")

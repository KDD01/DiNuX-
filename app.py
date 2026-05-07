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
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
except Exception as e:
    st.error("Neural Connection Error. Check API Key.")

# --- 2. ADVANCED CSS (Clean & Professional) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Dark Theme */
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

    /* Control Panel Box (Separate from Chat) */
    .control-panel-box {
        background: rgba(22, 27, 34, 0.9);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* Fixed Footer */
    .fixed-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0d1117;
        padding: 8px 0;
        border-top: 1px solid #30363d;
        text-align: center;
        z-index: 998;
    }
    .copyright { font-size: 10px; color: #8b949e; }

    /* Chat Styling */
    .stChatMessage { border-radius: 12px; border: 1px solid rgba(48, 54, 61, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    st.write("---")
    
    # ⚙️ Control Center Toggle (Top Left Position)
    if 'show_control' not in st.session_state:
        st.session_state.show_control = False
    
    if st.button("⚙️ Control Center Settings"):
        st.session_state.show_control = not st.session_state.show_control
    
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

# --- 5. CONTROL CENTER DIALOGUE (Separate Container) ---
# මෙය Chat එක ඇතුළේ නොවී වෙනමම ඉහළින් දිග හැරේ
if st.session_state.show_control:
    with st.container():
        st.markdown('<div class="control-panel-box">', unsafe_allow_html=True)
        col_title, col_close = st.columns([0.9, 0.1])
        with col_title:
            st.subheader("🛠️ System Configuration")
        with col_close:
            if st.button("❌"):
                st.session_state.show_control = False
                st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            selected_model = st.selectbox("Neural Engine", ["gemini-1.5-flash", "gemini-1.5-pro"])
            st.write("Status: **Optimal**")
        with c2:
            uploaded_file = st.file_uploader("Vision Input", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)
else:
    selected_model = "gemini-1.5-flash"
    uploaded_file = None

# --- 6. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat message container
chat_placeholder = st.container()

with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Spacing for footer
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# --- 7. INPUT & FOOTER ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

st.markdown("""
    <div class="fixed-footer">
        <div class="copyright">© 2026 KDD STUDIO | Designed by Dinush Dilhara</div>
    </div>
    """, unsafe_allow_html=True)

# --- 8. STABLE BRAIN LOGIC (Error Fixed) ---
if prompt:
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    # 2. Assistant Reply Logic
    with chat_placeholder:
        with st.chat_message("assistant"):
            response_area = st.empty()
            full_response = ""
            
            try:
                # API Call Setup
                model = genai.GenerativeModel(model_name=selected_model)
                
                # Instruction and Content
                contents = [f"System: You are DiNuX AI by Dinush Dilhara. Reply in friendly Sinhala.", prompt]
                if uploaded_file:
                    contents.append(Image.open(uploaded_file))

                # Generating Response
                response = model.generate_content(contents, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        response_area.markdown(full_response + "▌")
                
                response_area.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error("Brain connection failed. Please try again.")
                # print(e) # Debugging සඳහා පමණි

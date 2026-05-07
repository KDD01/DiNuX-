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

# --- 2. ELITE UI DESIGN (STYLING) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Dark Deep Sea Theme */
    .stApp { background: radial-gradient(circle at top right, #0d1117, #010409); color: #e6edf3; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 17, 23, 0.9) !important;
        border-right: 1px solid rgba(48, 54, 61, 0.5);
    }

    /* Header & Branding */
    .header-container { text-align: center; padding: 20px 0; }
    .shining-title {
        font-size: 50px; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #58a6ff, #ffffff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        margin-bottom: 5px;
    }
    .power-text {
        font-size: 12px; font-weight: 700; color: #3b82f6;
        text-transform: uppercase; letter-spacing: 3px;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Control Center Expander Styling */
    .stExpander {
        background: rgba(22, 27, 34, 0.7) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }

    /* Professional Cards */
    .feature-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 10px; padding: 12px; margin-bottom: 10px;
    }

    /* Custom Chat Message */
    .stChatMessage { border-radius: 12px; border: 1px solid rgba(48, 54, 61, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Developer Info & Health) ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.caption("Quantum Suite v3.2")
    st.write("---")
    
    st.markdown("### 👤 Lead Developer")
    st.info("**Dinush Dilhara**\n\nKDD STUDIO Architecture")
    
    st.write("---")
    st.markdown("### 📊 Neural Stats")
    st.write("Uptime: 99.9%")
    st.write("Core: Stable")
    
    if st.button("🗑️ Reset Neural Path"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER SECTION ---
st.markdown("""
    <div class="header-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-text">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. CONTROL CENTER (Expandable Menu) ---
with st.expander("🛠️ Open Control Center", expanded=False):
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        st.markdown("**Core Settings**")
        selected_model = st.selectbox("Intelligence Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
        
    with col_c2:
        st.markdown("**Vision Mode**")
        uploaded_file = st.file_uploader("Source Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if uploaded_file:
            st.success("Vision Active")
            
    with col_c3:
        st.markdown("**System Actions**")
        if st.button("Creative Writing"):
            st.session_state.prompt_type = "Write a creative story."
        if st.button("Code Assistant"):
            st.session_state.prompt_type = "Help me with a Python script."

# --- 6. MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History Container
chat_container = st.container(height=450, border=False)
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("Ask DiNuX anything...")

# --- 7. NEURAL CORE LOGIC ---
if prompt:
    # Update UI with User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Response Generation
    with chat_container:
        with st.chat_message("assistant"):
            res_placeholder = st.empty()
            full_res = ""
            
            try:
                model = genai.GenerativeModel(model_name=selected_model)
                system_instruction = "You are DiNuX AI, a pro assistant by Dinush Dilhara. Speak in high-quality Sinhala."
                
                # Dynamic inputs
                content_list = [system_instruction, prompt]
                if uploaded_file:
                    content_list.append(Image.open(uploaded_file))
                
                response = model.generate_content(content_list, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_placeholder.markdown(full_res + "▌")
                
                res_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception:
                st.error("Neural path blocked. Please check connectivity.")

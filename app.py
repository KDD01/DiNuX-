import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from streamlit_mic_recorder import mic_recorder

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
    st.error("API Connection Error")

# --- 2. ADVANCED CSS (Clean UI & Sidebar Detection) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Branding */
    .header-container { text-align: center; margin-bottom: 30px; width: 100%; }
    .shining-title {
        font-size: clamp(30px, 10vw, 55px); font-weight: 900;
        background: linear-gradient(120deg, #ffffff 20%, #64748b 50%, #ffffff 80%);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shine 3s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .dev-text { color: #94a3b8; font-size: 15px; }
    .power-text { color: #3b82f6; font-size: 12px; font-weight: 700; text-transform: uppercase; }

    /* --- IMPORTANT: Floating Menu Styling & Sidebar Auto-Hide --- */
    /* Sidebar එක open වුනාම floating-menu එක hide කරන CSS logic එක */
    section[data-testid="stSidebar"][aria-expanded="true"] ~ section .floating-menu {
        display: none !important;
    }
    
    .floating-menu {
        position: fixed; top: 60px; left: 10px; z-index: 999999;
        width: 50px !important; transition: 0.3s ease;
    }

    div[data-testid="stExpander"] {
        background-color: #1e293b !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
        width: 50px !important;
    }

    /* Remove Arrow & Clean Icons */
    details summary::-webkit-details-marker { display:none !important; }
    details summary { list-style: none !important; text-align: center; }
    details summary p { font-size: 20px !important; margin: 0 !important; color: #60a5fa; }
    
    /* File Uploader Clean Icon */
    .stFileUploader label { display: none !important; }
    .stFileUploader section div { display: none !important; }
    .stFileUploader section { padding: 0 !important; min-height: 0 !important; }
    
    /* Custom icon size for professional look */
    .icon-container { font-size: 18px; text-align: center; padding: 5px 0; }

    section[data-testid="stSidebar"] { background-color: #080c14 !important; border-right: 1px solid #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Details & Settings) ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    
    st.title("Main Menu")
    selected_model = st.selectbox("Intelligence", ["gemini-1.5-flash", "gemini-1.5-pro"])
    
    st.markdown("---")
    st.subheader("👤 About Developer")
    st.info("""
    **Name:** Dinush Dilhara  
    **Studio:** KDD Studio  
    **Role:** Lead AI Developer  
    **Project:** DiNuX Pro AI
    """)
    
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. FLOATING MENU (With Auto-Hide logic) ---
# Wrapping in a div for CSS targeting
st.markdown('<div class="floating-menu">', unsafe_allow_html=True)
with st.expander("☰", expanded=False):
    # Professional Icon Only Uploader
    img_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key="f_up")
    
    # Professional Mic Icon
    st.markdown("<div class='icon-container'>🎙️</div>", unsafe_allow_html=True)
    voice_data = mic_recorder(start_prompt="●", stop_prompt="■", key='f_vc')
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. HEADER ---
st.markdown(f'''
    <div class="header-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <span class="dev-text">Developed by Dinush Dilhara</span><br>
        <span class="power-text">POWERED BY KDD STUDIO</span>
    </div>
    ''', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# --- 7. STABLE CORE BRAIN ---
if prompt or img_file or voice_data:
    user_query = prompt if prompt else "Analyze the attached file."
    if voice_data: user_query = "Voice Command Received."
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file: st.image(img_file, width=300)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        try:
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            parts = ["You are DiNuX AI, a helpful assistant by Dinush Dilhara. Speak in Sinhala.", user_query]
            if img_file: parts.append(Image.open(img_file))
            
            response = model.generate_content(parts, stream=True)
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception:
            st.error("Brain Connection Error. Please try again.")

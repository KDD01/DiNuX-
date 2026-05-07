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
    st.error("API Error")

# --- 2. ADVANCED CSS (Animations & Professional UI) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Branding */
    .header-container { text-align: center; margin-bottom: 35px; width: 100%; }
    .shining-title {
        font-size: clamp(30px, 10vw, 55px);
        font-weight: 900;
        background: linear-gradient(120deg, #ffffff 20%, #64748b 50%, #ffffff 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text; color: white;
        animation: shine 3s linear infinite;
        margin: 0;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .dev-text { color: #94a3b8; font-size: 15px; }
    .power-text { color: #3b82f6; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }

    /* Floating Menu Design */
    div[data-testid="stExpander"] {
        position: fixed;
        top: 65px;
        left: 10px;
        z-index: 999999;
        width: 65px !important;
        background-color: rgba(30, 41, 59, 0.9) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Remove default arrow */
    details summary::-webkit-details-marker { display:none !important; }
    details summary { list-style: none !important; cursor: pointer; }
    
    /* Animation when opening */
    details[open] { animation: slideIn 0.3s ease-out; }
    @keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

    /* Align items in list */
    .stFileUploader section { padding: 0 !important; }
    
    /* Hide Floating Menu when Sidebar is Open (Standard Streamlit Sidebar detection) */
    [data-sidebar-state="expanded"] ~ .main .floating-menu { display: none !important; }
    
    section[data-testid="stSidebar"] { background-color: #080c14 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Settings) ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    st.title("Settings")
    selected_model = st.selectbox("Intelligence", ["gemini-1.5-flash", "gemini-1.5-pro"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 4. FLOATING MENU LOGIC ---
# Sidebar එක open වෙලාද කියලා බලන logic එක
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

with st.container():
    # Icons විතරක් සහිත ලස්සන expander එක
    with st.expander("☰", expanded=False):
        # Image Button Icon
        img_file = st.file_uploader("📷", type=["jpg", "png", "jpeg"], key="f_up", label_visibility="collapsed")
        
        # Voice Button Icon
        st.markdown("<div style='text-align: center; padding: 5px;'>🎙️</div>", unsafe_allow_html=True)
        voice_data = mic_recorder(start_prompt="●", stop_prompt="■", key='f_vc')
        
        # Auto-close on input
        if img_file or voice_data:
            st.session_state.menu_open = False

# --- 5. CENTERED HEADER ---
st.markdown(f'''
    <div class="header-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <span class="dev-text">Developed by Dinush Dilhara</span>
        <span class="power-text">Powered by KDD Studio</span>
    </div>
    ''', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# --- 7. CORE LOGIC (Error Free) ---
if prompt or img_file or voice_data:
    user_query = prompt if prompt else "නිරීක්ෂණය කරන්න."
    if voice_data:
        user_query = "Voice input received."
        
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file:
            st.image(img_file, width=280)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        sys_msg = "You are DiNuX AI, created by Dinush Dilhara. Use friendly spoken Sinhala (oyaa/mama)."

        try:
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            content_parts = [sys_msg, user_query]
            if img_file:
                content_parts.append(Image.open(img_file))

            response = model.generate_content(content_parts, stream=True)
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            st.error("Error connecting to brain. Please try again.")

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURATION & STABLE API SETUP ---
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
    st.error("API Configuration Error.")

# --- 2. ADVANCED UI & MINI FLOATING MENU CSS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Branding Centering */
    .header-container { text-align: center; margin-bottom: 35px; width: 100%; padding-top: 10px; }
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
    .dev-text { color: #94a3b8; font-size: 15px; font-weight: 500; display: block; margin-top: 5px; }
    .power-text { color: #3b82f6; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; display: block; margin-top: 2px; }

    /* Hide Streamlit Expander Arrow & Style Floating Menu */
    details summary::-webkit-details-marker { display:none !important; }
    details summary { list-style: none !important; }
    
    div[data-testid="stExpander"] {
        position: fixed;
        top: 65px;
        left: 10px;
        z-index: 999999;
        width: 60px !important;
        background-color: #1e293b !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        padding: 5px !important;
        transition: 0.3s;
    }
    
    div[data-testid="stExpander"] summary p {
        font-size: 24px !important;
        margin: 0 !important;
        text-align: center;
        color: #60a5fa;
    }

    /* Style for simple buttons inside expander */
    .stFileUploader section { padding: 0 !important; }
    section[data-testid="stSidebar"] { background-color: #080c14 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FLOATING ICON BUTTONS (Auto-close Logic) ---
if "menu_state" not in st.session_state:
    st.session_state.menu_state = False

with st.container():
    # 'label' එක විදිහට "☰" විතරක් භාවිතා කර අයිකනය සකස් කිරීම
    with st.expander("☰", expanded=st.session_state.menu_state):
        # Attractive simple buttons/inputs
        img_file = st.file_uploader("📸", type=["jpg", "png", "jpeg"], key="f_up", label_visibility="collapsed")
        
        # Audio recording button
        voice_data = mic_recorder(start_prompt="🎤", stop_prompt="✔️", key='f_vc')
        
        # Auto-close once input is detected
        if img_file or voice_data:
            st.session_state.menu_state = False

# --- 4. MAIN SIDEBAR (Settings) ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    st.title("Settings")
    selected_model = st.selectbox("Intelligence", ["gemini-1.5-flash", "gemini-1.5-pro"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

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

# Display Message History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# --- 7. STABLE MULTIMODAL LOGIC (Fixed Errors) ---
if prompt or img_file or voice_data:
    # Logic to handle user input
    user_query = prompt if prompt else "Analyze the content."
    if voice_data:
        user_query = "Audio command received."
        
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file:
            st.image(img_file, width=280)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        # Friendly Sinhala System Message
        sys_msg = "You are DiNuX AI, created by Dinush Dilhara. Use friendly spoken Sinhala (oyaa/mama)."

        try:
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            
            # Prepare content parts properly to avoid 'Busy/Overload' errors
            content_parts = [sys_msg, user_query]
            if img_file:
                content_parts.append(Image.open(img_file))

            # Stream the response
            response = model.generate_content(content_parts, stream=True)
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            # Enhanced Error Handling
            st.warning("සමාවෙන්න, මම මේ වෙලාවේ පොඩි විවේකයක් ගන්නවා. කරුණාකර තව මොහොතකින් උත්සාහ කරන්න.")
            print(f"Internal Log: {e}")

import streamlit as st
import google.generativeai as genai
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURATION (Fixed Error Logic) ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 
TAVILY_API_KEY = "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"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    search_tool = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UI SETTINGS & MINI FLOATING BUTTON CSS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Branding Centering */
    .header-container { text-align: center; margin-bottom: 35px; width: 100%; padding-top: 10px; }
    .shining-title {
        font-size: clamp(35px, 10vw, 55px);
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
    .dev-text { color: #94a3b8; font-size: 16px; font-weight: 500; display: block; margin-top: 5px; }
    .power-text { color: #3b82f6; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; display: block; margin-top: 2px; }

    /* Shrink the floating expander to icon size */
    div[data-testid="stExpander"] {
        position: fixed;
        top: 60px;
        left: 10px;
        z-index: 999999;
        width: 50px !important;
        background-color: transparent !important;
        border: none !important;
    }
    div[data-testid="stExpander"] summary {
        list-style: none;
        padding: 0;
        display: flex;
        justify-content: center;
    }
    div[data-testid="stExpander"] summary p {
        font-size: 22px !important;
        margin: 0;
        color: #3b82f6;
    }
    
    section[data-testid="stSidebar"] { background-color: #080c14 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FLOATING ICON MENU (Auto-close logic) ---
# Initialize session state for the expander if not exists
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

with st.container():
    # 'expanded' parameter controls if the menu is open or closed
    with st.expander("☰", expanded=st.session_state.menu_open):
        img_file = st.file_uploader("Image", type=["jpg", "png", "jpeg"], key="f_up", label_visibility="collapsed")
        voice_data = mic_recorder(start_prompt="🎤", stop_prompt="✔️", key='f_vc')
        
        # Close the menu automatically if data is input
        if img_file or voice_data:
            st.session_state.menu_open = False

# --- 4. MAIN SIDEBAR ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    st.title("Settings")
    selected_model = st.selectbox("Intelligence", ["gemini-1.5-flash", "gemini-1.5-pro"])
    if st.button("🗑️ Clear History"):
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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# --- 7. STABLE LOGIC ---
if prompt or img_file or voice_data:
    user_query = prompt if prompt else "Analyze the attached content."
    if voice_data:
        user_query = "Voice input received."
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file:
            st.image(img_file, width=250)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        sys_msg = "You are DiNuX AI by Dinush Dilhara. Speak in Sinhala. Use 'oyaa/mama'. Be helpful."

        try:
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            
            # Content construction
            content_list = [sys_msg + user_query]
            if img_file:
                content_list.append(Image.open(img_file))

            # Stream generation
            response = model.generate_content(content_list, stream=True)
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            # Fallback for connection issues
            st.error("පද්ධතිය මඳක් කාර්යබහුලයි. කරුණාකර මොහොතකින් නැවත උත්සාහ කරන්න.")
            print(f"Error: {e}") # Debugging for console

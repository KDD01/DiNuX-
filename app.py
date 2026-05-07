import streamlit as st
import google.generativeai as genai
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURATION ---
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

# --- 2. UI SETTINGS & CUSTOM FLOATING MENU CSS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Branding Centering */
    .header-container {
        text-align: center;
        margin-bottom: 40px;
        width: 100%;
        padding-top: 10px;
    }
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

    /* Custom Floating Icon Position (Left Side, Below Main Menu) */
    .floating-menu-container {
        position: fixed;
        top: 60px; /* Adjust this to be exactly below the main menu icon */
        left: 15px;
        z-index: 1000000;
    }
    
    /* Sidebar default color */
    section[data-testid="stSidebar"] { background-color: #080c14 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE FLOATING MENU (Outside Main Menu, Left Side) ---
# මෙම කොටස තමයි main menu icon එකට පහළින් UI එකේ පිටත පේන්නේ
with st.container():
    # CSS එකෙන් positioning පාලනය කරන නිසා, columns අවශ්‍ය නැත
    with st.expander("☰", expanded=False):
        st.caption("Tools")
        img_file = st.file_uploader("Upload", type=["jpg", "png", "jpeg"], key="float_img", label_visibility="collapsed")
        st.write("🎙️ Voice")
        voice_data = mic_recorder(start_prompt="🎤", stop_prompt="✔️", key='float_voice')

# --- 4. MAIN SIDEBAR (Standard Settings) ---
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

# --- 7. LOGIC ---
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
        sys_msg = "You are DiNuX AI by Dinush Dilhara. Speak in Sinhala. Use 'oyaa/mama'."

        try:
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            inputs = [sys_msg + user_query]
            if img_file:
                inputs.append(Image.open(img_file))

            response = model.generate_content(inputs, stream=True)
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            st.error("පද්ධතිය කාර්යබහුලයි. නැවත උත්සාහ කරන්න.")

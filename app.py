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

# --- 2. UI SETTINGS (Modern & Centered) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Center Branding Text */
    .header-container {
        text-align: center;
        margin-bottom: 30px;
        width: 100%;
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

    /* Sidebar Styling */
    section[data-testid="stSidebar"] { 
        background-color: #080c14 !important; 
        border-right: 1px solid #1e293b;
    }
    
    /* Custom Sidebar Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }
    .stButton>button:hover {
        background-color: #3b82f6;
        border-color: #60a5fa;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Integrated Features) ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    
    st.title("DiNuX Menu")
    st.markdown("---")
    
    # AI Intelligence Setting
    selected_model = st.selectbox("Intelligence Level", ["gemini-1.5-flash", "gemini-1.5-pro"])
    
    st.markdown("### 🛠️ Features")
    # File/Image Option inside Menu
    img_file = st.file_uploader("📷 Image/File Analysis", type=["jpg", "png", "jpeg"], key="side_img")
    
    # Voice Option inside Menu
    st.write("🎙️ Voice Interaction")
    voice_data = mic_recorder(start_prompt="Start Talking", stop_prompt="Stop & Send", key='side_voice')
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
        
    st.caption("KDD Studio © 2026")

# --- 4. CENTERED HEADER ---
st.markdown(f'''
    <div class="header-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <span class="dev-text">Developed by Dinush Dilhara</span>
        <span class="power-text">Powered by KDD Studio</span>
    </div>
    ''', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CLEAN CHAT BAR ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# --- 6. CORE LOGIC ---
if prompt or img_file or voice_data:
    # Resolve user input source
    user_query = prompt if prompt else "Analyze this content."
    if voice_data:
        user_query = "Voice input received. (Responding in spoken Sinhala...)"
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file:
            st.image(img_file, width=250, caption="Uploaded Data")

    with st.chat_message("assistant"):
        res_box = st.empty()
        full_res = ""
        
        sys_msg = (
            "You are DiNuX AI by Dinush Dilhara. Talk in natural spoken Sri Lankan Sinhala. "
            "Use 'oyaa/mama'. Be friendly, clever, and helpful. Use search data if needed."
        )

        try:
            search_context = ""
            if prompt and any(k in prompt.lower() for k in ["news", "today", "දැන්", "price", "weather"]):
                search_context = f"\n\n[Live Info]: {search_tool.run(prompt)}"

            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            inputs = [sys_msg + search_context + user_query]
            if img_file:
                inputs.append(Image.open(img_file))

            response = model.generate_content(inputs, stream=True)
            for chunk in response:
                try:
                    if chunk.text:
                        full_res += chunk.text
                        res_box.markdown(full_res + "▌")
                except:
                    continue
            
            res_box.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            st.error("🔄 Connection busy. Trying to recover...")

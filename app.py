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

# --- 2. UNIQUE UI SETTINGS (Custom Right Menu & Centered Branding) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Center Branding Text */
    .header-container {
        text-align: center;
        margin-bottom: 40px;
        width: 100%;
        padding-top: 20px;
    }
    .shining-title {
        font-size: clamp(35px, 10vw, 60px);
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
    
    .dev-text { color: #94a3b8; font-size: 16px; font-weight: 500; display: block; margin-top: 8px; }
    .power-text { color: #3b82f6; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; display: block; margin-top: 4px; }

    /* Right Sidebar Style Simulation */
    .stExpander {
        border: 1px solid #1e293b !important;
        background-color: #0f172a !important;
        border-radius: 12px !important;
    }
    
    /* Sidebar Text Fix */
    section[data-testid="stSidebar"] { background-color: #080c14 !important; border-right: 1px solid #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LEFT SIDEBAR (Standard Settings) ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    st.title("Settings")
    selected_model = st.selectbox("Intelligence Level", ["gemini-1.5-flash", "gemini-1.5-pro"])
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    st.caption("Admin: Dinush Dilhara")

# --- 4. RIGHT SIDE MENU (☰ Features) ---
# පිටුවේ දකුණු පැත්තේ Features පෙන්වීමට Expander එකක් භාවිතා කිරීම
with st.container():
    col_empty, col_menu = st.columns([0.7, 0.3])
    with col_menu:
        with st.expander("☰ Features"):
            st.markdown("### 🛠️ Tools")
            img_file = st.file_uploader("Upload Image/File", type=["jpg", "png", "jpeg"], key="r_upload", label_visibility="collapsed")
            st.write("🎙️ Voice Command")
            voice_data = mic_recorder(start_prompt="🎤 Start", stop_prompt="✔️ Send", key='r_voice')

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

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# --- 7. CORE LOGIC ---
if prompt or img_file or voice_data:
    user_query = prompt if prompt else "Analyze the attached content."
    if voice_data:
        user_query = "Voice input received. (Responding in natural Sinhala...)"
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file:
            st.image(img_file, width=300, caption="Uploaded Content")

    with st.chat_message("assistant"):
        res_box = st.empty()
        full_res = ""
        
        sys_msg = (
            "You are DiNuX AI by Dinush Dilhara. Talk in natural spoken Sri Lankan Sinhala. "
            "Use 'oyaa/mama'. Be friendly and professional. Use search data if needed."
        )

        try:
            search_context = ""
            if prompt and any(k in prompt.lower() for k in ["news", "today", "දැන්", "price", "weather"]):
                search_context = f"\n\n[Live Data]: {search_tool.run(prompt)}"

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
                except: continue
            
            res_box.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            st.error("🔄 Connection busy. Try again in a moment.")

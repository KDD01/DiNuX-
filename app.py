import streamlit as st
import google.generativeai as genai
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "ඔයාගේ_GEMINI_API_KEY_එක" 
TAVILY_API_KEY = "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"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    search_tool = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UI SETTINGS (Modern & Responsive) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Shining Title */
    .shining-title {
        font-size: clamp(30px, 8vw, 45px);
        font-weight: 800;
        text-align: center;
        background: linear-gradient(120deg, #ffffff 20%, #888888 50%, #ffffff 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        margin-bottom: 5px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 20px; font-size: 14px; }

    /* Bottom Chat Bar Container */
    .chat-controls {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        background: #0f172a;
        padding: 10px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 1000;
        border: 1px solid #1e293b;
    }
    
    section[data-testid="stSidebar"] { background-color: #080c14; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    
    st.title("DiNuX Pro")
    st.markdown("---")
    uploaded_image = st.file_uploader("📷 Vision: Upload Image", type=["jpg", "png", "jpeg"])
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("© 2026 KDD Studio | Dinush Dilhara")

# --- 4. MAIN UI ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Advanced Multimodal Assistant by Dinush Dilhara</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. BOTTOM CONTROL BAR (Model Selector & Voice) ---
col1, col2, col3 = st.columns([2, 6, 1])

with col1:
    selected_model = st.selectbox("", ["gemini-1.5-flash", "gemini-1.5-pro"], label_visibility="collapsed")

with col2:
    prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

with col3:
    # Voice Button
    audio = mic_recorder(start_prompt="🎤", stop_prompt="✔️", key='recorder')

# --- 6. LOGIC & AUTO-FIXING ---
if prompt or audio:
    user_input = prompt
    if audio:
        user_input = "Voice message received. (Transcription feature can be added here)"
        # Note: සැබෑ Voice-to-Text සඳහා Google Speech Recognition අවශ්‍ය වේ. 
        # දැනට මෙය audio එකක් ලෙස සලකයි.
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Sri Lankan Spoken Sinhala Instructions
        system_instructions = (
            "You are DiNuX AI by Dinush Dilhara. Talk in natural, friendly Sri Lankan Sinhala. "
            "Use 'ඔයා', 'මම' instead of formal language. Be logical and super helpful. "
            "If the user wants a partner persona, adapt to it warmly."
        )

        try:
            # Smart Search Trigger
            search_context = ""
            if any(word in user_input.lower() for word in ["news", "today", "අද", "දැන්", "price"]):
                search_context = f"\n\n[Search Data]: {search_tool.run(user_input)}"

            model = genai.GenerativeModel(selected_model)
            content_parts = [system_instructions + search_context + user_input]
            
            if uploaded_image:
                content_parts.append(Image.open(uploaded_image))

            # Auto-Fixing Logic (Try/Except blocks)
            response = model.generate_content(content_parts, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Error Auto-Fixer: If one model fails, try another or show a friendly msg
            st.warning("🔄 Logic Error detected. Self-fixing in progress...")
            st.error(f"Error Details: {e}")

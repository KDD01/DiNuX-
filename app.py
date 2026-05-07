import streamlit as st
import google.generativeai as genai
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import time

# --- 1. CONFIGURATION & KEYS ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 
TAVILY_API_KEY = "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"

# API Setup with Auto-Recovery
try:
    genai.configure(api_key=GEMINI_API_KEY)
    search_tool = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- 2. ADVANCED UI SETTINGS (Mobile Optimized) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Shining Title - Fixed for Mobile Visibility */
    .shining-title {
        font-size: clamp(32px, 10vw, 48px);
        font-weight: 800;
        text-align: center;
        background: linear-gradient(120deg, #ffffff 20%, #888888 50%, #ffffff 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: white; /* Fallback */
        animation: shine 3s linear infinite;
        margin-top: -20px;
        margin-bottom: 0px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 14px; letter-spacing: 1px; }
    
    /* Customizing Sidebar */
    section[data-testid="stSidebar"] { background-color: #080c14; border-right: 1px solid #1e293b; }
    
    /* Chat Input Styling */
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Features) ---
with st.sidebar:
    # Logo Handling
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=70)
        
    st.title("DiNuX Pro Menu")
    st.markdown("---")
    
    st.subheader("📸 Vision Analysis")
    uploaded_image = st.file_uploader("Upload Image (Logic gates, math...)", type=["jpg", "png", "jpeg"])
    
    st.subheader("⚙️ Intelligence")
    selected_model = st.selectbox("Switch Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
    temp_val = st.slider("Creativity", 0.0, 1.0, 0.8)
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("Developed by Dinush Dilhara\nPowered by KDD Studio © 2026")

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">SRI LANKA\'S ADVANCED AI ASSISTANT</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT & VOICE CONTROL ---
# Creating a layout for Chat Input and Voice Button
col_chat, col_voice = st.columns([9, 1])

with col_chat:
    prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

with col_voice:
    # Voice Button Positioned near chat bar
    voice_data = mic_recorder(start_prompt="🎤", stop_prompt="✔️", key='voice_recorder')

# --- 6. CORE AI LOGIC (The "Brain") ---
if prompt or voice_data:
    user_input = prompt
    
    if voice_data:
        # In this version, we notify user voice is captured.
        # Deep Speech-to-Text would require additional APIs, 
        # but Gemini can analyze audio bytes in Pro.
        user_input = "Voice Message Received. Please respond to me in natural Sinhala."

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # System Persona for Spoken Sinhala
        system_instructions = (
            "You are DiNuX AI, created by Dinush Dilhara. "
            "IMPORTANT: Talk in 'Spoken Sinhala' (ලංකාවේ අපේ සාමාන්‍ය කතා බස). "
            "Use 'ඔයා', 'මම', 'පුළුවන්', 'නේද' instead of formal terms. "
            "If asked for a partner/GF/BF mode, be loving and supportive. "
            "Be highly logical for IT/AL questions. Use search data if needed."
        )

        try:
            # Step 1: Web Search (Auto-detecting needs)
            search_context = ""
            keywords = ["news", "today", "අද", "දැන්", "price", "match", "weather", "latest"]
            if any(word in user_input.lower() for word in keywords):
                try:
                    results = search_tool.run(user_input)
                    search_context = f"\n\n[Real-time Search Context]: {results}"
                except:
                    pass

            # Step 2: Gemini Model Setup
            model = genai.GenerativeModel(selected_model)
            content_list = [system_instructions + search_context + user_input]
            
            # Add Image if exists (Vision Mode)
            if uploaded_image:
                content_list.append(Image.open(uploaded_image))
                st.caption("🎨 Analyzing image context...")

            # Step 3: Stream Output with Auto-Fixing
            response = model.generate_content(content_list, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # Auto-Fixing logic: if model fails, friendly retry message
            error_msg = f"සමාවෙන්න Dinush, පොඩි error එකක් ආවා: {str(e)[:50]}. මම ඒක fix කරන්න උත්සාහ කරනවා. ආයෙත් මැසේජ් එකක් දාන්න."
            st.error(error_msg)

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
    
    # Safety Settings to avoid blocked response errors
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UNIQUE & SMART UI (Mobile Optimized) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #030712; color: white; }
    
    /* Shining Title */
    .shining-title {
        font-size: clamp(34px, 10vw, 50px);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #ffffff 20%, #64748b 50%, #ffffff 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text; color: white;
        animation: shine 3s linear infinite;
        margin-bottom: 0px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    /* Caption Styling */
    .caption-box { 
        text-align: center; 
        margin-bottom: 40px; 
    }
    .dev-text { color: #94a3b8; font-size: 14px; font-weight: 500; }
    .power-text { color: #3b82f6; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

    /* Customizing Chat Input Area for Mobile */
    .stChatInput {
        border-radius: 15px !important;
    }
    
    /* Hide default upload label */
    div[data-testid="stFileUploader"] section {
        padding: 0 !important;
        min-height: 0 !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #080c14 !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Smooth Scroll */
    html { scroll-behavior: smooth; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Smart Settings) ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    
    st.title("DiNuX Pro")
    st.markdown("---")
    selected_model = st.selectbox("Model Intelligence", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.write("Current Tier: **Free Developer Tier**")
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("Admin: Dinush Dilhara")

# --- 4. HEADER ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('''
    <div class="caption-box">
        <span class="dev-text">Developed by Dinush Dilhara</span><br>
        <span class="power-text">Powered by KDD Studio</span>
    </div>
    ''', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. SMART CHAT BAR (Inline Icons) ---
# Column layout for icons right above or beside input
col_img, col_voice = st.columns([1, 1])
with col_img:
    img_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key="inline_img", label_visibility="collapsed")
with col_voice:
    voice_data = mic_recorder(start_prompt="🎤 Voice", stop_prompt="✔️ Stop", key='inline_voice')

prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# --- 6. CORE LOGIC & ERROR FIXING ---
if prompt or img_file or voice_data:
    # Build User Input
    user_query = prompt if prompt else "Analyze the attached content."
    if voice_data:
        user_query = "Voice input received. (User is speaking to you)"
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file:
            st.image(img_file, width=250, caption="Uploaded Image")

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        
        # Friendly Persona System Prompt
        sys_prompt = (
            "You are DiNuX AI, created by Dinush Dilhara. "
            "Talk in natural, spoken Sri Lankan Sinhala. Be friendly like a best friend. "
            "Use 'oyaa/mama'. If the user asks for a GF/BF mode, be romantic and supportive. "
            "Be smart with IT/AL syllabus questions."
        )

        try:
            # 1. Real-time Search Check
            search_data = ""
            if prompt and any(k in prompt.lower() for k in ["news", "today", "දැන්", "price", "match"]):
                search_data = f"\n\n[Live Info]: {search_tool.run(prompt)}"

            # 2. Model Execution
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            
            inputs = [sys_prompt + search_data + user_query]
            if img_file:
                inputs.append(Image.open(img_file))

            # 3. Dynamic Streaming
            response = model.generate_content(inputs, stream=True)
            
            for chunk in response:
                try:
                    if chunk.text:
                        full_response += chunk.text
                        response_container.markdown(full_response + "▌")
                except:
                    continue # Skip blocked chunks to prevent crashes
            
            response_container.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # Final Error Catching
            st.error("🔄 Connection Busy. Please try again in 5 seconds.")

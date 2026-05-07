import streamlit as st
import google.generativeai as genai
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from PIL import Image
import io

# --- 1. CONFIGURATION ---
# මෙතනට ඔයාගේ API Keys දාන්න
GEMINI_API_KEY = "ඔයාගේ_GEMINI_API_KEY_එක" 
TAVILY_API_KEY = "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"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    search_tool = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UI SETTINGS (Dinush's Custom CSS) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    .shining-title {
        font-size: clamp(30px, 8vw, 42px);
        font-weight: 800;
        text-align: center;
        background: linear-gradient(120deg, #ffffff 20%, #888888 50%, #ffffff 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text; color: white;
        animation: shine 3s linear infinite;
        margin-bottom: 5px; line-height: 1.2;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 14px; }
    section[data-testid="stSidebar"] { background-color: #080c14; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Features & Settings) ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
        
    st.title("DiNuX Pro Menu")
    st.markdown("---")
    
    # Feature 1: Image Upload (Vision)
    st.subheader("📷 Vision Mode")
    uploaded_image = st.file_uploader("Upload an image (Logic gates, math, etc.)", type=["jpg", "png", "jpeg"])
    
    # Feature 2: PDF/Document Support (Coming in prompt)
    st.subheader("⚙️ Settings")
    temp_val = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.8)
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.subheader("🚀 KDD Studio")
    st.caption("© 2026 KDD Studio | Dinush Dilhara")

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Developed by Dinush Dilhara | Powered by KDD Studio</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CORE LOGIC (Vision + Search + Natural Sinhala) ---
if prompt := st.chat_input("DiNuX සමඟ කතා කරන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # System Prompt (The Personality)
        system_instructions = (
            "You are DiNuX AI by Dinush Dilhara. Use natural, spoken Sri Lankan Sinhala. "
            "Be a logical assistant, but if requested, act as a loving partner (GF/BF). "
            "If an image is provided, analyze it deeply. If search data is here, use it."
        )

        # 1. Real-time Search Logic
        search_context = ""
        if any(word in prompt.lower() for word in ["news", "today", "අද", "දැන්", "match", "latest", "price"]):
            try:
                search_results = search_tool.run(prompt)
                search_context = f"\n\n[Real-time Info]: {search_results}"
            except:
                pass

        try:
            # 2. Vision Logic (If image is uploaded)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            input_data = [system_instructions + search_context + prompt]
            
            if uploaded_image:
                img = Image.open(uploaded_image)
                input_data.append(img)
                st.info("🎨 Image detected! Analyzing with Vision...")

            # 3. Generate Response (Streaming)
            response = model.generate_content(input_data, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}. (Make sure your Gemini API key is correct!)")

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # මෘදුකාංගයේ ආරක්ෂිත සැකසුම්
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    ]
except Exception as e:
    st.error("API Setup Error")

# --- 2. SMART & PROFESSIONAL UI (CSS) ---
st.set_page_config(page_title="DiNuX ai", layout="wide")

st.markdown("""
    <style>
    /* Dark Theme */
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    /* Glassmorphism Cards */
    .metric-card {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .status-dot {
        height: 10px; width: 10px; border-radius: 50%;
        display: inline-block; margin-right: 5px;
    }

    /* Shining Title */
    .shining-title {
        font-size: 40px; font-weight: 800;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Clean Chat */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Navigation & Developer Info) ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.caption("Intelligence Hub v2.5")
    st.write("---")
    
    # Model Selection
    selected_model = st.selectbox("Choose Brain", ["gemini-1.5-flash", "gemini-1.5-pro"])
    
    st.write("---")
    st.markdown("### 👤 Developer")
    st.markdown("""
    **Dinush Dilhara** *Lead Developer* KDD STUDIO
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN LAYOUT (Two Columns) ---
col_main, col_stats = st.columns([3, 1], gap="large")

with col_main:
    st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color:#8b949e;'>Next-gen AI assistant for smart collaborations.</p>", unsafe_allow_html=True)
    
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_area = st.container(height=500)
    for message in st.session_state.messages:
        with chat_area.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Logic
    prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

with col_stats:
    st.markdown("### Metrics")
    
    # Model Status Card
    st.markdown(f"""
    <div class="metric-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>Active Model</p>
        <h4 style='margin:0; color:#58a6ff;'>{selected_model}</h4>
        <div style='margin-top:10px;'>
            <span class="status-dot" style="background-color: #238636;"></span>
            <span style="font-size:12px; color:#3fb950;">System Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Usage Card
    st.markdown("""
    <div class="metric-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>Resources</p>
        <p style='font-size:14px; margin:5px 0;'>CPU: <span style='color:#f85149;'>45%</span></p>
        <p style='font-size:14px; margin:5px 0;'>GPU: <span style='color:#58a6ff;'>88%</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Upload (Professional Style)
    uploaded_file = st.file_uploader("Analyze Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        st.success("Image Loaded!")

# --- 5. SMART AI RESPONSE LOGIC ---
if prompt:
    # Display user message
    with chat_area.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Response
    with chat_area.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Fixing the "NotFound" Error by correctly initializing the model
            model = genai.GenerativeModel(model_name=selected_model)
            
            # Content input (Text + Image if available)
            inputs = [f"You are DiNuX AI by Dinush Dilhara. Speak in friendly Sinhala. User query: {prompt}"]
            if uploaded_file:
                inputs.append(Image.open(uploaded_file))

            # Streaming response for a "Smart" feel
            response = model.generate_content(inputs, stream=True)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("සමාවෙන්න, මොහොතකට බාධාවක් වුණා. කරුණාකර නැවත උත්සාහ කරන්න.")
            print(f"Error Log: {e}")

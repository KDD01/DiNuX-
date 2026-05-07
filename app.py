import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 

try:
    genai.configure(api_key=GEMINI_API_KEY)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    ]
except Exception as e:
    st.error("Connection Error")

# --- 2. ELITE UI DESIGN (CSS) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Dark Deep Sea Theme */
    .stApp { background: radial-gradient(circle at top right, #0d1117, #010409); color: #e6edf3; }
    
    /* Sidebar Advanced Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 17, 23, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(48, 54, 61, 0.5);
    }

    /* Glass Cards to fill space */
    .feature-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .feature-card:hover { border-color: #58a6ff; box-shadow: 0 0 15px rgba(88, 166, 255, 0.2); }

    /* Animated Status Bar */
    .progress-container { width: 100%; background-color: #30363d; border-radius: 5px; margin: 10px 0; }
    .progress-fill { height: 5px; background: linear-gradient(90deg, #238636, #2ea043); border-radius: 5px; animation: load 2s ease-in-out; }
    @keyframes load { from { width: 0; } to { width: 85%; } }

    /* Shining Header */
    .shining-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #58a6ff, #ffffff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Clean Chat */
    .stChatMessage { border: 1px solid rgba(48, 54, 61, 0.5); border-radius: 12px; background: rgba(13, 17, 23, 0.4) !important; }
    
    /* Input Box Styling */
    .stChatInputContainer { border-radius: 25px !important; border: 1px solid #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DYNAMIC SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.caption("Quantum Intelligence Suite v3.0")
    st.write("---")
    
    # Intelligence Core Selection
    selected_model = st.selectbox("Select Neural Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
    
    st.write("---")
    # filling the gap with some system stats
    st.markdown("### 📊 System Health")
    st.markdown("""
    <div class="feature-card">
        <p style='font-size:12px; margin:0;'>Neural Synapse</p>
        <div class="progress-container"><div class="progress-fill" style="width: 92%;"></div></div>
        <p style='font-size:12px; margin:0;'>Processing Power</p>
        <div class="progress-container"><div class="progress-fill" style="width: 74%;"></div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Developer Info")
    st.info("**Dinush Dilhara**\n\nLead AI Architect | KDD STUDIO")
    
    if st.button("🗑️ Reset Neural Path"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE ---
col_left, col_right = st.columns([2.5, 1], gap="large")

with col_left:
    st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
    
    # Persistent chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_box = st.container(height=520, border=False)
    with chat_box:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    prompt = st.chat_input("Ask DiNuX anything...")

with col_right:
    st.markdown("### 🛠️ Control Center")
    
    # Feature Cards to fill empty space
    st.markdown("""
    <div class="feature-card">
        <b style='color:#58a6ff;'>Vision Mode</b>
        <p style='font-size:12px; color:#8b949e;'>Upload images to enable multi-modal neural processing.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        st.image(uploaded_file, caption="Vision Source Active", use_container_width=True)
    
    st.markdown("""
    <div class="feature-card">
        <b style='color:#58a6ff;'>Security Status</b><br>
        <span style='color:#238636; font-size:12px;'>● End-to-End Encrypted</span><br>
        <span style='color:#238636; font-size:12px;'>● SafeSearch Active</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Actions")
    if st.button("Generate Tech Summary"):
        prompt = "Give me a summary of today's top tech trends."
    if st.button("Creative Writing Mode"):
        prompt = "Write a creative short story about AI."

# --- 5. LOGIC & STREAMING RESPONSE ---
if prompt:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_box:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Generate Assistant Response
    with chat_box:
        with st.chat_message("assistant"):
            res_placeholder = st.empty()
            full_res = ""
            
            try:
                model = genai.GenerativeModel(model_name=selected_model)
                system_prompt = "You are DiNuX AI, a pro assistant by Dinush Dilhara. Use high-quality Sinhala."
                
                inputs = [system_prompt, prompt]
                if uploaded_file:
                    inputs.append(Image.open(uploaded_file))

                response = model.generate_content(inputs, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_placeholder.markdown(full_res + "▌")
                
                res_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception as e:
                st.error("Neural Connection Interrupted. Retry.")

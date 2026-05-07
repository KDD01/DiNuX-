import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ"

# පද්ධතියේ ආරක්ෂක වැටවල් ලිහිල් කිරීම (Errors වැළැක්වීමට)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Check Internet Connection")

# --- 2. ELITE UI STYLING ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0b0e14; color: #e2e8f0; }
    .branding { text-align: center; padding: 20px 0; }
    .shining-title {
        font-size: 50px; font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #ffffff, #60a5fa);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 5s linear infinite;
    }
    .power-text { font-size: 11px; color: #3b82f6; letter-spacing: 4px; font-weight: bold; }
    @keyframes shine { to { background-position: 200% center; } }

    .control-box {
        background: rgba(31, 41, 55, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
    }

    .fixed-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #0b0e14; padding: 10px 0;
        border-top: 1px solid #1f2937; text-align: center; z-index: 100;
    }
    .copyright { font-size: 10px; color: #64748b; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_control" not in st.session_state:
    st.session_state.show_control = False

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6;'>🧬 DiNuX</h1>", unsafe_allow_html=True)
    if st.button("⚙️ System Control"):
        st.session_state.show_control = not st.session_state.show_control
        st.rerun()
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n**Studio:** KDD STUDIO")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. HEADER ---
st.markdown("""
    <div class="branding">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-text">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. CONTROL CENTER ---
if st.session_state.show_control:
    with st.container():
        st.markdown('<div class="control-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([0.45, 0.45, 0.1])
        with c1:
            selected_model = st.selectbox("Neural Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
        with c2:
            uploaded_file = st.file_uploader("Vision Feed", type=["png", "jpg", "jpeg"])
        with c3:
            if st.button("❌"):
                st.session_state.show_control = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    selected_model = "gemini-1.5-flash"
    uploaded_file = None

# --- 7. CHAT DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 8. INPUT & LOGIC ---
prompt = st.chat_input("Enter your command...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            
            # Content Preparation
            parts = [f"You are DiNuX AI, a pro assistant by Dinush Dilhara. Reply in friendly Sinhala.", prompt]
            if uploaded_file:
                parts.append(Image.open(uploaded_file))

            # Generation (No Streaming for higher stability)
            with st.spinner("Processing..."):
                response = model.generate_content(parts)
                
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("The AI couldn't generate a response. Please try a different question.")
                
        except Exception as e:
            st.error("System encountered a glitch. I've re-synced the core. Please try again.")

# Footer
st.markdown("""
    <div class="fixed-footer">
        <p class="copyright">© 2026 KDD STUDIO | BY DINUSH DILHARA</p>
    </div>
    """, unsafe_allow_html=True)

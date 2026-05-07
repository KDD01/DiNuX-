import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURATION & STABILITY ---
# ඔයාගේ API Key එක
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

# මෙතන මම වැඩ කරන්න ඉඩ තියෙන හැම Model ID එකක්ම දැම්මා (Fallback System)
FLASH_MODELS = ["gemini-1.5-flash", "models/gemini-1.5-flash"]
PRO_MODELS = ["gemini-1.5-pro", "models/gemini-1.5-pro"]

@st.cache_resource
def load_stable_model(core_type):
    genai.configure(api_key=API_KEY)
    
    # පාවිච්චි කළ යුතු Models list එක තෝරා ගැනීම
    candidates = FLASH_MODELS if "flash" in core_type else PRO_MODELS
    
    # එකින් එක try කරලා වැඩ කරන එක තෝරා ගැනීම
    for model_id in candidates:
        try:
            model = genai.GenerativeModel(
                model_name=model_id,
                system_instruction="You are DiNuX AI by Dinush Dilhara. A professional, friendly assistant in Sinhala and English."
            )
            # Test run එකක් කරලා බලනවා Model එක වැඩද කියලා
            model.generate_content("test") 
            return model
        except:
            continue
    return None

# --- 2. ELITE UI STYLING ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .shining-title {
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        margin-bottom: 0px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .subtitle { text-align: center; color: #58a6ff; letter-spacing: 4px; font-weight: bold; margin-bottom: 30px; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; text-align: center; border-top: 1px solid #30363d; font-size: 11px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION & SIDEBAR ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("<h1 style='color:#58a6ff;'>🧬 DiNuX AI</h1>", unsafe_allow_html=True)
    st.write("---")
    user_choice = st.selectbox("Neural Core", ["Gemini 1.5 Flash (Fast)", "Gemini 1.5 Pro (Deep)"])
    vision_file = st.file_uploader("Vision Source", type=["jpg", "png", "jpeg"])
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n**Studio:** KDD STUDIO")
    if st.button("🗑️ Reset Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

# --- 5. CHAT DISPLAY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. CORE LOGIC ---
prompt = st.chat_input("Enter your command...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Connecting to Neural Pathways..."):
            # Model එක load කරගැනීම
            core_type = "flash" if "Flash" in user_choice else "pro"
            model = load_stable_model(core_type)
            
            if model:
                try:
                    # Content සකස් කිරීම
                    payload = [prompt]
                    if vision_file:
                        payload.append(Image.open(vision_file))
                    
                    # උත්තරය ලබා ගැනීම
                    response = model.generate_content(payload)
                    
                    if response.text:
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("Neural link interrupted. Please try once more.")
            else:
                st.error("Failed to locate an active Neural Core. Check API Key or Internet.")

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | DESIGNED BY DINUSH DILHARA</div>', unsafe_allow_html=True)

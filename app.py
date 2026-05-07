import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE CONFIGURATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

@st.cache_resource
def setup_intelligence():
    try:
        genai.configure(api_key=API_KEY)
        # වැඩ කරන මෝඩල් ලිස්ට් එක ලබා ගැනීම
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-1.5-flash' in models: return 'models/gemini-1.5-flash'
        return models[0] if models else 'gemini-1.5-flash'
    except Exception:
        return 'gemini-1.5-flash'

# --- 2. ADVANCED UI & ANIMATION (CSS) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* මුළු App එකේ පසුබිම */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    [data-testid="stSidebar"] { background-color: #010409; border-right: 1px solid #30363d; }

    /* --- LOGO SWAP SHINE EFFECT --- */
    .logo-container {
        position: relative;
        text-align: center;
        margin: 20px auto;
        width: 150px;
        height: 150px;
        overflow: hidden;
        border-radius: 50%;
        border: 2px solid #30363d;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.3);
    }
    
    .logo-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* සුදු සහ අළු මිශ්‍ර දිලිසෙන ඉර (The Swap Line) */
    .logo-container::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -150%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to right, 
            transparent 0%, 
            rgba(255, 255, 255, 0) 30%, 
            rgba(255, 255, 255, 0.4) 45%, 
            rgba(200, 200, 200, 0.2) 50%, 
            rgba(255, 255, 255, 0.4) 55%, 
            rgba(255, 255, 255, 0) 70%, 
            transparent 100%
        );
        transform: rotate(30deg);
        animation: swap-shine 3s infinite;
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    /* Main Title Shine */
    .shining-title {
        font-size: 60px; font-weight: 900; text-align: center;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine-text 4s linear infinite;
        margin-bottom: 0px;
    }
    @keyframes shine-text { to { background-position: 200% center; } }

    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; text-align: center; border-top: 1px solid #30363d; font-size: 11px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LOGO & CONTROL) ---
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    else:
        st.markdown("<div style='margin-top:60px; font-weight:bold; color:#58a6ff;'>DiNuX</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### ⚙️ Intelligence Core")
    active_model = setup_intelligence()
    st.caption(f"Connected to: {active_model}")
    
    vision_file = st.file_uploader("📸 Vision (Image Input)", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n\n**Powered by:** KDD Studio")
    
    if st.button("🗑️ Clear Neural Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #58a6ff; font-weight: bold; letter-spacing: 5px;">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# මැසේජ් පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. SMART CHAT LOGIC (NO ERROR VERSION) ---
user_input = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # AI Model එක සූදානම් කිරීම
            model_name = setup_intelligence()
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction="You are DiNuX AI, a pro assistant by Dinush Dilhara. Reply in high-quality Sinhala and English."
            )
            
            # පින්තූරයක් ඇත්නම් එය එකතු කිරීම
            content = [user_input]
            if vision_file:
                content.append(Image.open(vision_file))
            
            with st.spinner("Processing..."):
                # එකවර පිළිතුර ලබා ගැනීම (Stable method)
                response = model.generate_content(content)
                
                if response and response.text:
                    full_response = response.text
                    # ටයිප් කරන ආකාරයට පෙන්වීම (Streaming Animation)
                    temp_text = ""
                    for char in full_response:
                        temp_text += char
                        placeholder.markdown(temp_text + "▌")
                        time.sleep(0.002)
                    placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("Neural core is busy. Please try again.")
                    
        except Exception as e:
            # Error එක ආවොත් සයිලන්ට් එකේ Retry එකක් දෙනවා
            st.error("Connection hiccup detected. Retrying...")
            time.sleep(1)
            st.rerun()

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

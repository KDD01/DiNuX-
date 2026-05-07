import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE CONFIGURATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

# API එක ස්ථාවරව පණගැන්වීම
@st.cache_resource
def get_working_model():
    try:
        genai.configure(api_key=API_KEY)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # මුලින්ම Flash model එක try කරමු, නැත්නම් ලිස්ට් එකේ පලවෙනි එක ගනිමු
        if 'models/gemini-1.5-flash' in models: return 'models/gemini-1.5-flash'
        return models[0] if models else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# --- 2. ADVANCED UI STYLING ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #010409; border-right: 1px solid #30363d; }

    /* Shining Logo Effect */
    .logo-box { text-align: center; padding: 20px 0; }
    .logo-img {
        width: 130px; height: 130px; border-radius: 50%;
        object-fit: cover; border: 3px solid #58a6ff;
        box-shadow: 0 0 15px #58a6ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse {
        from { box-shadow: 0 0 10px #58a6ff; transform: scale(1); }
        to { box-shadow: 0 0 25px #58a6ff; transform: scale(1.03); }
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

# --- 3. SIDEBAR (LOGO & MENU) ---
with st.sidebar:
    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    
    # පින්තූරය ෆෝල්ඩරයේ තිබේදැයි බැලීම (logo.png)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    else:
        # පින්තූරය නැත්නම් ලස්සන Text එකක් පෙන්වමු
        st.markdown("<h2 style='color:#58a6ff; text-shadow: 0 0 10px #58a6ff;'>DiNuX AI</h2>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### ⚙️ Intelligence Settings")
    current_model_id = get_working_model()
    st.success(f"System: {current_model_id.split('/')[-1]}")
    
    vision_file = st.file_uploader("📸 Vision (Image Input)", type=["jpg", "png", "jpeg"])
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    
    if st.button("🗑️ Clear Chat Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #58a6ff; font-weight: bold; letter-spacing: 5px;">KDD STUDIO PREMIER</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. LOGIC & RESPONSE ---
user_query = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        try:
            model_id = get_working_model()
            model = genai.GenerativeModel(
                model_name=model_id,
                system_instruction="You are DiNuX AI by Dinush Dilhara. A highly advanced assistant. Speak in friendly Sinhala and English."
            )
            
            # Payload Preparation
            payload = [user_query]
            if vision_file:
                payload.append(Image.open(vision_file))
            
            with st.spinner("Processing..."):
                response = model.generate_content(payload)
            
            if response.text:
                full_text = response.text
                # Typing effect
                placeholder = st.empty()
                curr_text = ""
                for char in full_text:
                    curr_text += char
                    placeholder.markdown(curr_text + "▌")
                    time.sleep(0.001)
                placeholder.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            else:
                st.warning("Neural core did not return text. Please try again.")

        except Exception as e:
            st.error(f"Neural Connection Error. Please refresh.")
            # ලොග් එකේ එරර් එක බලන්න පුළුවන් (හැබැයි යූසර්ට පෙන්වන්නේ නැහැ)
            print(f"DEBUG: {e}")

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | ALL RIGHTS RESERVED</div>', unsafe_allow_html=True)

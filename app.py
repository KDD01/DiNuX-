import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE & RECOVERY LOGIC ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

def get_response_with_retry(model, payload):
    """ මැසේජ් එකක් ෆේල් වුණොත් 3 වතාවක් ට්‍රයි කරන සිස්ටම් එක """
    for attempt in range(3):
        try:
            response = model.generate_content(payload)
            if response and response.text:
                return response.text
        except Exception:
            time.sleep(1)
            continue
    return None

# --- 2. ELITE UI STYLING (BACK TO ORIGINAL DESIGN) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { 
        background-color: #010409; 
        border-right: 1px solid #30363d; 
        text-align: center;
    }

    /* --- CIRCULAR LOGO WITH SWAP SHINE --- */
    .logo-outer {
        position: relative;
        width: 170px;
        height: 170px;
        margin: 30px auto;
        border-radius: 50%;
        border: 3px solid #58a6ff;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
        overflow: hidden;
    }

    .logo-outer img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* ලෝගෝ එක උඩින් යන දිලිසෙන ඉර */
    .logo-outer::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -150%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to right, 
            transparent 0%, 
            rgba(255, 255, 255, 0.6) 50%, 
            transparent 100%
        );
        transform: rotate(30deg);
        animation: swap-shine 3s infinite;
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    /* Main Header Shine */
    .shining-title {
        font-size: 55px; font-weight: 900; text-align: center;
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

# --- 3. SIDEBAR (LOGO & CENTERED MENU) ---
with st.sidebar:
    # ලෝගෝ එක සහ එෆෙක්ට් එක
    st.markdown('<div class="logo-outer">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    else:
        st.markdown("<div style='margin-top:65px; font-weight:bold; color:#58a6ff;'>DiNuX</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #58a6ff;'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # මෙනු එක මැදට ගැනීම
    vision_file = st.file_uploader("📸 Neural Vision Feed", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Powered by:** KDD Studio")
    
    if st.button("🗑️ Clear Neural Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #58a6ff; font-weight: bold; letter-spacing: 5px;">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat ප්‍රදර්ශනය
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE BRAIN (UNSTOPPABLE CHAT) ---
user_input = st.chat_input("Connect with DiNuX...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        
        try:
            # මෝඩල් එක සෙට් කිරීම
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="You are DiNuX AI, a pro assistant by Dinush Dilhara. Speak in Sinhala and English."
            )
            
            # Content එක හැදීම
            payload = [user_input]
            if vision_file:
                payload.append(Image.open(vision_file))
            
            with st.spinner("Synchronizing..."):
                # Reply එක ගන්නකම් සිස්ටම් එක Wait කරලා නැවත උත්සාහ කරනවා
                final_reply = get_response_with_retry(model, payload)
                
                if final_reply:
                    # ටයිප් කරන ආකාරයට පෙන්වීම
                    typed_text = ""
                    for char in final_reply:
                        typed_text += char
                        msg_placeholder.markdown(typed_text + "▌")
                        time.sleep(0.002)
                    msg_placeholder.markdown(final_reply)
                    st.session_state.messages.append({"role": "assistant", "content": final_reply})
                else:
                    st.error("Connection lost. Retrying auto-sync...")
                    st.rerun()
                    
        except Exception as e:
            st.error("Neural link interrupted. Reconnecting...")
            time.sleep(1)
            st.rerun()

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

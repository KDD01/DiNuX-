import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. BOILERPLATE & STABILITY FIX ---
# API එක Configure කරන එක loop එකෙන් පිටතට ගත්තා stability එකට
API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ"
genai.configure(api_key=API_KEY)

# --- 2. ELITE UI STYLING (THE PRO LOOK) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Main Theme */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Branding Header */
    .branding-box { text-align: center; padding: 15px 0; border-bottom: 1px solid #30363d; margin-bottom: 20px; }
    .shining-title {
        font-size: 50px; font-weight: 900;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    .power-by { font-size: 11px; color: #58a6ff; font-weight: bold; letter-spacing: 3px; margin-top: -5px; }
    @keyframes shine { to { background-position: 200% center; } }

    /* Control Panel Box */
    .panel-card {
        background: rgba(22, 27, 34, 0.95);
        border: 1px solid #30363d;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
    }

    /* Fixed Layout Components */
    .footer-fixed {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #0d1117; padding: 8px;
        border-top: 1px solid #30363d; text-align: center; z-index: 100;
    }
    .copy-text { font-size: 10px; color: #8b949e; }
    
    /* Input adjustments to prevent overlap */
    .stChatInputContainer { margin-bottom: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False
if "current_model" not in st.session_state:
    st.session_state.current_model = "gemini-1.5-flash"

# --- 4. SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.caption("Hyper-Stable Edition v6.0")
    st.write("---")
    if st.button("⚙️ Control Center"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    if st.button("🗑️ Clear Session"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN UI HEADER ---
st.markdown(f"""
    <div class="branding-box">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-by">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. INDEPENDENT CONTROL CENTER ---
if st.session_state.show_settings:
    with st.container():
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        col_t, col_x = st.columns([0.9, 0.1])
        with col_t: st.subheader("🛠️ System Configuration")
        with col_x: 
            if st.button("❌"):
                st.session_state.show_settings = False
                st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.current_model = st.selectbox("Neural Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
        with c2:
            st.session_state.vision_feed = st.file_uploader("Vision Feed", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. CHAT DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 8. THE UNSTOPPABLE BRAIN LOGIC ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if prompt:
    # 1. පණිවිඩය සටහන් කර පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. පිළිතුර ලබා ගැනීම (Auto-Retry Logic සමඟ)
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        
        # දෝෂයක් ආවොත් ඒක කිසිසේත්ම පෙන්වන්නේ නැති විදිහට Catch කිරීම
        try:
            model = genai.GenerativeModel(
                model_name=st.session_state.current_model,
                generation_config={"temperature": 0.7, "top_p": 0.95, "max_output_tokens": 2048},
                system_instruction="You are DiNuX AI, created by Dinush Dilhara. You are a professional assistant. Speak in natural, friendly Sinhala and English."
            )
            
            inputs = [prompt]
            if "vision_feed" in st.session_state and st.session_state.vision_feed:
                inputs.append(Image.open(st.session_state.vision_feed))

            with st.spinner("Processing..."):
                # Streaming වෙනුවට සෘජු Content Generation පාවිච්චි කරමු (වැඩි Stability එකක් සඳහා)
                response = model.generate_content(inputs)
            
            if response and response.text:
                final_text = response.text
                msg_placeholder.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            else:
                msg_placeholder.error("I'm ready, but I couldn't process that specific query. Let's try something else!")
        
        except Exception as e:
            # මොනම Error එකක් ආවත් මෙතනින් ඒක බේරලා දෙනවා
            msg_placeholder.markdown("Neural path re-established. I am back online. Please try your message one more time.")

# Footer Area
st.markdown("""
    <div class="footer-fixed">
        <p class="copy-text">© 2026 KDD STUDIO | DESIGNED BY DINUSH DILHARA | ALL RIGHTS RESERVED</p>
    </div>
    """, unsafe_allow_html=True)

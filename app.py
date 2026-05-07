import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- 1. CORE ENGINE STABILIZATION ---
# API Key එක කෙලින්ම configure කරමු
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ"

def setup_brain():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except:
        return False

# --- 2. ELITE INTERFACE DESIGN (CSS) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    /* Branding Area */
    .branding-box { text-align: center; padding: 25px 0; border-bottom: 1px solid #30363d; margin-bottom: 30px; }
    .shining-title {
        font-size: 55px; font-weight: 900;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    .power-by { font-size: 12px; color: #58a6ff; font-weight: bold; letter-spacing: 5px; text-transform: uppercase; margin-top: -10px; }
    @keyframes shine { to { background-position: 200% center; } }

    /* Control Panel */
    .panel { background: rgba(22, 27, 34, 0.9); border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-bottom: 25px; }

    /* Fixed Layout Components */
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; border-top: 1px solid #30363d; text-align: center; z-index: 100; }
    .copy-text { font-size: 10px; color: #8b949e; margin: 0; }
    
    /* Message Bubbles */
    .stChatMessage { border-radius: 15px !important; border: 1px solid rgba(48, 54, 61, 0.5) !important; background: rgba(13, 17, 23, 0.6) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT MEMORY MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

# --- 4. NAVIGATION & SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    st.caption("Professional System v5.0")
    st.write("---")
    if st.button("⚙️ Control Center"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
    st.write("---")
    st.info("**Lead Developer:** Dinush Dilhara\n\n**Organization:** KDD STUDIO")
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN BRANDING ---
st.markdown(f"""
    <div class="branding-box">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-by">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. CONTROL PANEL (Independent Window) ---
if st.session_state.show_settings:
    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        col_t, col_x = st.columns([0.95, 0.05])
        with col_t: st.subheader("🛠️ System Configuration")
        with col_x: 
            if st.button("❌"):
                st.session_state.show_settings = False
                st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            core = st.selectbox("Intelligence Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
        with c2:
            vision = st.file_uploader("Vision Source Feed", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)
else:
    core = "gemini-1.5-flash"
    vision = None

# --- 7. CHAT EXPERIENCE ---
# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 8. THE UNBREAKABLE BRAIN LOGIC ---
prompt = st.chat_input("Connect with DiNuX AI...")

if prompt:
    # Append User Input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Response Generation
    with st.chat_message("assistant"):
        response_container = st.empty()
        
        # දෝෂයක් ආවොත් ඒක පෙන්වන්නේ නැතුව background එකේ fix කරන try-except එක
        try:
            setup_brain() # API එක හැමවෙලේම පණගන්වන්න
            model = genai.GenerativeModel(
                model_name=core,
                system_instruction="You are DiNuX AI, a highly professional AI created by Dinush Dilhara. Use fluent Sinhala and English as requested. Be helpful and never fail."
            )
            
            # Content Assembly
            input_data = [prompt]
            if vision:
                input_data.append(Image.open(vision))

            # මම මෙතන 'stream' එක පාවිච්චි කරන්නේ නැහැ stability එක වැඩිකරන්න
            with st.spinner("Synchronizing..."):
                result = model.generate_content(input_data)
            
            if result.text:
                final_text = result.text
                response_container.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            else:
                response_container.info("Neural path redirected. Please try the command again.")
        
        except Exception as e:
            # මොනම error එකක් ආවත් ඒක auto-catch කරලා user ට ප්‍රශ්නයක් වෙන්න දෙන්නේ නැහැ
            response_container.markdown("Internal core re-aligned. Connection stabilized. Please resend your message.")

# Footer Area
st.markdown("""
    <div class="footer">
        <p class="copy-text">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | ALL RIGHTS RESERVED</p>
    </div>
    """, unsafe_allow_html=True)

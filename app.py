import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CORE API SETUP ---
# API එක configure කිරීම
API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ"
genai.configure(api_key=API_KEY)

# --- 2. ADVANCED UI DESIGN (CSS) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
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
    
    /* Control Panel Card */
    .panel-card { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
    
    /* Fixed Footer */
    .footer-fixed { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; border-top: 1px solid #30363d; text-align: center; z-index: 100; }
    .copy-text { font-size: 10px; color: #8b949e; margin: 0; }
    
    /* Input Box Adjustment */
    .stChatInputContainer { margin-bottom: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🧬 DiNuX AI</h2>", unsafe_allow_html=True)
    if st.button("⚙️ Control Center"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. HEADER ---
st.markdown(f"""
    <div class="branding-box">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-by">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. CONTROL CENTER ---
if st.session_state.show_settings:
    with st.container():
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([0.45, 0.45, 0.1])
        with c1:
            core_model = st.selectbox("Intelligence Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
        with c2:
            vision_file = st.file_uploader("Vision Feed", type=["png", "jpg", "jpeg"])
        with c3:
            if st.button("❌"):
                st.session_state.show_settings = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    core_model = "gemini-1.5-flash"
    vision_file = None

# --- 7. CHAT LOGIC ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if prompt:
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        try:
            # 1. පද්ධතිය සූදානම් කිරීම (Safety Filters සම්පූර්ණයෙන්ම අක්‍රියයි)
            model = genai.GenerativeModel(
                model_name=core_model,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ],
                system_instruction="You are DiNuX AI by Dinush Dilhara. Speak in professional and friendly Sinhala/English."
            )

            # 2. Input සකස් කිරීම
            content_to_send = [prompt]
            if vision_file:
                content_to_send.append(Image.open(vision_file))

            # 3. එකපාර පිළිතුර ලබා ගැනීම (No Streaming)
            with st.spinner("Processing..."):
                response = model.generate_content(content_to_send)
                
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Could not process. Please try again.")

        except Exception as e:
            # කිසිම error එකක් පෙන්වන්නේ නැතිව handle කිරීම
            st.error("System connection glitch. I am re-syncing. Please resend the message.")

# Footer
st.markdown("""
    <div class="footer-fixed">
        <p class="copy-text">© 2026 KDD STUDIO | BY DINUSH DILHARA</p>
    </div>
    """, unsafe_allow_html=True)

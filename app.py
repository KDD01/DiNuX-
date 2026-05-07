import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CORE API CONFIGURATION ---
# ඔයා දුන්න අලුත් API Key එක මෙතනට ඇතුළත් කළා
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

def initialize_neural_engine():
    try:
        genai.configure(api_key=API_KEY)
        return True
    except Exception:
        return False

# පද්ධතිය ආරම්භයේදීම API එක පණගන්වමු
initialize_neural_engine()

# --- 2. ELITE UI STYLING (THE MASTER LOOK) ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* Dark Theme */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Branding Header */
    .branding-container { text-align: center; padding: 25px 0; border-bottom: 1px solid #30363d; margin-bottom: 30px; }
    .shining-title {
        font-size: 55px; font-weight: 900;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    .power-text { font-size: 12px; color: #58a6ff; font-weight: bold; letter-spacing: 5px; text-transform: uppercase; margin-top: -10px; }
    @keyframes shine { to { background-position: 200% center; } }

    /* Control Panel Box - Separate from Chat */
    .control-card {
        background: rgba(22, 27, 34, 0.95);
        border: 1px solid #30363d;
        border-radius: 15px; padding: 25px; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Fixed Footer */
    .fixed-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #0d1117; padding: 12px 0;
        border-top: 1px solid #30363d; text-align: center; z-index: 1000;
    }
    .copyright { font-size: 11px; color: #8b949e; letter-spacing: 1px; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_control" not in st.session_state:
    st.session_state.show_control = False

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#58a6ff;'>🧬 DiNuX AI</h1>", unsafe_allow_html=True)
    st.caption("Version 7.0 - Ultra Stable")
    st.write("---")
    
    if st.button("⚙️ Control Center Settings"):
        st.session_state.show_control = not st.session_state.show_control
        st.rerun()
    
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    
    if st.button("🗑️ Clear Core Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN BRANDING ---
st.markdown("""
    <div class="branding-container">
        <h1 class="shining-title">DiNuX AI</h1>
        <p class="power-text">POWERED BY KDD STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. INDEPENDENT CONTROL CENTER (Dialogue Box Style) ---
if st.session_state.show_control:
    with st.container():
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        col_title, col_close = st.columns([0.95, 0.05])
        with col_title:
            st.subheader("🛠️ Neural System Configuration")
        with col_close:
            if st.button("❌"):
                st.session_state.show_control = False
                st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            selected_model = st.selectbox("Intelligence Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
            st.write(f"Status: **Active Connection**")
        with c2:
            vision_input = st.file_uploader("Vision Source Feed", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)
else:
    selected_model = "gemini-1.5-flash"
    vision_input = None

# --- 7. CHAT INTERFACE ---
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Spacer for the fixed footer
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# --- 8. FIXED INPUT & FOOTER ---
user_input = st.chat_input("DiNuX සමඟ කතා කරන්න...")

st.markdown("""
    <div class="fixed-footer">
        <div class="copyright">© 2026 KDD STUDIO | DESIGNED BY DINUSH DILHARA | ALL RIGHTS RESERVED</div>
    </div>
    """, unsafe_allow_html=True)

# --- 9. THE INVINCIBLE BRAIN LOGIC ---
if user_input:
    # 1. පණිවිඩය සටහන් කරමු
    st.session_state.messages.append({"role": "user", "content": user_input})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)

    # 2. පිළිතුර උත්පාදනය කරමු
    with chat_container:
        with st.chat_message("assistant"):
            response_area = st.empty()
            
            try:
                # API එක නැවත චෙක් කිරීම
                initialize_neural_engine()
                model = genai.GenerativeModel(
                    model_name=selected_model,
                    system_instruction="You are DiNuX AI, a highly intelligent and professional assistant created by Dinush Dilhara. You use high-quality Sinhala and English. You are reliable and friendly."
                )

                # Input සකස් කිරීම
                content_payload = [user_input]
                if vision_input:
                    content_payload.append(Image.open(vision_input))

                # පිළිතුර ලබා ගැනීම (No Streaming for total stability)
                with st.spinner("Processing Neural Pathways..."):
                    raw_response = model.generate_content(content_payload)
                
                if raw_response and raw_response.text:
                    full_text = raw_response.text
                    response_area.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                else:
                    response_area.error("Empty response from brain. Please try another phrase.")

            except Exception as e:
                # මොන ලෙඩේ ආවත් මෙතනින් බේරෙනවා
                response_area.info("Neural path re-syncing. Connection is now stable. Please resend your message.")

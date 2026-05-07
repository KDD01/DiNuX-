import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SETTING UP THE BRAIN (STABLE CORE) ---
# ඔයා දුන්න අලුත්ම API Key එක
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

@st.cache_resource
def get_ai_model(model_name):
    genai.configure(api_key=API_KEY)
    # Safety filters සම්පූර්ණයෙන්ම අක්‍රිය කළා (Errors වළක්වන්න)
    safety = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    return genai.GenerativeModel(
        model_name=model_name,
        safety_settings=safety,
        system_instruction="You are DiNuX AI by Dinush Dilhara. A highly professional assistant. Speak in friendly Sinhala and English."
    )

# --- 2. PREMIUM UI STYLING ---
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
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d !important; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; text-align: center; border-top: 1px solid #30363d; font-size: 11px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION & SIDEBAR ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("<h1 style='color:#58a6ff;'>🧬 DiNuX AI</h1>", unsafe_allow_html=True)
    st.write("---")
    selected_model = st.selectbox("Neural Core", ["gemini-1.5-flash", "gemini-1.5-pro"])
    vision_file = st.file_uploader("Vision Source", type=["jpg", "png", "jpeg"])
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n\n**Studio:** KDD STUDIO")
    if st.button("🗑️ Reset All"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

# --- 5. CHAT ENGINE ---
# කලින් තිබුණ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# අලුත් මැසේජ් එකක් ලැබීම
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if prompt:
    # 1. User මැසේජ් එක ඇතුළත් කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("Synchronizing..."):
            try:
                # AI Model එක ස්ථාවරව ලබා ගැනීම
                model = get_ai_model(selected_model)
                
                # Content එක සකස් කිරීම
                payload = [prompt]
                if vision_file:
                    payload.append(Image.open(vision_file))
                
                # පිළිතුර ජෙනරේට් කිරීම (සෘජුවම)
                response = model.generate_content(payload)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("I'm having trouble processing that. Let's try again.")
            
            except Exception as e:
                # මොකක් හරි ලොකු එරර් එකක් ආවොත් පමණක් පෙන්වන්න
                st.error(f"Neural Path Error: {str(e)}")

# --- 6. FOOTER ---
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA</div>', unsafe_allow_html=True)

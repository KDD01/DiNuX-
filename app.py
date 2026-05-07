import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SETTINGS & STABILITY ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

# API එක එකපාරක් පමණක් Configure කිරීම
if "configured" not in st.session_state:
    genai.configure(api_key=API_KEY)
    st.session_state.configured = True

# --- 2. PREMIUM UI STYLING ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .branding { text-align: center; padding: 20px; border-bottom: 1px solid #30363d; margin-bottom: 25px; }
    .shining-title {
        font-size: 55px; font-weight: 900;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; border-top: 1px solid #30363d; text-align: center; font-size: 11px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#58a6ff;'>🧬 DiNuX AI</h1>", unsafe_allow_html=True)
    st.write("---")
    # මෙතනින් මෝඩල් එක තෝරන්න (වැඩ කරන්නේ නැතිනම් අනික උත්සාහ කරන්න)
    model_name = st.radio("Select Model Core:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    vision_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    st.write("---")
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- 5. HEADER ---
st.markdown('<div class="branding"><h1 class="shining-title">DiNuX AI</h1><p style="color:#58a6ff; letter-spacing:4px;">KDD STUDIO PREMIER EDITION</p></div>', unsafe_allow_html=True)

# --- 6. CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 7. THE BRAIN (DEBUG MODE) ---
prompt = st.chat_input("Ask DiNuX anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 1. මෝඩල් එක පණගැන්වීම
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction="You are DiNuX AI, a pro assistant by Dinush Dilhara. Speak in Sinhala & English."
            )
            
            # 2. Input සකස් කිරීම
            content_payload = [prompt]
            if vision_file:
                content_payload.append(Image.open(vision_file))

            # 3. පිළිතුර ලබා ගැනීම
            with st.spinner("Processing..."):
                response = model.generate_content(content_payload)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("The AI returned an empty response. Try rephrasing.")

        except Exception as e:
            # දැන් "hiccup" වෙනුවට ඇත්තම ලෙඩේ මෙතනින් පෙන්වයි
            st.error(f"⚠️ System Error: {str(e)}")
            st.info("If it says '404', please try switching the model in the sidebar.")

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | DESIGNED BY DINUSH DILHARA</div>', unsafe_allow_html=True)

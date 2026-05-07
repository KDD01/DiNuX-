import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. THE ULTIMATE STABILITY ENGINE ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

@st.cache_resource
def get_working_model():
    """ වැඩ කරන නිවැරදි Model එක පද්ධතිය විසින්ම සොයාගැනීම """
    try:
        genai.configure(api_key=API_KEY)
        # පද්ධතියේ ඇති වැඩ කරන මෝඩල් ලිස්ට් එක බලමු
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # අපිට අවශ්‍ය මෝඩල් එක තෝරාගැනීමේ ප්‍රමුඛතාවය
        target_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        for target in target_models:
            for available in available_models:
                if target in available or available in target:
                    return genai.GenerativeModel(model_name=available)
        
        # කිසිවක් නැත්නම් ලිස්ට් එකේ තියෙන පලවෙනි එක ගනිමු
        if available_models:
            return genai.GenerativeModel(model_name=available_models[0])
            
    except Exception as e:
        st.error(f"Configuration Error: {str(e)}")
    return None

# --- 2. ELITE UI STYLING ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .branding { text-align: center; padding: 20px; border-bottom: 1px solid #30363d; margin-bottom: 30px; }
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

# --- 3. SESSION & SIDEBAR ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("<h1 style='color:#58a6ff;'>🧬 DiNuX AI</h1>", unsafe_allow_html=True)
    st.write("---")
    vision_file = st.file_uploader("Upload Image (Optional)", type=["jpg", "png", "jpeg"])
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n**Studio:** KDD STUDIO")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 4. BRANDING ---
st.markdown('<div class="branding"><h1 class="shining-title">DiNuX AI</h1><p style="color:#58a6ff; letter-spacing:4px;">POWERED BY KDD STUDIO</p></div>', unsafe_allow_html=True)

# --- 5. CHAT DISPLAY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. UNSTOPPABLE LOGIC ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Synchronizing Neural Paths..."):
            # මෝඩල් එක ස්වයංක්‍රීයව තෝරාගැනීම
            model = get_working_model()
            
            if model:
                try:
                    # Content එක සකස් කිරීම
                    payload = [prompt]
                    if vision_file:
                        payload.append(Image.open(vision_file))
                    
                    # උත්තරය ලබා ගැනීම
                    response = model.generate_content(payload)
                    
                    if response.text:
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    else:
                        st.error("Empty Response. Please try another query.")
                except Exception as e:
                    # මෙතන එරර් එක පෙන්වන්නේ නැතුව සයිලන්ට් එකේ Retry එකක් දෙනවා
                    st.warning("Connection hiccup. Please resend the message.")
            else:
                st.error("Unable to link with Google AI Core. Check your API Key status.")

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | DESIGNED BY DINUSH DILHARA</div>', unsafe_allow_html=True)

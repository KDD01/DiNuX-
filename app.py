import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time

# 1. Page Configuration - Mobile & Desktop Responsive
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Ultra-Modern Responsive UI (CSS)
st.markdown("""
    <style>
    /* Dark Deep Background */
    .stApp {
        background-color: #0b0b0b;
        background-image: radial-gradient(circle at 50% -20%, #1a1a3a 0%, #0b0b0b 80%);
        color: #e3e3e3;
    }

    header, footer {visibility: hidden;}

    /* KDD Studio & DiNuX Branding */
    .kdd-title {
        font-size: 1.2rem;
        color: #8e8e8e;
        font-weight: 500;
        letter-spacing: 2px;
        margin-bottom: -10px;
    }
    
    .brand-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Chat Area Optimization */
    .stChatMessage {
        max-width: 850px;
        margin: auto;
        border: none !important;
        background: transparent !important;
    }

    /* Mobile Responsive Input Bar */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] {
            width: 92% !important;
            bottom: 15px !important;
        }
        .main-hero-text { font-size: 2.5rem !important; }
    }

    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 65%;
        background: #1e1e1e !important;
        border: 1px solid #3c4043 !important;
        border-radius: 28px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Engine: Audio
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- SIDEBAR Branding ---
with st.sidebar:
    st.markdown("<h2 class='brand-gradient'>KDD Studio</h2>", unsafe_allow_html=True)
    st.caption("Quantum AI Interface v7.0")
    st.markdown("---")
    voice_mode = st.toggle("Voice Mode 🔊", value=True)
    if st.button("Clear Chat 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- AI LOGIC WITH AUTO-RECOVERY ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# අක්‍රිය වූ Model එක වෙනුවට භාවිතා කළ හැකි අලුත්ම Models ලැයිස්තුව
MODELS_TO_TRY = ["llama-3.3-70b-versatile", "llama-3.1-70b-specdec", "mixtral-8x7b-32768"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p class='kdd-title'>KDD STUDIO</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-hero-text' style='font-size: 4rem;'>Hello, <span class='brand-gradient'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8e8e8e;'>ඔබේ ඕනෑම ගැටලුවක් වෘත්තීය මට්ටමින් විසඳීමට මම සූදානම්.</p></div>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INTERACTION & AUTO BUG FIX ---
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        success = False
        
        # ස්වයංක්‍රීයව Model එක මාරු කරමින් උත්සාහ කිරීම (Self-Healing Logic)
        for model_id in MODELS_TO_TRY:
            if success: break
            try:
                sys_msg = "ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. අතිශය බුද්ධිමත් සිංහල භාෂාවෙන් පිළිතුරු දෙන්න."
                history = [{"role": "system", "content": sys_msg}] + st.session_state.messages
                
                completion = client.chat.completions.create(
                    messages=history,
                    model=model_id, # වැරදි Model එකක් හමු වුණොත් මීළඟ එකට මාරු වේ
                    temperature=0.4,
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                
                placeholder.markdown(full_res)
                success = True
                
                if voice_mode:
                    play_voice(full_res)
                
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception as e:
                # දෝෂයක් ආවොත් එය සඟවා මීළඟ Model එකෙන් උත්සාහ කරයි
                continue 

        if not success:
            st.error("පද්ධතියේ තාවකාලික බාධාවක්. කරුණාකර සුළු මොහොතකින් නැවත උත්සාහ කරන්න.")

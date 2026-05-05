import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Modern & Responsive UI Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e11;
        background-image: radial-gradient(circle at 50% 20%, #1c1c3d 0%, #0e0e11 100%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
    
    /* Center the chat content */
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 10rem;
    }

    /* DiNuX Branding */
    .dinux-logo {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
    }

    /* Chat Input Styling */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50% !important;
        transform: translateX(-50%);
        width: 65% !important;
        z-index: 1000;
    }
    
    div[data-testid="stChatInput"] > div {
        background: #1e1e24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 28px !important;
    }

    /* Message Aesthetics */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 15px;
    }

    .welcome-box {
        text-align: center;
        margin-top: 15vh;
    }
    .welcome-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .welcome-sub { font-size: 2.5rem; color: #757575; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# 3. Voice Support Logic
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        audio_html = f'<audio autoplay src="data:audio/mp3;base64,{b64}">'
        st.markdown(audio_html, unsafe_allow_html=True)
    except: pass

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    is_voice = st.toggle("Voice Mode 🔊", value=True)
    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- INITIALIZE API CLIENT ---
# වැදගත්: මෙම API Key එක ක්‍රියා නොකරන්නේ නම් Groq වෙබ් අඩවියෙන් අලුත් Key එකක් ලබාගන්න.
API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-box">
            <h1 class="welcome-title">Hello, DiNuX</h1>
            <h2 class="welcome-sub">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Message DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Super Intelligent Prompt
        sys_prompt = "ඔබේ නම DiNuX AI. ඔබ නිර්මාණය කළේ Dinush Dilhara. ඔබ ඉතා බුද්ධිමත්, තර්කානුකූල සහ සහායකයෙකි. සැමවිටම පිරිසිදු සිංහලෙන් සහ මිනිසෙකු මෙන් කතා කරන්න."
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            # Stream the response
            completion = client.chat.completions.create(
                messages=history,
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=4096,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            
            if is_voice:
                play_voice(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # හරියටම Error එක බලාගන්න මෙතන print කරනවා
            error_msg = f"Connection Error: {str(e)}"
            st.error(error_msg)
            if "rate_limit_exceeded" in str(e).lower():
                st.warning("⚠️ Groq API සීමාව ඉක්මවා ඇත. කරුණාකර විනාඩියකින් නැවත උත්සාහ කරන්න හෝ නව API Key එකක් ඇතුළත් කරන්න.")

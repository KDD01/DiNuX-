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

# 2. Modern Glassmorphism UI
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e11;
        background-image: radial-gradient(circle at 50% 20%, #1c1c3d 0%, #0e0e11 100%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
    
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 10rem;
    }

    .dinux-logo {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
    }

    /* Floating Chat Input like Gemini */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50% !important;
        transform: translateX(-50%);
        width: 65% !important;
        z-index: 1000;
        background: transparent !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background: #1e1e24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 28px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .welcome-box { text-align: center; margin-top: 15vh; }
    .welcome-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .welcome-sub { font-size: 2.5rem; color: #757575; font-weight: 500; }
    
    /* Smooth transition for messages */
    .stChatMessage {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Voice System
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Console")
    is_voice = st.toggle("Audio Response 🔊", value=True)
    if st.button("Refresh Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- INITIALIZE API ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
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

# Chat Logic
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # ADVANCED SYSTEM PROMPT TO STOP LOOPING
        sys_prompt = """
        ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara.
        වැදගත් උපදෙස්:
        1. ලැබෙන සෑම ප්‍රශ්නයක්ම ස්වාධීනව විශ්ලේෂණය කර තාර්කිකව (Logically) සිතා පිළිතුරු දෙන්න.
        2. එකම දේ නැවත නැවත පැවසීමෙන් (Looping) වළකින්න. පිළිතුර කෙටි හා පැහැදිලිව අවසන් කරන්න.
        3. සිංහල භාෂාව භාවිතා කිරීමේදී ඉතා ස්වාභාවික වචන භාවිතා කරන්න.
        4. ප්‍රශ්නයට අදාළ නැති දේවල් පවසා කාලය නාස්ති නොකරන්න.
        """
        
        # Keeping history context but preventing it from confusing the model
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:] # Only last 10 messages for focus

        try:
            completion = client.chat.completions.create(
                messages=history,
                model="llama-3.3-70b-versatile",
                temperature=0.4, # Balanced for logic and creativity
                max_tokens=2048,
                top_p=0.9,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    text_chunk = chunk.choices[0].delta.content
                    full_response += text_chunk
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            
            if is_voice:
                play_voice(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("System connection busy. Please try again.")

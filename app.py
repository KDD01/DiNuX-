import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import os

# 1. Gemini Style Config
st.set_page_config(
    page_title="DiNuX AI",
    page_icon="✨",
    layout="centered", # Gemini පෙනුම සඳහා මෙය centered විය යුතුයි
    initial_sidebar_state="collapsed"
)

# 2. Gemini UI (Mobile-First) CSS
st.markdown("""
    <style>
    /* Gemini Dark Theme Background */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }

    /* Remove Streamlit Header & Padding */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        max-width: 800px !important;
    }

    /* Gemini Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding-top: 20px !important;
        font-family: 'Google Sans', sans-serif;
    }

    /* User Message Style */
    [data-testid="stChatMessage"][data-testid="chatAvatarIcon-user"] {
        background-color: #2b2b2b !important;
    }

    /* Chat Input Bar - Fixed at Bottom Like Mobile App */
    .stChatInputContainer {
        position: fixed;
        bottom: 20px;
        background-color: #1e1f20 !important;
        border-radius: 28px !important;
        border: 1px solid #444746 !important;
        padding: 5px 15px !important;
    }

    /* Titles and Text */
    h1 {
        font-family: 'Google Sans', sans-serif;
        font-weight: 500;
        color: #e3e3e3;
        font-size: 2.2rem;
        text-align: left;
    }

    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #444746;
    }

    /* Responsive Mobile Fixes */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem; }
        .block-container { padding: 1rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Voice Engine
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.read()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- UI Setup ---
with st.sidebar:
    st.markdown("### DiNuX Settings")
    voice_enabled = st.checkbox("Voice Response", value=False)
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")

# Main Header
st.markdown('<h1>Hello, <span class="gemini-gradient">I\'m DiNuX</span></h1>', unsafe_allow_html=True)
st.markdown("<p style='color: #8e918f;'>සෑම විටම නිවැරදි සහ තර්කානුකූල පිළිතුරු...</p>", unsafe_allow_html=True)

# API & Session
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Message Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input Logic
if prompt := st.chat_input("ඔබේ ප්‍රශ්නය මෙතැනින් විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # දිනුෂ්, මේ තමයි ඔයා ඉල්ලපු Logical & Direct Answer pattern එක
        sys_instruction = """
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara.
        ඔබේ පිළිතුරු සැපයීමේ රටාව (Response Pattern):
        1. කෙලින්ම ප්‍රශ්නයට පිළිතුර දෙන්න (Direct & Precise).
        2. අනවශ්‍ය හැඳින්වීම් හෝ අනවශ්‍ය පැහැදිලි කිරීම් (Fillers) සම්පූර්ණයෙන්ම ඉවත් කරන්න.
        3. තර්කානුකූලව (Logically) කරුණු ගලපා පිළිතුරු දෙන්න.
        4. පරිශීලකයා 'ඔබ කවුද' කියා ඇසුවහොත් පමණක් 'නිර්මාණය කළේ Dinush Dilhara' බව කියන්න.
        5. සැමවිටම ස්වභාවික සිංහල භාෂාව (Unicode) භාවිතා කරන්න.
        """
        
        full_history = [{"role": "system", "content": sys_instruction}] + st.session_state.messages

        try:
            response_container = st.empty()
            completion = client.chat.completions.create(
                messages=full_history,
                model="llama-3.3-70b-versatile",
                temperature=0.4, # ඉතාමත් නිවැරදි පිළිතුරු සඳහා low temperature එකක් යෙදුවා
                max_tokens=1024
            )
            
            final_response = completion.choices[0].message.content
            response_container.markdown(final_response)
            
            if voice_enabled:
                play_voice(final_response)
                
            st.session_state.messages.append({"role": "assistant", "content": final_response})
        except Exception as e:
            st.error("දත්ත ලබා ගැනීමේදී දෝෂයක් ඇති විය.")

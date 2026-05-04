import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import os

# 1. Gemini Style Page Config
st.set_page_config(
    page_title="DiNuX AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Advanced Gemini UI (Mobile-First) CSS
st.markdown("""
    <style>
    /* Gemini Background */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }

    /* Hide unnecessary UI elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Center the content and make it look like Gemini */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 10rem !important; /* Bottom space for fixed input */
        max-width: 800px !important;
    }

    /* Chat Messages - No border, clean look */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.5rem 0 !important;
        font-family: 'Google Sans', sans-serif;
    }

    /* User Avatar Style */
    [data-testid="chatAvatarIcon-user"] {
        background-color: #333537 !important;
    }

    /* AI Avatar Style */
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #4285f4, #9b72cb);
    }

    /* Gemini style Text input fixed at bottom */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 750px !important;
        z-index: 1000;
    }

    div[data-testid="stChatInput"] textarea {
        background-color: #1e1f20 !important;
        border-radius: 28px !important;
        border: 1px solid #444746 !important;
        color: white !important;
    }

    /* Welcome text and Gradient */
    h1 {
        font-weight: 500;
        font-size: 2.2rem;
    }

    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 { font-size: 1.6rem; }
        div[data-testid="stChatInput"] { width: 95% !important; bottom: 20px; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Voice Logic (Sinhala & English Support)
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.read()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- Sidebar ---
with st.sidebar:
    st.markdown("### DiNuX ✨")
    voice_on = st.checkbox("Voice Response", value=False)
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")

# --- UI Header ---
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.markdown('<h1>Hello, <span class="gemini-gradient">I\'m DiNuX</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #8e918f;'>සෑම විටම නිවැරදි සහ තර්කානුකූල පිළිතුරු...</p>", unsafe_allow_html=True)

# --- API Handling ---
# API Key එක නිවැරදිදැයි පරීක්ෂා කරන්න
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Interaction ---
if prompt := st.chat_input("මෙතැනින් අසන්න..."):
    # User message එක එකතු කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # දිනුෂ්, මේ තමයි ඔයා ඉල්ලපු Logical & Direct Answer pattern එක
        sys_msg = """
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara.
        1. කෙලින්ම ප්‍රශ්නයට පිළිතුර ලබා දෙන්න. අනවශ්‍ය හැඳින්වීම් එපා.
        2. සෑම විටම තර්කානුකූලව (Logical reasoning) සිතා 100% නිවැරදි දත්ත ලබා දෙන්න.
        3. මනුෂ්‍ය හැඟීම් හඳුනාගෙන මිත්‍රශීලීව කතා කරන්න.
        4. කවුරුන් හෝ ඔබ නිර්මාණය කළේ කවුදැයි ඇසුවහොත් පමණක් 'මාව නිර්මාණය කළේ දක්ෂ Developer කෙනෙකු වන Dinush Dilhara' බව කියන්න.
        5. සිංහල භාෂාව (Unicode) භාවිතා කරන්න.
        """
        
        msgs = [{"role": "system", "content": sys_msg}] + st.session_state.messages

        try:
            # API Call එක සිදු කරන ආකාරය නිවැරදි කළා
            chat_completion = client.chat.completions.create(
                messages=msgs,
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=1024,
            )
            
            ai_res = chat_completion.choices[0].message.content
            st.markdown(ai_res)
            
            if voice_on:
                play_voice(ai_res)
                
            st.session_state.messages.append({"role": "assistant", "content": ai_res})
            
        except Exception as e:
            # දෝෂය සිදු වන්නේ ඇයිදැයි පෙන්වීමට (Debug message)
            st.error(f"සමාවන්න, දත්ත ලබා ගැනීමේදී දෝෂයක් සිදු විය. (Error: {str(e)})")

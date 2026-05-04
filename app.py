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
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Advanced CSS for Gemini UI & Floating Bottom Input
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Content Container */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 8rem !important;
        max-width: 800px !important;
    }

    /* Chat Messages Styles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1rem 0 !important;
    }

    /* Floating Chat Input at Bottom */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 700px !important;
        z-index: 1000;
        background-color: #1e1f20 !important;
        border-radius: 30px !important;
        padding: 4px !important;
    }

    div[data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        border: none !important;
        color: white !important;
    }

    /* Sidebar/Menu Design */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #333;
    }

    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 95% !important; bottom: 20px; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logic Functions
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.read()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- Sidebar (The Menu) ---
with st.sidebar:
    st.markdown("<h2 class='gemini-gradient'>Menu</h2>", unsafe_allow_html=True)
    st.markdown("---")
    voice_on = st.toggle("Voice Mode 🔊", value=False)
    if st.button("Clear Chat 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Developed by Dinush Dilhara")
    st.caption("Version: 2.0 (Stable)")

# --- Chat Engine ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
if not st.session_state.messages:
    st.markdown('<h1>Hello, <span class="gemini-gradient">I\'m DiNuX</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #8e918f;'>සෑම විටම නිවැරදි සහ තර්කානුකූල පිළිතුරු...</p>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("මෙතැනින් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # දිනුෂ්, මෙතන මම Model එක මාරු කළා Rate limit ප්‍රශ්නය නිසා
        sys_msg = """
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara.
        1. කෙලින්ම ප්‍රශ්නයට පිළිතුරු දෙන්න.
        2. අනවශ්‍ය හැඳින්වීම් සම්පූර්ණයෙන්ම ඉවත් කරන්න.
        3. තර්කානුකූලව සහ බුද්ධිමත් ලෙස පිළිතුරු සපයන්න.
        4. සිංහල භාෂාව භාවිතා කරන්න.
        """
        
        history = [{"role": "system", "content": sys_msg}] + st.session_state.messages

        try:
            # මෙතන Model එක 'llama3-8b-8192' ලෙස වෙනස් කර ඇත (Error එක මඟහැරීමට)
            chat = client.chat.completions.create(
                messages=history,
                model="llama3-8b-8192",
                temperature=0.6,
                max_tokens=1024,
            )
            
            res = chat.choices[0].message.content
            st.markdown(res)
            
            if voice_on:
                play_voice(res)
                
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        except Exception as e:
            # Error එකක් ආවොත් පෙන්වන ආකාරය
            st.warning("සමාවන්න, සේවාදායකයේ තදබදයක් පවතී. කරුණාකර සුළු මොහොතකින් නැවත උත්සාහ කරන්න.")

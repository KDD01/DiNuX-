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

# 2. Modern UI Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e11;
        background-image: radial-gradient(circle at 50% 20%, #1c1c3d 0%, #0e0e11 100%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
    
    .block-container {
        max-width: 900px;
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

    .welcome-box { text-align: center; margin-top: 15vh; }
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

# 3. Voice Logic
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
    is_voice = st.toggle("Voice Mode 🔊", value=True)
    if st.button("Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# --- ENGINE ---
# කරුණාකර ඔබගේ Groq API Key එක මෙහි භාවිතා කරන්න.
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

# History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Message DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # FACTUAL & LOGICAL SYSTEM PROMPT
        sys_prompt = """
        ඔබේ නම DiNuX AI. ඔබ නිර්මාණය කළේ Dinush Dilhara.
        ඔබේ ප්‍රධාන වගකීම වන්නේ පරිශීලකයා අසන ප්‍රශ්න වලට 100% ක් නිවැරදි, සත්‍ය සහ තාර්කික තොරතුරු ලබා දීමයි.
        නීති:
        1. හිතලු හෝ අසත්‍ය තොරතුරු (Hallucinations) ලබා නොදෙන්න.
        2. ඔබ යම් දෙයක් ගැන නොදන්නේ නම්, එය නොදන්නා බව අවංකව පවසන්න.
        3. පිළිතුරු දීමට පෙර කරුණු කිහිපවරක් තර්කානුකූලව විශ්ලේෂණය කරන්න.
        4. පිරිසිදු සිංහල භාෂාව සහ ගෞරවනීය ස්වරූපය භාවිතා කරන්න.
        5. තොරතුරු සැපයීමේදී අදාළ විෂය ක්ෂේත්‍රයේ නිවැරදිම දත්ත භාවිතා කරන්න.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            completion = client.chat.completions.create(
                messages=history,
                model="llama-3.3-70b-versatile",
                temperature=0.1,  # ඉතා අඩු අගයක් දමා ඇත (වැඩි නිවැරදිභාවයක් සඳහා)
                max_tokens=4096,
                top_p=1,
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
            st.error(f"Error: API limit reached or Connection lost. ({e})")

import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
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

# 2. UI Styling (Gemini Dark Vibe)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e11;
        background-image: radial-gradient(circle at 50% 20%, #1c1c3d 0%, #0e0e11 100%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
    .block-container { max-width: 850px; padding-bottom: 10rem; }
    
    .dinux-logo {
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.2rem; text-align: center;
    }

    div[data-testid="stChatInput"] {
        position: fixed; bottom: 40px; left: 50% !important;
        transform: translateX(-50%); width: 75% !important;
        z-index: 1000;
    }
    
    div[data-testid="stChatInput"] > div {
        background: #1e1e24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 28px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- API CORE SETUP (CRITICAL FIX) ---
GEMINI_API_KEY = "AIzaSyB-3mqtHBYgaEqTSi1aACF76VH745vvejs"

try:
    # API එක Configure කිරීමේදී වඩාත් ස්ථාවර ක්‍රමය භාවිතා කිරීම
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 404 Error එක මගහැරීමට වඩාත් ගැලපෙන model නම භාවිතා කිරීම
    # මෙහිදී 'gemini-1.5-flash' යනු වඩාත් ස්ථාවර අනුවාදයයි
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Configuration Issue: {e}")

# Web Search
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n\n".join(results)
    except: return ""

# Voice Output
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- SESSION HANDLING ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
if not st.session_state.messages:
    st.markdown(f"""
        <div style="text-align:center; margin-top:20vh;">
            <p style="color:#4facfe; font-weight:bold; letter-spacing:2px; margin-bottom:0;">DS MEDIA HUB</p>
            <h1 style="font-size:4rem; font-weight:700; background:linear-gradient(90deg, #4285f4, #9b72cb, #d96570); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Hello, DiNuX</h1>
            <h2 style="font-size:2rem; color:#5f6368; font-weight:500;">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Processing
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Search live data
        search_results = search_web(prompt)
        
        # Instructions
        sys_instructions = f"""
        ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara.
        සත්‍ය තොරතුරු පමණක් ලබා දෙන්න. පිරිසිදු සිංහල හා ඉංග්‍රීසි භාවිතා කරන්න.
        Live Search Context: {search_results}
        """
        
        try:
            # Response Generation
            response = model.generate_content([sys_instructions, prompt], stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            play_voice(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # මෙහිදී Error එකක් ආවොත් එය පැහැදිලිව පෙන්වයි
            st.error(f"බාධාවක් ඇති විය: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

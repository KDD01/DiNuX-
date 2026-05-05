import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import base64
from gtts import gTTS
import io
import time

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. UI Styling (Your Favorite Dark Gemini UI)
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

    .welcome-section {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; height: 50vh; text-align: center;
    }
    .welcome-text {
        font-size: 4rem; font-weight: 700;
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-welcome { font-size: 2.5rem; color: #5f6368; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE SETUP ---

# Your Provided Gemini API Key
GEMINI_API_KEY = "AIzaSyB-3mqtHBYgaEqTSi1aACF76VH745vvejs"
genai.configure(api_key=GEMINI_API_KEY)

# Safety & Generation Config
generation_config = {
  "temperature": 0.3, # වැඩි නිරවද්‍යතාවයක් සඳහා
  "top_p": 0.95,
  "max_output_tokens": 8192,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

# Web Search Function (Live Truthful Data)
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=4)]
            return "\n\n".join(results)
    except:
        return ""

# Voice Output Function
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- SESSION HANDLING ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-section">
            <p style="color:#4facfe; font-weight:bold; letter-spacing:2px; margin-bottom:0;">DS MEDIA HUB</p>
            <h1 class="welcome-text">Hello, DiNuX</h1>
            <h2 class="sub-welcome">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT PROCESSING ---
if prompt := st.chat_input("Ask DiNuX anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # 1. Live Web Search (For 100% truth)
        search_results = search_web(prompt)
        
        # 2. System Instructions for Personality & Language
        sys_instructions = f"""
        ඔබේ නම DiNuX AI. ඔබ නිර්මාණය කළේ Dinush Dilhara (DS Media Hub).
        පහත ලබා දී ඇති සජීවී සෙවුම් තොරතුරු ඇසුරින් පමණක් 100% නිවැරදි පිළිතුරු දෙන්න.
        සජීවී තොරතුරු: {search_results}
        
        නීති:
        - සිංහල සහ ඉංග්‍රීසි භාෂා දෙකම ඉතාමත් ස්වාභාවිකව සහ නිවැරදිව භාවිතා කරන්න.
        - බොරු තොරතුරු ලබා නොදෙන්න.
        - සැමවිටම මිත්‍රශීලී සහ බුද්ධිමත් සහායකයෙකු වන්න.
        """
        
        try:
            # 3. Streamed Generation using Gemini
            response = model.generate_content([sys_instructions, prompt], stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            play_voice(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("දත්ත සැකසීමේදී සුළු බාධාවක් ඇති විය. කරුණාකර නැවත උත්සාහ කරන්න.")

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("Developed by Dinush Dilhara for DS Media Hub.")
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

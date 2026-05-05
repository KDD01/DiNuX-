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

# 2. UI Styling (Gemini Dark Theme)
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

# --- API SETUP ---
GEMINI_API_KEY = "AIzaSyB-3mqtHBYgaEqTSi1aACF76VH745vvejs"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Configuration Error: {e}")

# Web Search
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n\n".join(results)
    except: return ""

# Voice
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- SESSION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-section">
            <p style="color:#4facfe; font-weight:bold; letter-spacing:2px;">DS MEDIA HUB</p>
            <h1 class="welcome-text">Hello, DiNuX</h1>
            <h2 class="sub-welcome">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        search_data = search_web(prompt)
        
        sys_instructions = f"""
        ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara (DS Media Hub).
        සජීවී දත්ත: {search_data}
        ලබා දී ඇති දත්ත ඇසුරින් 100% නිවැරදිව සිංහලෙන් හෝ ඉංග්‍රීසියෙන් පිළිතුරු දෙන්න.
        """
        
        try:
            # ඉල්ලීම යැවීම
            response = model.generate_content([sys_instructions, prompt], stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            play_voice(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # වැරැද්ද මොකක්ද කියලා මෙතනින් බලාගන්න පුළුවන්
            st.error(f"Error: {str(e)}")

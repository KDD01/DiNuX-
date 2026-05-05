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

# 2. UI Styling (Branding and Design)
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

# --- API CORE SETUP (AUTO-DETECTION LOGIC) ---
GEMINI_API_KEY = "AIzaSyB-3mqtHBYgaEqTSi1aACF76VH745vvejs"

def initialize_model():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # දැනට පවතින Models ලැයිස්තුව පරීක්ෂා කර වැඩ කරන එකක් තෝරා ගැනීම
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # වඩාත්ම ගැලපෙන Model එකක් තෝරා ගැනීම (Priority List)
        priority_models = ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.5-pro']
        
        selected_model = None
        for pm in priority_models:
            if pm in available_models:
                selected_model = pm
                break
        
        if not selected_model:
            selected_model = available_models[0] # කිසිවක් නැතිනම් ලැයිස්තුවේ පළමුවැන්න
            
        return genai.GenerativeModel(selected_model)
    except Exception as e:
        st.error(f"Initialization Failed: {e}")
        return None

model = initialize_model()

# Helper Functions
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n\n".join(results)
    except: return ""

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

if not st.session_state.messages:
    st.markdown(f"""
        <div style="text-align:center; margin-top:20vh;">
            <p style="color:#4facfe; font-weight:bold; letter-spacing:2px; margin-bottom:0;">DS MEDIA HUB</p>
            <h1 style="font-size:4rem; font-weight:700; background:linear-gradient(90deg, #4285f4, #9b72cb, #d96570); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Hello, DiNuX</h1>
            <h2 style="font-size:2rem; color:#5f6368; font-weight:500;">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- PROCESSING ---
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        search_results = search_web(prompt)
        
        sys_instructions = f"""
        ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara.
        Context: {search_results}
        100% සත්‍ය තොරතුරු සිංහලෙන් හෝ ඉංග්‍රීසියෙන් ලබා දෙන්න.
        """
        
        try:
            if model:
                response = model.generate_content([sys_instructions, prompt], stream=True)
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                play_voice(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("AI Model එක ක්‍රියාත්මක කළ නොහැක. කරුණාකර API Key එක පරීක්ෂා කරන්න.")
        except Exception as e:
            st.error(f"බාධාවක් ඇති විය: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

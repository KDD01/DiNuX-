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
    initial_sidebar_state="expanded"
)

# 2. UI Styling (Enhanced Glassmorphism UI)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e1e3f 0%, #0e0e11 100%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0e0e11; }
    ::-webkit-scrollbar-thumb { background: #3c4043; border-radius: 10px; }

    /* Logo & Text Styling */
    .dinux-logo {
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem; text-align: center;
        filter: drop-shadow(0 2px 10px rgba(0,0,0,0.3));
    }

    /* Chat Styling */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
    }

    /* Input Bar Fix */
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; 
        z-index: 1000; background: transparent !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background: #1e1e24 !important;
        border: 1px solid #4facfe !important;
        border-radius: 30px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }

    /* Welcome Screen */
    .welcome-box {
        text-align: center; margin-top: 15vh;
        animation: fadeIn 1.5s ease-in;
    }
    @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
    </style>
    """, unsafe_allow_html=True)

# --- API CORE SETUP ---
# ඔබ ලබාදුන් අලුත් API Key එක මෙතැනට ඇතුළත් කර ඇත
GEMINI_API_KEY = "AIzaSyB27W11humZP7AiXWmrkwEHQcNq2LXxjkw"

def initialize_model():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # පවතින Models හඳුනා ගැනීම
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # වඩාත් ස්ථාවර Models තෝරා ගැනීම
        priority = ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.5-pro']
        selected = next((m for m in priority if m in available_models), available_models[0] if available_models else None)
        
        if selected:
            return genai.GenerativeModel(selected)
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
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
        tts = gTTS(text=text[:500], lang=lang, slow=False) # Limit length for speed
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
    st.markdown("""
        <div class="welcome-box">
            <h1 style="font-size: 4.5rem; font-weight: 900; color: white;">DiNuX <span style="color:#4facfe;">AI</span></h1>
            <p style="font-size: 1.5rem; color: #aaa;">Dinush Dilhara ගේ නිර්මාණයක්... ඔබට කෙසේ උදව් වෙන්නද?</p>
        </div>
    """, unsafe_allow_html=True)

# History Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- PROCESSING ---
if prompt := st.chat_input("Ask anything from DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Web Search logic
        search_data = search_web(prompt)
        sys_prompt = f"ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara. තොරතුරු: {search_data}. සැමවිටම කෙටියෙන් සහ පැහැදිලිව පිළිතුරු දෙන්න."
        
        try:
            if model:
                # Streaming Response
                response = model.generate_content([sys_prompt, prompt], stream=True)
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                play_voice(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Model unavailable. Please double check your API Key settings.")
        except Exception as e:
            st.error(f"නැවත උත්සාහ කරන්න (Error: {str(e)})")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Advanced Artificial Intelligence</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Developer Details")
    st.write("👤 **Name:** Dinush Dilhara")
    st.write("🌐 **Platform:** DS MEDIA HUB")
    st.info("මෙම AI පද්ධතිය Google Gemini 1.5 තාක්ෂණයෙන් බලගන්වා ඇත.")

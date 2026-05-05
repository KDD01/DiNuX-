import streamlit as st
from groq import Groq
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

# 2. UI Styling (Keeping your favorite UI)
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
        transform: translateX(-50%); width: 65% !important;
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

# 3. Core Engine Functions
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
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

# --- API INITIALIZATION ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-section">
            <h1 class="welcome-text">Hello, DiNuX</h1>
            <h2 class="sub-welcome">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT LOGIC WITH ERROR RECOVERY ---
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # 1. Background Search (Live Data)
        search_context = search_web(prompt)
        
        sys_prompt = f"""
        ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara.
        වැදගත්: පරිශීලකයාට 100% නිවැරදි තොරතුරු ලබා දෙන්න. 
        සෙවුම් ප්‍රතිඵල: {search_context}
        තාර්කිකව සිතා පිළිතුරු දෙන්න. Looping වීම වළක්වන්න. පිරිසිදු සිංහල භාවිතා කරන්න.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-8:]

        # 2. Advanced Multi-Model Request
        models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]
        success = False

        for model_name in models_to_try:
            if success: break
            try:
                completion = client.chat.completions.create(
                    messages=history,
                    model=model_name,
                    temperature=0.3,
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                success = True
                
            except Exception as e:
                # If rate limited, wait a second and try the next model
                if model_name != models_to_try[-1]:
                    time.sleep(1)
                    continue
                else:
                    st.error("පද්ධතියේ අධික කාර්යබහුල බවක් පවතී. කරුණාකර විනාඩියකින් නැවත උත්සාහ කරන්න.")

        if success:
            play_voice(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar Settings
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

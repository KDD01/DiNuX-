import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import base64
from gtts import gTTS
import io
import time
import random

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. UI Styling (Keeping your favorite layout)
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

# 3. Secure API Key Management
# සීමාව ඉක්මවා යාම වැළැක්වීමට මෙතනට තව Keys 2ක් විතර දාන්න.
API_KEYS = [
    "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"
]

def get_client():
    # අහඹු ලෙස Key එකක් තෝරා ගැනීම මගින් සීමාවන් බෙදී යයි
    selected_key = random.choice(API_KEYS)
    return Groq(api_key=selected_key)

# 4. Core Functions
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

# --- APP LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<div style='text-align:center; margin-top:20vh;'><h1 style='font-size:4rem; color:white;'>Hello, <span style='color:#4facfe;'>DiNuX</span></h1><h2 style='color:#757575;'>How can I help you today?</h2></div>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # 1. Search Live Context
        search_data = search_web(prompt)
        
        # 2. System Instructions
        sys_instructions = f"""
        ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara.
        සත්‍ය තොරතුරු පමණක් ලබා දෙන්න. පිරිසිදු සිංහල හා ඉංග්‍රීසි භාවිතා කරන්න.
        Search Context: {search_data}
        """
        
        history = [{"role": "system", "content": sys_instructions}] + st.session_state.messages[-10:]

        # 3. High-Stability Request Logic (Models 3ක් හරහා උත්සාහ කිරීම)
        available_models = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama3-70b-8192"]
        success = False
        
        for model in available_models:
            if success: break
            try:
                client = get_client()
                completion = client.chat.completions.create(
                    messages=history,
                    model=model,
                    temperature=0.3,
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                play_voice(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                success = True
                
            except Exception as e:
                # Rate limit දෝෂයක් නම් තත්පරයක් රැඳී සිට ඊළඟ Model එක බලන්න
                time.sleep(1.5)
                continue 

        if not success:
            st.error("සියලුම පද්ධති මේ මොහොතේ කාර්යබහුලයි. කරුණාකර තත්පර 30කින් නැවත උත්සාහ කරන්න.")

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

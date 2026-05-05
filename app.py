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
    initial_sidebar_state="expanded"
)

# 2. Advanced UI Styling (Same UI, Higher Stability)
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
        transform: translateX(-50%); width: 80% !important;
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

# 3. API Key Rotation Logic (To prevent "Busy" Error)
# ඔබට පුළුවන් නම් තව API Keys 2-3ක් හදලා මේ List එකට දාන්න. එවිට සීමාවන් වැටෙන්නේ නැත.
API_KEYS = [
    "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",
    # "මෙතනට තව Key එකක් දාන්න",
    # "මෙතනට තව Key එකක් දාන්න"
]

def get_groq_client(user_key=None):
    if user_key:
        return Groq(api_key=user_key)
    return Groq(api_key=random.choice(API_KEYS))

# 4. Helper Functions
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=4)]
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

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    user_api_key = st.text_input("Custom Groq API Key (Optional)", type="password", help="සීමාවන් ඉක්මවා ගියහොත් ඔබේම Key එකක් මෙතනට ලබා දිය හැක.")
    st.info("Created by Dinush Dilhara for DS Media Hub.")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT ENGINE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
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
        
        search_context = search_web(prompt)
        
        sys_prompt = f"""
        නම: DiNuX AI. නිර්මාණය කළේ: Dinush Dilhara.
        වැදගත්: සජීවී සෙවුම් ප්‍රතිඵල ඇසුරින් 100% නිවැරදි තොරතුරු දෙන්න.
        භාෂාව: සිංහල සහ ඉංග්‍රීසි ඉතාමත් නිවැරදිව භාවිතා කරන්න.
        Context: {search_context}
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]

        # Smart Retry Logic
        models = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama3-70b-8192"]
        client = get_groq_client(user_api_key if user_api_key else None)
        
        success = False
        for model_name in models:
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
                play_voice(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    continue # Try next model
                else:
                    st.error("පද්ධතියේ දෝෂයකි. කරුණාකර මොහොතකින් උත්සාහ කරන්න.")
                    break

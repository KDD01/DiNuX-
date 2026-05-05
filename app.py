import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import base64
from gtts import gTTS
import io
import time

# 1. Page Configuration (Keeping your standard layout)
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. UI Styling (Your Favorite Gemini-Style UI - No Changes)
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

# 3. Enhanced Web Search (Deep Crawl Logic)
def search_web(query):
    try:
        with DDGS() as ddgs:
            # සෙවුම් ප්‍රතිඵල 5ක් දක්වා වැඩි කර ඇත (වැඩි නිවැරදිභාවයක් සඳහා)
            results = [r['body'] for r in ddgs.text(query, max_results=5)]
            return "\n\n".join(results)
    except:
        return "Search error. Please verify facts manually."

# 4. Professional Voice Response
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

# --- API CORE ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen (Preserved)
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

# --- ADVANCED LOGIC PROCESSING ---
if prompt := st.chat_input("Ask DiNuX anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Live Fact-Checking
        with st.spinner("සත්‍ය තොරතුරු සොයමින්..."):
            search_context = search_web(prompt)
        
        # High-End System Instruction
        sys_prompt = f"""
        ඔබේ නම DiNuX AI. ඔබ Dinush Dilhara (KDD Studio) විසින් නිපදවන ලද සත්‍යවාදී සහ දියුණුම AI සහායකයායි.
        
        පිළිතුරු සැපයීමේ නීති:
        1. Accuracy First: පහත ලබා දී ඇති සජීවී සෙවුම් ප්‍රතිඵල පමණක් පදනම් කරගෙන පිළිතුර ගොඩනගන්න. හිතලු තොරතුරු සම්පූර්ණයෙන්ම තහනම්.
           සෙවුම් තොරතුරු: {search_context}
        2. Language Proficiency: 
           - සිංහල: ඉතාමත් පිරිසිදු, ගෞරවනීය සහ ස්වාභාවික (Human-like) සිංහල භාවිතා කරන්න.
           - English: Use professional, grammatically perfect, and clear English.
        3. Logic: ප්‍රශ්නය තාර්කිකව විශ්ලේෂණය කරන්න. පිළිතුරේ ගුණාත්මකභාවය 100% ක් විය යුතුය.
        4. No Looping: එකම වාක්‍යය නැවත නැවත නොකියන්න.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]

        # Multi-Model Stability (Error Recovery)
        models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]
        success = False

        for model_name in models_to_try:
            if success: break
            try:
                completion = client.chat.completions.create(
                    messages=history,
                    model=model_name,
                    temperature=0.2, # Accuracy එක උපරිම කිරීමට අඩු කර ඇත
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                success = True
                
            except Exception:
                if model_name != models_to_try[-1]:
                    time.sleep(1)
                    continue
                else:
                    st.error("System connection busy. Please wait a moment.")

        if success:
            play_voice(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("Created by Dinush Dilhara")
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

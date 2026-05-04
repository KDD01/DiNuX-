import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io

# 1. Page Configuration - Advanced Gemini Look
st.set_page_config(
    page_title="DiNuX AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Ultra-Modern Gemini UI CSS
st.markdown("""
    <style>
    /* Gemini Dark Theme */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    header, footer {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 10rem !important;
        max-width: 850px !important;
    }

    /* Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1.5rem 0 !important;
        border: none !important;
    }

    /* Avatar Styles */
    [data-testid="chatAvatarIcon-user"] { background-color: #333537 !important; }
    [data-testid="chatAvatarIcon-assistant"] { 
        background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570); 
    }

    /* Fixed Bottom Input Bar - Gemini Style */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 750px !important;
        background-color: #1e1f20 !important;
        border-radius: 32px !important;
        border: 1px solid #444746 !important;
        padding: 8px !important;
        z-index: 1000;
    }

    div[data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: white !important;
        border: none !important;
        font-size: 1rem !important;
    }

    /* Sidebar Menu Styling */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #333;
    }

    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
    }

    /* Mobile Fixes */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 95% !important; bottom: 15px; }
        .gemini-gradient { font-size: 1.8rem; }
    }
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

# --- Sidebar / Menu ---
with st.sidebar:
    st.markdown("<h2 class='gemini-gradient'>DiNuX</h2>", unsafe_allow_html=True)
    st.markdown("---")
    voice_on = st.toggle("Voice Response 🔊", value=False)
    if st.button("New Chat 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")
    st.caption("Model: Advanced Logical Engine")

# --- AI Core ---
# ඔයාගේ API Key එක මෙතන තියෙනවා
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Header
if not st.session_state.messages:
    st.markdown('<h1>Hello, <span class="gemini-gradient">I\'m DiNuX</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #8e918f; font-size: 1.2rem;'>සෑම විටම නිවැරදි සහ තර්කානුකූල පිළිතුරු...</p>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Interaction Logic ---
if prompt := st.chat_input("මෙතැනින් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # System Instruction: Direct & Logical
        sys_msg = """
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara.
        - පිළිතුර කෙලින්ම (Directly) ලබා දෙන්න. 
        - අනවශ්‍ය හැඳින්වීම් හෝ Fillers සම්පූර්ණයෙන්ම ඉවත් කරන්න.
        - තර්කානුකූලව (Logically) කරුණු ගලපා පිළිතුරු දෙන්න.
        - සිංහල භාෂාව භාවිතා කරන්න.
        """
        
        history = [{"role": "system", "content": sys_msg}] + st.session_state.messages

        try:
            # පද්ධතියේ වේගය සහ සීමාවන් (Limits) අනුව හොඳම Model එක මෙහි යොදා ඇත
            chat = client.chat.completions.create(
                messages=history,
                model="llama-3.1-8b-instant", # මෙය ඉතා වේගවත් සහ Error අඩු මාදිලියකි
                temperature=0.4,
                max_tokens=2048
            )
            
            res = chat.choices[0].message.content
            st.markdown(res)
            
            if voice_on:
                play_voice(res)
                
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        except Exception as e:
            # දෝෂයක් ආවොත් Mixtral මාදිලියට මාරු වී නැවත උත්සාහ කිරීම (Fallback Mechanism)
            try:
                chat = client.chat.completions.create(
                    messages=history,
                    model="mixtral-8x7b-32768",
                    temperature=0.5
                )
                res = chat.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("සේවාදායකයේ තාවකාලික බාධාවක් පවතී. කරුණාකර තප්පර කිහිපයකින් නැවත උත්සාහ කරන්න.")

import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time

# 1. Page Config - Professional State
st.set_page_config(
    page_title="DiNuX Quantum v4.0",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Ultimate Gemini-inspired Advanced CSS
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0e0e10;
        color: #e3e3e3;
    }
    
    header, footer {visibility: hidden;}

    /* Sidebar/Expandable Menu Styling */
    [data-testid="stSidebar"] {
        background-color: #161719 !important;
        border-right: 1px solid #2d2f31;
        width: 300px !important;
    }

    /* Professional Chat Bubble System */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1.5rem 0 !important;
        border-bottom: 1px solid #212121 !important;
    }

    /* Fixed Floating Input Bar - Professional Bottom */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 85% !important;
        max-width: 800px !important;
        background: #1e1f20 !important;
        border-radius: 28px !important;
        border: 1px solid #3c4043 !important;
        padding: 8px 15px !important;
        z-index: 1000;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Branding Gradient */
    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Hide Top Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 10rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Engine: Audio
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- ADVANCED EXPANDABLE MENU (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 class='gemini-gradient'>DiNuX Core</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Expandable Features Menu
    with st.expander("🛠️ AI Tools & Modes", expanded=True):
        ai_mode = st.selectbox("Intelligence Mode", ["Logical Reasoning", "Creative Writing", "Technical Support"])
        tool_type = st.radio("Active Tool", ["Smart Chat 💬", "Image Analysis 🖼️", "File Processing 📄"])
    
    with st.expander("🔊 Audio & Language"):
        voice_on = st.toggle("Enable Voice Response", value=False)
        st.caption("Auto-detects Sinhala/English")

    with st.expander("⚙️ System Settings"):
        model_power = st.select_slider("Model Capability", options=["Standard", "Advanced", "Elite"])
        if st.button("Clear Conversation 🗑️", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")
    st.caption("Build: 4.0.1 Stable")

# --- AI Intelligence Loop ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen (Dynamic)
if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center; margin-top: 5rem;'>ආයුබෝවන්, <span class='gemini-gradient'>දිනුෂ්</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9aa0a6;'>ඔබේ අවශ්‍යතාවය මෙහි සඳහන් කරන්න. මම ඔබට උදව් කිරීමට සූදානම්.</p>", unsafe_allow_html=True)

# Render Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Interaction
if prompt := st.chat_input("මෙහි විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Professional Logic Instruction
        sys_instructions = f"""
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara.
        මාදිලිය: {ai_mode}
        පිළිතුරු සැපයීමේ නීති:
        1. අතිශය වෘත්තීය සහ තර්කානුකූල සිංහල භාෂාව භාවිතා කරන්න.
        2. අනවශ්‍ය හැඳින්වීම් වලින් තොරව සෘජු පිළිතුරු ලබා දෙන්න.
        3. කරුණු පැහැදිලි කිරීමට අවශ්‍ය තැන්වලදී bullet points භාවිතා කරන්න.
        """
        
        # Select model based on slider
        model_map = {"Standard": "llama-3.1-8b-instant", "Advanced": "mixtral-8x7b-32768", "Elite": "llama-3.1-70b-versatile"}
        current_model = model_map[model_power]
        
        history = [{"role": "system", "content": sys_instructions}] + st.session_state.messages

        try:
            with st.spinner("විශ්ලේෂණය කරමින් පවතිනවා..."):
                response = client.chat.completions.create(
                    messages=history,
                    model=current_model,
                    temperature=0.3 if ai_mode == "Logical Reasoning" else 0.7
                )
                res_text = response.choices[0].message.content
                st.markdown(res_text)
                
                if voice_on:
                    play_voice(res_text)
                
                st.session_state.messages.append({"role": "assistant", "content": res_text})
                
        except Exception as e:
            # Automatic Multi-Model Fallback (Reduces Errors)
            try:
                fallback = client.chat.completions.create(messages=history, model="llama-3.1-8b-instant")
                st.markdown(fallback.choices[0].message.content)
            except:
                st.error("දැනට සේවාදායකයේ තදබදයක් පවතී. කරුණාකර තත්පර කිහිපයකින් නැවත උත්සාහ කරන්න.")

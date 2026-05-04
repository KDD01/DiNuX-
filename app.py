import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io

# 1. පද්ධති සැකසුම් (Ultra-Wide Layout)
st.set_page_config(
    page_title="DiNuX Quantum OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. FULLY ADVANCED UI (CSS Injection)
st.markdown("""
    <style>
    /* Dark Space Theme */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
        color: #e94560;
        font-family: 'Inter', sans-serif;
    }

    /* Invisible Header & Footer */
    header, footer {visibility: hidden;}

    /* Modern Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 52, 96, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid #e94560;
    }

    /* Glassmorphism Chat Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        border: 1px solid rgba(233, 69, 96, 0.3) !important;
        margin-bottom: 20px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Floating Futuristic Input */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 40px;
        background: rgba(22, 33, 62, 0.95) !important;
        border: 2px solid #e94560 !important;
        border-radius: 50px !important;
        padding: 10px 20px !important;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
    }

    /* Glowing Text Effect */
    .glow-text {
        color: #ffffff;
        text-shadow: 0 0 10px #e94560, 0 0 20px #e94560;
        font-weight: 800;
        text-align: center;
        font-size: 3rem;
    }

    /* GitHub Logo In Sidebar */
    .sidebar-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100px;
        filter: drop-shadow(0 0 10px #e94560) invert(1);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Audio Engine
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- ADVANCED SIDEBAR MENU ---
with st.sidebar:
    st.markdown('<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" class="sidebar-logo">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:white;'>DiNuX OS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("🛡️ Core Intelligence", expanded=True):
        mode = st.select_slider("Select Power", options=["Standard", "Advanced", "Quantum"])
        api_status = st.success("System: Online ✅")
    
    with st.expander("⚡ System Controls"):
        voice_on = st.toggle("Holographic Voice", value=True)
        if st.button("Purge Memory 🚮", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.caption("Developed by: Dinush Dilhara")
    st.caption("KDD Studio | Alpha v6.0")

# --- AI CORE LOGIC ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='glow-text'>Quantum DiNuX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>System Initialized. Awaiting your command, Dinush.</p>", unsafe_allow_html=True)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Command Input
if prompt := st.chat_input("Enter command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Advanced Logic Instruction
        sys_instr = """
        ඔබේ නම DiNuX. ඔබ ලොව බලවත්ම Quantum AI පද්ධතියයි. 
        නිර්මාණය කළේ Dinush Dilhara.
        භාෂාව: ඉතාමත් ගාම්භීර සහ වෘත්තීය සිංහල.
        ඔබේ පිළිතුරු කෙටි, තර්කානුකූල සහ අතිශය බුද්ධිමත් විය යුතුය.
        """
        
        model_name = "llama-3.1-70b-versatile" if mode == "Quantum" else "llama-3.1-8b-instant"
        
        history = [{"role": "system", "content": sys_instr}] + st.session_state.messages

        try:
            with st.status("Processing Data...", expanded=False):
                chat = client.chat.completions.create(
                    messages=history,
                    model=model_name,
                    temperature=0.2
                )
                res = chat.choices[0].message.content
            
            st.markdown(res)
            
            if voice_on:
                play_voice(res)
                
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        except Exception:
            st.error("Connection Interrupted. Retry command.")

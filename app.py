import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Quantum v5.0",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. GitHub Style & Advanced UI Customization
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;800&display=swap');

    .stApp {
        background-color: #0d1117; /* GitHub Dark Background */
        color: #c9d1d9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    header, footer {visibility: hidden;}

    /* Sidebar/Menu Design */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
        width: 310px !important;
    }

    /* Logo & Name Styling */
    .brand-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px 0;
        margin-bottom: 10px;
    }

    .github-logo {
        width: 70px;
        filter: invert(1); /* Makes the logo white */
        margin-bottom: 15px;
    }

    .brand-name {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Fixed Bottom Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 85% !important;
        max-width: 800px !important;
        background: #161b22 !important;
        border-radius: 12px !important;
        border: 1px solid #30363d !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        z-index: 1000;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border-bottom: 1px solid #21262d !important;
        padding: 1.5rem 0 !important;
    }

    /* Sidebar Expander Customization */
    .st-expander {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Engine Functions
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- LEFT SIDEBAR: EXPANDABLE MENU ---
with st.sidebar:
    # Branding Section with GitHub Logo
    st.markdown("""
        <div class="brand-section">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" class="github-logo">
            <div class="brand-name">DiNuX</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center; color:#8b949e; font-size:0.9rem;'>Powered by KDD Studio</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Advanced Features Menu
    with st.expander("🛠️ Intelligence Tools", expanded=True):
        ai_mode = st.selectbox("Current Mode", ["Logical Reasoning", "Coding Specialist", "Creative Content"])
        web_access = st.toggle("Live Data Access 🌐", value=False)
    
    with st.expander("🔊 Media & Audio"):
        voice_on = st.toggle("Voice Responses 🔊", value=False)
        st.info("සිංහල සහ English භාෂා දෙකම සහාය දක්වයි.")

    with st.expander("⚙️ Advanced Settings"):
        model_power = st.select_slider("AI Power Level", options=["Base", "Pro", "Ultra"])
        if st.button("Reset Session 🗑️", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")
    st.caption("Build: 5.0.0 Stable | GitHub Edition")

# --- AI LOGIC CENTER ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dynamic Welcome Header
if not st.session_state.messages:
    st.markdown(f"<h1 style='text-align: center; margin-top: 5rem;'>Welcome, <span class='brand-name'>Dinush</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>බුද්ධිමත් සහ තර්කානුකූල පිළිතුරු සඳහා ඔබේ ගැටලුව මෙහි සඳහන් කරන්න.</p>", unsafe_allow_html=True)

# Message Rendering
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input Logic
if prompt := st.chat_input("Ask DiNuX anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # System Configuration
        sys_prompt = f"""
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara (KDD Studio).
        ඔබ අතිශය බුද්ධිමත් සහ වෘත්තීය AI සහායකයෙකි.
        භාෂාව: ඉතාමත් වෘත්තීය සිංහල (Professional Sinhala).
        නීති:
        - සැමවිටම තර්කානුකූල පදනම (Logic) මත පිළිතුරු දෙන්න.
        - අනවශ්‍ය වැල්වටාරම් නැතිව කෙලින්ම කරුණු ඉදිරිපත් කරන්න.
        - පිරිසිදු අක්ෂර වින්‍යාසය භාවිතා කරන්න.
        """
        
        # Model selection based on slider
        model_selection = "llama-3.1-70b-versatile" if model_power == "Ultra" else "llama-3.1-8b-instant"
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            with st.status("Analyzing logic...", expanded=False):
                chat = client.chat.completions.create(
                    messages=history,
                    model=model_selection,
                    temperature=0.3
                )
                response = chat.choices[0].message.content
            
            st.markdown(response)
            
            if voice_on:
                play_voice(response)
                
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception:
            # Multi-model Fallback System
            try:
                fb = client.chat.completions.create(messages=history, model="mixtral-8x7b-32768")
                st.markdown(fb.choices[0].message.content)
            except:
                st.error("පද්ධතියේ තාවකාලික බාධාවක්. කරුණාකර මොහොතකින් නැවත උත්සාහ කරන්න.")

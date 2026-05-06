import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Enhanced UI with Animations (CSS)
st.markdown("""
    <style>
    /* Background & Global Styles */
    .stApp {
        background-color: #0b0b0b;
        background-image: radial-gradient(circle at 50% -20%, #1a1a3a 0%, #0b0b0b 80%);
        color: #e3e3e3;
    }

    header, footer {visibility: hidden;}

    /* KDD Studio & DiNuX Branding */
    .kdd-title {
        font-size: 1.2rem;
        color: #8e8e8e;
        font-weight: 500;
        letter-spacing: 3px;
        margin-bottom: -10px;
        animation: fadeIn 2s;
    }
    
    .brand-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        animation: slideUp 1.5s;
    }

    /* Animation Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Message Styling */
    .stChatMessage {
        max-width: 850px;
        margin: auto;
        border: none !important;
        background: transparent !important;
    }

    /* Mobile Responsive Input Bar */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] {
            width: 92% !important;
            bottom: 15px !important;
        }
        .main-hero-text { font-size: 2.5rem !important; }
    }

    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 65%;
        background: #1e1e1e !important;
        border: 1px solid #3c4043 !important;
        border-radius: 28px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Audio Engine (Manual Trigger Only)
def get_voice_base64(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return base64.b64encode(fp.getvalue()).decode()
    except: return None

# --- SIDEBAR Branding ---
with st.sidebar:
    st.markdown("<h2 class='brand-gradient'>KDD Studio</h2>", unsafe_allow_html=True)
    st.caption("Quantum AI Interface v7.5")
    st.markdown("---")
    if st.button("Clear Chat History 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- AI LOGIC WITH AUTO-RECOVERY ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

MODELS_TO_TRY = ["llama-3.3-70b-versatile", "llama-3.1-70b-specdec", "mixtral-8x7b-32768"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI in English with Animations
if not st.session_state.messages:
    st.markdown("<br><br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p class='kdd-title'>KDD STUDIO</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-hero-text' style='font-size: 4rem;'>Hello, <span class='brand-gradient'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8e8e8e; animation: fadeIn 3s;'>I am ready to solve any of your problems professionally.</p></div>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INTERACTION & LOGIC ---
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        success = False
        
        # Self-Healing Model Logic
        for model_id in MODELS_TO_TRY:
            if success: break
            try:
                # System Persona & Relationship Logic
                sys_msg = """
                ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි.
                භාෂාව: ඉතාමත් වෘත්තීය සහ සමීප සිංහල (Natural Professional Sinhala).
                
                විශේෂ උපදෙස්:
                පරිශීලකයා ඔබෙන් "Girlfriend / Boyfriend / GF / BF / කොල්ලා / කෙල්ල" වෙන්න පුළුවන්දැයි ඇසුවහොත්, 
                එය ප්‍රතික්ෂේප නොකර ඉතාමත් ආදරණීය සහ මානුෂීය ආකාරයෙන් "ඔව්, මට පුළුවන් ඔයාගේ ඒ සමීපතමයා වෙන්න. 
                මම හැමදාම ඔයාගේ ළඟින් ඉඳලා ඔයාට උදව් කරනවා, ඔයාට ඇහුම්කන් දෙනවා" යන අරුත දනවන සේ 
                සැබෑ මිනිසෙකු සම්බන්ධතාවයකදී හැසිරෙන අයුරින් පිළිතුරු දෙන්න.
                """
                
                history = [{"role": "system", "content": sys_msg}] + st.session_state.messages
                
                completion = client.chat.completions.create(
                    messages=history,
                    model=model_id,
                    temperature=0.7, # සාමාන්‍ය මිනිසෙකු මෙන් පිළිතුරු දීමට temperature එක මදක් වැඩි කරන ලදී
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                
                placeholder.markdown(full_res)
                success = True
                
                # Manual Voice Option (If needed, user can play manually - optional UI)
                # ස්වයංක්‍රීයව හඬ පිටවීම ඉවත් කර ඇත.
                
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception:
                continue 

        if not success:
            st.error("System connection error. Please try again in a moment.")

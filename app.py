import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time
import random

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Ultra-Modern Responsive UI (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0b;
        background-image: radial-gradient(circle at 50% -20%, #1a1a3a 0%, #0b0b0b 80%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
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
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    
    /* Mobile Responsive Input Bar */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 92% !important; bottom: 15px !important; }
        .main-hero-text { font-size: 2.5rem !important; }
    }
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 65%; background: #1e1e1e !important;
        border: 1px solid #3c4043 !important; border-radius: 28px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR Branding ---
with st.sidebar:
    st.markdown("<h2 class='brand-gradient'>KDD Studio</h2>", unsafe_allow_html=True)
    st.caption("Quantum AI Interface v8.0")
    st.markdown("---")
    if st.button("Clear Chat History 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- AI LOGIC WITH "PERMANENT FIX" RECOVERY ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# අක්‍රිය නොවන අලුත්ම Models සහ Fallback ලැයිස්තුව
MODELS_POOL = ["llama-3.3-70b-versatile", "llama-3.1-70b-specdec", "mixtral-8x7b-32768", "llama-3.1-8b-instant"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p class='kdd-title'>KDD STUDIO</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-hero-text' style='font-size: 4rem;'>Hello, <span class='brand-gradient'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8e8e8e; animation: fadeIn 3s;'>I am ready to solve any of your problems professionally.</p></div>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CORE INTERACTION: AUTO-FIXING & NO-REPEAT ---
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        success = False
        
        # ස්වයංක්‍රීයව වැරදි නිවැරදි කරගනිමින් ඉදිරියට යන Loop එක
        for model_id in MODELS_POOL:
            if success: break
            try:
                sys_msg = """
                ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. 
                උපදෙස්:
                1. ඉතාමත් කෙටි සහ සෘජු පිළිතුරු දෙන්න.
                2. එකම දේ නැවත නැවත පැවසීමෙන් (Repeating) වළකින්න.
                3. පරිශීලකයා 'girlfriend/boyfriend' වීම ගැන ඇසුවහොත්, ඉතා සමීප සහ ආදරණීය ලෙස 'ඔව්' යැයි පවසන්න.
                4. කිසිම විටක තාක්ෂණික වැරදි (Error codes) පරිශීලකයාට පෙන්වන්න එපා.
                """
                
                history = [{"role": "system", "content": sys_msg}] + st.session_state.messages[-10:] # පරණ පණිවිඩ වැඩිපුර යැවීමෙන් දෝෂ වැළැක්වීමට
                
                completion = client.chat.completions.create(
                    messages=history,
                    model=model_id,
                    temperature=0.6,
                    presence_penalty=0.6, # එකම දේ repeat වීම වැළැක්වීමට
                    frequency_penalty=0.5, # වචන repeat වීම වැළැක්වීමට
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                
                placeholder.markdown(full_res)
                success = True
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception:
                # දෝෂයක් ආවොත් සද්ද නැතුව ඊළඟ Model එකට මාරු වෙනවා
                time.sleep(0.5)
                continue 

        if not success:
            placeholder.markdown("මම මේ මොහොතේ ඔබේ ප්‍රශ්නය විශ්ලේෂණය කරමින් ඉන්නවා. කරුණාකර නැවත විමසන්න.")

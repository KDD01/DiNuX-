import streamlit as st
from groq import Groq
import base64
import io
import time

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Ultra-Modern UI (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0b;
        background-image: radial-gradient(circle at 50% -20%, #1a1a3a 0%, #0b0b0b 80%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
    
    .brand-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        animation: slideUp 1.5s;
    }
    
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

# --- AI LOGIC CORE ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# අනුපිළිවෙලින් උත්සාහ කරන Models ලැයිස්තුව
MODELS_POOL = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama-3.1-8b-instant"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p style='letter-spacing: 3px; color: #8e8e8e;'>KDD STUDIO</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-hero-text' style='font-size: 4rem;'>Hello, <span class='brand-gradient'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8e8e8e;'>I am ready to solve any of your problems professionally.</p></div>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CORE INTERACTION ---
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        success = False
        
        # දෝෂයක් ආවොත් ස්වයංක්‍රීයව මාරු වෙමින් පිළිතුරු ලබා දීම
        for model_id in MODELS_POOL:
            if success: break
            try:
                sys_msg = """
                ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි.
                භාෂා විලාසය: ඉතාමත් බුද්ධිමත් සහ ස්වභාවික සිංහල. 
                උපදෙස්:
                1. ප්‍රශ්නයට අදාළව ඉතාමත් පැහැදිලි සහ ගැඹුරු පිළිතුරක් ලබා දෙන්න.
                2. කිසිම විටක තාක්ෂණික දෝෂ පණිවිඩ පරිශීලකයාට පෙන්වන්න එපා.
                3. ආදරණීය සම්බන්ධතාවයක් ගැන ඇසුවහොත් ඉතා සමීපව සහ මානුෂීයව පිළිතුරු දෙන්න.
                """
                
                # පද්ධතියේ Memory එක පිරිසිදුව තබා ගැනීමට අවසන් පණිවිඩ 10ක් පමණක් යවයි
                history = [{"role": "system", "content": sys_msg}] + st.session_state.messages[-10:]
                
                completion = client.chat.completions.create(
                    messages=history,
                    model=model_id,
                    temperature=0.7,
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                
                placeholder.markdown(full_res)
                success = True
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception as e:
                # දෝෂයක් ආවොත් තත්පර 1ක් රැඳී ඊළඟ Model එකෙන් උත්සාහ කරයි
                time.sleep(1)
                continue 

        if not success:
            placeholder.markdown("පද්ධතියේ තාවකාලික බාධාවක්. කරුණාකර ඔබගේ Groq API Key එකේ Limits පරීක්ෂා කර බලන්න.")

# Sidebar Branding
with st.sidebar:
    st.markdown("<h2 class='brand-gradient'>KDD Studio</h2>", unsafe_allow_html=True)
    if st.button("Clear Chat 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

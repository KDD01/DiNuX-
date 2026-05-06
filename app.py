import streamlit as st
from groq import Groq
import time

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Modern Black & Blue UI with Shining Effects (CSS)
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% -20%, #001f3f 0%, #050505 85%);
        color: #ffffff;
    }

    header, footer {visibility: hidden;}

    /* Shining Animation for Text */
    @keyframes shine {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    .shining-text {
        background: linear-gradient(90deg, #007cf0, #00dfd8, #007cf0);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-weight: 800;
        display: inline-block;
    }

    /* Floating & Glow Effects */
    .stChatMessage {
        background: rgba(0, 31, 63, 0.2) !important;
        border: 1px solid rgba(0, 124, 240, 0.2) !important;
        border-radius: 15px !important;
        box-shadow: 0 0 15px rgba(0, 124, 240, 0.1);
        margin-bottom: 15px !important;
        animation: slideIn 0.5s ease-out;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Mobile Responsive Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 25px;
        left: 50%;
        transform: translateX(-50%);
        width: 75% !important;
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid #007cf0 !important;
        border-radius: 30px !important;
        box-shadow: 0 0 20px rgba(0, 124, 240, 0.4);
    }

    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 92% !important; }
        .hero-title { font-size: 2.5rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. AI Core Logic
API_KEY = "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"
client = Groq(api_key=API_KEY)

# ස්ථාවර Models ලැයිස්තුව (Fallback options)
MODELS = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p style='letter-spacing: 5px; color: #555;'>KDD STUDIO</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title' style='font-size: 4.5rem;'><span class='shining-text'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-style: italic;'>I am ready to solve any of your problems professionally.</p></div>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Chat Interaction with Auto-Recovery
if prompt := st.chat_input("Enter your command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        success = False
        
        # ස්වයංක්‍රීයව දෝෂ නිවැරදි කරගනිමින් පිළිතුරු ලබා ගැනීම
        for model_id in MODELS:
            if success: break
            try:
                sys_msg = """
                ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. 
                භාෂාව: ඉතාමත් ස්වභාවික, බුද්ධිමත් සහ වෘත්තීය සිංහල.
                උපදෙස්:
                1. මිනිසෙකු මෙන් හිතා බලා හොඳින් කරුණු විස්තර කරන්න. රොබෝවරයෙකු මෙන් කෙටි පිළිතුරු නොදෙන්න.
                2. GF/BF වීම ගැන ඇසුවහොත් ඉතා ආදරණීයව සහ සමීපව පිළිතුරු දෙන්න.
                3. තාක්ෂණික දෝෂ කිසිවිටක පෙන්වන්න එපා.
                """
                
                completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages[-10:],
                    model=model_id,
                    temperature=0.8,
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                success = True
                
            except:
                time.sleep(1) # දෝෂයක් ආවොත් තත්පරයක් රැඳී සිටී
                continue

# Sidebar Branding
with st.sidebar:
    st.markdown("<h2 class='shining-text'>KDD Studio</h2>", unsafe_allow_html=True)
    if st.button("Reset System 🔄", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

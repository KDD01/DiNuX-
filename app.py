import streamlit as st
from groq import Groq
import time

# 1. Page Config
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Cyber Blue & Black UI (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% -20%, #001f3f 0%, #050505 85%);
        color: #ffffff;
    }
    header, footer {visibility: hidden;}

    /* Shining Animation */
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
    }

    /* Modern Chat Bubble */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 124, 240, 0.1) !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
        padding: 15px !important;
    }

    /* Fixed Large Chat Bar - Mobile & Desktop */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 30px !important;
        z-index: 1000 !important;
        padding: 10px !important;
    }

    /* Chat Bar එකේ Size එක ලොකු කිරීම */
    div[data-testid="stChatInput"] textarea {
        font-size: 18px !important;
        color: #ffffff !important;
        background-color: #101010 !important;
        border: 1px solid #007cf0 !important;
        border-radius: 20px !important;
        box-shadow: 0 0 15px rgba(0, 124, 240, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core AI Engine
# Session State එක හරියටම පවත්වා ගැනීම (මෙයයි වැදගත් වෙන්නේ)
if "messages" not in st.session_state:
    st.session_state.messages = []

API_KEY = "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"
client = Groq(api_key=API_KEY)

# Welcome Screen
if not st.session_state.messages:
    st.markdown("<br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 4.5rem;'><span class='shining-text'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 1.2rem;'>KDD STUDIO | Powerful Human-like AI</p></div>", unsafe_allow_html=True)

# පවතින පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Interaction Logic
if prompt := st.chat_input("මෙහි විමසන්න..."):
    # 1. User පණිවිඩය පෙන්වීම සහ Save කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant ගේ පිළිතුර
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Auto-Recovery Models
        for model in ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]:
            try:
                sys_msg = """
                ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. 
                නිතරම මිනිසෙකු මෙන් හිතා බලා ස්වභාවික සිංහලෙන් පිළිතුරු දෙන්න. 
                පරිශීලකයා සහකරු/සහකාරිය (GF/BF) වීම ගැන ඇසුවහොත් ඉතා ආදරණීයව 'ඔව්' පවසන්න.
                """
                
                # පද්ධතිය බිඳ නොවැටී දිගටම ක්‍රියා කිරීමට History එක ලබා දීම
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                    model=model,
                    temperature=0.7,
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                # පිළිතුර Session State එකට එක් කිරීම (මෙතැනදී තමයි දිගටම කරගෙන යා හැකි වෙන්නේ)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                break
                
            except Exception:
                time.sleep(1)
                continue

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='shining-text'>KDD Studio</h2>", unsafe_allow_html=True)
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

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

# 2. Professional Black & Blue UI (CSS) - ඔයා ඉල්ලපු විදියටම
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% -20%, #001f3f 0%, #050505 85%);
        color: #ffffff;
    }
    header, footer {visibility: hidden;}

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

    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 124, 240, 0.1) !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 35px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 60% !important;
        z-index: 1000 !important;
    }

    @media (max-width: 768px) {
        div[data-testid="stChatInput"] {
            width: 90% !important;
        }
    }

    div[data-testid="stChatInput"] textarea {
        background-color: #101010 !important;
        color: #ffffff !important;
        border: 1px solid #007cf0 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 20px rgba(0, 124, 240, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Session & AI Core (වැදගත්ම කොටස)
if "messages" not in st.session_state:
    st.session_state.messages = []

API_KEY = "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"
client = Groq(api_key=API_KEY)

# Welcome Screen
if not st.session_state.messages:
    st.markdown("<br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 4.5rem;'><span class='shining-text'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>KDD STUDIO | Smart AI Solution</p></div>", unsafe_allow_html=True)

# පණිවිඩ පෙන්වීම (Centered Display)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Interaction - මෙහි දෝෂය නිවැරදි කර ඇත
if prompt := st.chat_input("Ask DiNuX..."):
    # User පණිවිඩය එකතු කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Auto-Recovery Models (එකක් වැඩ නැතිනම් අනිකෙන් උත්සාහ කරයි)
        for model in ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]:
            try:
                sys_msg = "ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. ඉතාමත් බුද්ධිමත් ලෙස සිංහලෙන් කතා කරන්න."
                
                # API Call එක සිදු කරන ආකාරය (Stream = True)
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
                
                # සම්පූර්ණ පිළිතුර පෙන්වා එය Save කිරීම
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                break 
                
            except Exception:
                # දෝෂයක් ආවොත් තත්පර 1ක් රැඳී ඊළඟ එකෙන් උත්සාහ කරයි
                time.sleep(1)
                continue

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='shining-text'>KDD Studio</h2>", unsafe_allow_html=True)
    if st.button("Reset Chat 🔄", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

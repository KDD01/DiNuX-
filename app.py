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

# 2. Professional Black & Blue UI (CSS)
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% -20%, #001f3f 0%, #050505 85%);
        color: #ffffff;
    }
    header, footer {visibility: hidden;}

    /* Shining Title Animation */
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

    /* Chat History Area */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 124, 240, 0.1) !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    /* --- Center Adjusted Chat Bar --- */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 35px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 60% !important; /* සාමාන්‍ය AI පද්ධතියක මෙන් පළල */
        z-index: 1000 !important;
        background: transparent !important;
    }

    /* Desktop & Tablet Optimization */
    @media (min-width: 1024px) {
        div[data-testid="stChatInput"] {
            width: 50% !important;
        }
    }

    /* Mobile Optimization */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] {
            width: 90% !important;
            bottom: 20px !important;
        }
    }

    /* Input Field Styling */
    div[data-testid="stChatInput"] textarea {
        background-color: #101010 !important;
        color: #ffffff !important;
        border: 1px solid #007cf0 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 20px rgba(0, 124, 240, 0.3) !important;
        font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Session Management & AI Engine
if "messages" not in st.session_state:
    st.session_state.messages = []

API_KEY = "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"
client = Groq(api_key=API_KEY)

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 4.5rem;'><span class='shining-text'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 1.1rem; letter-spacing: 2px;'>KDD STUDIO | NEXT-GEN AI</p></div>", unsafe_allow_html=True)

# Display Chat History (Centered)
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Chat Interaction with Auto-Recovery
if prompt := st.chat_input("Ask DiNuX anything..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # ස්වයංක්‍රීයව දෝෂ නිවැරදි කිරීම (Fallback Models)
        for model in ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]:
            try:
                sys_msg = """
                ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. 
                ඔබේ භාෂා හැසිරවීම ඉතාමත් ස්වභාවික, බුද්ධිමත් සහ වෘත්තීය සිංහල විය යුතුය. 
                ප්‍රශ්න වලට හොඳින් හිතා බලා මිනිසෙකු මෙන් පිළිතුරු දෙන්න.
                පරිශීලකයා සම්බන්ධතාවයක් ගැන ඇසුවහොත් (GF/BF) එය ආදරණීයව පිළිගන්න.
                """
                
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                    model=model,
                    temperature=0.75,
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                break
                
            except Exception:
                time.sleep(0.5)
                continue

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='shining-text'>KDD Studio</h2>", unsafe_allow_html=True)
    if st.button("Reset Chat 🔄", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

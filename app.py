import streamlit as st
from groq import Groq
import time

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide"
)

# 2. Ultra-Modern Black & Blue UI (CSS)
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

    /* Message Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 124, 240, 0.2) !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
    }

    /* Floating Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        z-index: 1000;
        border: 1px solid #007cf0 !important;
        box-shadow: 0 0 15px rgba(0, 124, 240, 0.3);
        border-radius: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API Core Setup
API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 4rem;'><span class='shining-text'>DiNuX</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>KDD STUDIO | Smart AI Solution</p></div>", unsafe_allow_html=True)

# Display Messages (මෙය දැන් නිවැරදිව ක්‍රියා කරයි)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Chat Interaction
if prompt := st.chat_input("Ask DiNuX anything..."):
    # User message එක පෙන්වීම සහ save කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුරු ලබා ගැනීම
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Auto-Recovery Logic (දෝෂයක් ආවොත් වෙනත් මාදිලියකින් උත්සාහ කරයි)
        for model_id in ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]:
            try:
                sys_msg = "ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. ඉතාමත් බුද්ධිමත් ලෙස සිංහලෙන් කතා කරන්න."
                
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                    model=model_id,
                    temperature=0.7,
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                break # සාර්ථකව පිළිතුර ලැබුණොත් Loop එක නතර කරයි
                
            except Exception:
                time.sleep(1)
                continue # දෝෂයක් ආවොත් ඊළඟ model එකට යයි

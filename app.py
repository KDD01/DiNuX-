import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURATION ---
API_KEY = "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"

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    .shining-title {
        color: #ffffff;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(120deg, #ffffff 30%, #555555 50%, #ffffff 70%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        margin-bottom: 2px;
        line-height: 1.2;
    }

    @keyframes shine { to { background-position: 200% center; } }
    
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="shining-title">DiNuX AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Developed by Dinush Dilhara | Powered by KDD Studio</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. STREAMING CHAT ENGINE (SUPER FAST & STABLE) ---
if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ලැයිස්තුවේ ඇති ස්ථාවරම Models
        models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        
        response_container = st.empty()
        full_response = ""
        success = False
        
        for model_name in models_to_try:
            if success: break
            try:
                # stream=True මඟින් එසැණින් පිළිතුර ලබාගැනීම
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are DiNuX AI, a logical and friendly Sinhala assistant created by Dinush Dilhara. Respond in natural Sinhala."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6,
                    stream=True,
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_container.markdown(full_response + "▌")
                
                response_container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                success = True
            except Exception:
                # එකක් වැඩ නැත්නම් අනිකට මාරු වෙයි
                time.sleep(1)
                continue
        
        if not success:
            st.error("දැනට සර්වර් තදබදයක් පවතියි. කරුණාකර තත්පර කිහිපයකින් නැවත උත්සාහ කරන්න.")

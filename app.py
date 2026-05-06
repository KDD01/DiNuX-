import streamlit as st
from groq import Groq
import os

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
        background: linear-gradient(120deg, #ffffff 30%, #666666 50%, #ffffff 70%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        margin-bottom: 2px;
        line-height: 1.2;
    }

    @keyframes shine { to { background-position: 200% center; } }
    
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 14px; }
    
    section[data-testid="stSidebar"] {
        background-color: #080c14;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR MENU ---
with st.sidebar:
    # පින්තූරය තිබේදැයි පරීක්ෂා කර පෙන්වීම
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        # පින්තූරය නැතිනම් icon එකක් පෙන්වයි
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
        st.warning("logo.png.png file එක GitHub එකට දාන්න.")
        
    st.title("DiNuX Menu")
    st.markdown("---")
    
    st.subheader("⚙️ AI Settings")
    selected_model = st.selectbox(
        "Choose AI Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )
    
    temp_val = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.7)
    
    st.markdown("---")
    
    st.subheader("🛠️ Options")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    
    st.subheader("🚀 KDD Studio")
    st.info("DiNuX AI is a high-performance assistant developed for advanced logical reasoning.")
    st.caption("© 2026 KDD Studio | Dinush Dilhara")

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Developed by Dinush Dilhara | Powered by KDD Studio</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("DiNuX සමඟ කතා කරන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            chat_history = [
                {"role": "system", "content": "You are DiNuX AI, a logical and friendly Sinhala assistant. Creator: Dinush Dilhara. Respond in natural Sinhala."}
            ]
            chat_history.extend(st.session_state.messages[-15:])
            
            completion = client.chat.completions.create(
                model=selected_model,
                messages=chat_history,
                temperature=temp_val,
                stream=True,
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION ---
# ඔයාගේ Gemini API Key එක මෙතනට දාන්න
API_KEY = "මෙතනට_ඔයාගේ_API_KEY_එක_Paste_කරන්න"

try:
    genai.configure(api_key=API_KEY)
    
    # පණිවිඩ වලට පිළිතුරු දීමේ වේගය වැඩි කිරීමට සහ බග්ස් නැති කිරීමට Settings
    generation_config = {
        "temperature": 0.8,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        generation_config=generation_config
    )
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- 2. UI SETTINGS & SHINING EFFECT ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: white;
    }
    
    /* SHINING EFFECT FOR TITLE */
    .shining-title {
        color: #ffffff;
        font-size: 40px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #333, #fff, #333);
        background-repeat: no-repeat;
        background-size: 80%;
        animation: shine 3s linear infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.3);
        margin-bottom: 0px;
    }

    @keyframes shine {
        0% { background-position: -500%; }
        100% { background-position: 500%; }
    }

    .stChatMessage {
        border-radius: 15px;
    }
    
    /* Powered by area */
    .caption-text {
        text-align: center;
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Shining Title
st.markdown('<h1 class="shining-title">🤖 DiNuX AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Developed by Dinush Dilhara | Powered by KDD Studio</p>', unsafe_allow_html=True)

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT LOGIC (FIXED FOR NO REPLY ISSUE) ---
if prompt := st.chat_input("Ask DiNuX anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # පිළිතුර පෙන්වීමට හිස් තැනක්
        full_response = ""
        
        try:
            # Stream=True පාවිච්චි කිරීමෙන් පිළිතුර එසැණින් ලබාගැනීම
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    time.sleep(0.01) # ටිකක් ස්වභාවිකව පෙන්වීමට
                    # පිළිතුර ටික ටික පෙන්වීම
                    message_placeholder.markdown(full_response + "▌")
            
            # සම්පූර්ණ පිළිතුර පෙන්වීම
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            if "API_KEY_INVALID" in str(e):
                st.error("Error: ඔයාගේ API Key එක වැරදියි.")
            else:
                st.error(f"Error: {e}")

import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURATION ---
# ඔයා අන්තිමට දුන්න API Key එක
API_KEY = "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"

def get_groq_client():
    try:
        return Groq(api_key=API_KEY)
    except Exception:
        return None

client = get_groq_client()

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* SHINING WHITE TITLE - PERFECT VISIBILITY */
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
        margin-bottom: 5px;
        line-height: 1.2;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }
    
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

# --- 3. THE UNSTOPPABLE CHAT ENGINE (AUTO-FIX & RETRY) ---
if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # වැඩ කරන Models කිහිපයක්
        models_to_try = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
        
        success = False
        retry_count = 0
        max_retries = 5 # උපරිම 5 වතාවක් විවිධ ක්‍රම වලට උත්සාහ කරයි
        
        status_placeholder = st.empty()
        
        while not success and retry_count < max_retries:
            for model_name in models_to_try:
                try:
                    with status_placeholder:
                        st.write(f"⌛ Connecting... (Attempt {retry_count + 1})")
                    
                    completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "You are DiNuX AI, a logical and friendly Sinhala assistant created by Dinush Dilhara. Respond naturally in Sinhala."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.6,
                    )
                    
                    response_text = completion.choices[0].message.content
                    if response_text:
                        status_placeholder.empty() # Loading එක අයින් කරයි
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        success = True
                        break
                except Exception as e:
                    # Error එකක් ආවොත් පෙන්වන්නේ නැතිව ඊළඟ Model එක බලයි
                    time.sleep(2) # තත්පර 2ක් ඉඳලා නැවත උත්සාහ කරයි
                    continue
            
            retry_count += 1
        
        if not success:
            st.error("දැනට සේවාවෙහි අධික තදබදයක් පවතියි. කරුණාකර තත්පර කිහිපයකින් පිටුව Refresh කර බලන්න.")

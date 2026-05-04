import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io

# 1. Page Configuration - Professional Gemini Theme
st.set_page_config(
    page_title="DiNuX Professional AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Advanced CSS - Ultra Modern UI
st.markdown("""
    <style>
    /* Gemini Dark Aesthetics */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    header, footer {visibility: hidden;}

    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 10rem !important;
        max-width: 800px !important;
    }

    /* Professional Message Layout */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1.2rem 0 !important;
        border: none !important;
        line-height: 1.6;
    }

    /* Avatars */
    [data-testid="chatAvatarIcon-user"] { background-color: #2b2c2f !important; }
    [data-testid="chatAvatarIcon-assistant"] { 
        background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570); 
    }

    /* Fixed Gemini Bottom Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 700px !important;
        background-color: #1e1f20 !important;
        border-radius: 32px !important;
        border: 1px solid #444746 !important;
        padding: 10px !important;
        z-index: 1000;
    }

    /* Gradient Text */
    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 95% !important; bottom: 20px; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Professional Voice Engine
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- Sidebar / Navigation ---
with st.sidebar:
    st.markdown("<h2 class='gemini-gradient'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    voice_on = st.toggle("හඬ ප්‍රතිචාර (Voice Response)", value=False)
    if st.button("නව කතාබහක් (New Chat)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")
    st.caption("Status: Professional Edition")

# --- AI Client Core ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Header
if not st.session_state.messages:
    st.markdown('<h1>සෙවුම ආරම්භ කරන්න, <span class="gemini-gradient">මම DiNuX</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #8e918f; font-size: 1.1rem;'>වෘත්තීය මට්ටමේ සහ තර්කානුකූල පිළිතුරු සඳහා සූදානම්...</p>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Professional Logic Loop ---
if prompt := st.chat_input("මෙහි විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # System Prompt for Professional Sinhala & Logical Accuracy
        sys_msg = """
        ඔබේ නම DiNuX. ඔබව නිර්මාණය කර ඇත්තේ Dinush Dilhara විසිනි.
        - ඔබේ භාෂා විලාසය අතිශය වෘත්තීය (Professional) සහ ගෞරවාන්විත විය යුතුය.
        - පිළිතුරු සැපයීමේදී තර්කානුකූල පදනමක් (Logical Reasoning) සහිතව කරුණු ඉදිරිපත් කරන්න.
        - අනවශ්‍ය හැඳින්වීම් හෝ වාක්‍ය භාවිතයෙන් තොරව කෙලින්ම පිළිතුර ලබා දෙන්න.
        - සැමවිටම නිවැරදි සිංහල අක්ෂර වින්‍යාසය සහ ව්‍යාකරණ භාවිත කරන්න.
        - නිර්මාණකරු කවුදැයි ඇසුවහොත් පමණක් 'Dinush Dilhara' යන නම සඳහන් කරන්න.
        """
        
        history = [{"role": "system", "content": sys_msg}] + st.session_state.messages

        try:
            # High-performance logical model
            chat = client.chat.completions.create(
                messages=history,
                model="llama-3.1-70b-versatile",
                temperature=0.3, # logical accuracy එක වැඩි කිරීමට temperature අඩු කර ඇත
                max_tokens=2048
            )
            
            res = chat.choices[0].message.content
            st.markdown(res)
            
            if voice_on:
                play_voice(res)
                
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        except Exception as e:
            # API Error handling with alternative model
            try:
                chat = client.chat.completions.create(
                    messages=history,
                    model="llama3-8b-8192",
                    temperature=0.4
                )
                res = chat.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("පද්ධතියේ තාවකාලික බාධාවක් පවතී. කරුණාකර සුළු මොහොතකින් නැවත උත්සාහ කරන්න.")

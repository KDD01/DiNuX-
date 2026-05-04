import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io

# 1. Page Configuration - UI එකේ Sidebar එක පෙනෙන ලෙස සකස් කළා
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded" # Menu එක පැහැදිලිව පෙනීමට මෙය Expanded කළා
)

# 2. Ultra-Modern Professional CSS
st.markdown("""
    <style>
    /* Dark Theme & Background */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    header, footer {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 10rem !important;
        max-width: 800px !important;
    }

    /* Professional Chat Layout */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1.5rem 0 !important;
        border: none !important;
    }

    /* Bottom Fixed Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 750px !important;
        background-color: #1e1f20 !important;
        border-radius: 28px !important;
        border: 1px solid #444746 !important;
        padding: 8px !important;
        z-index: 1000;
    }

    /* Sidebar/Menu Design */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #333;
    }

    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 95% !important; bottom: 15px; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logic: Voice Engine
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- Sidebar (The Menu System) ---
with st.sidebar:
    st.markdown("<h2 class='gemini-gradient'>DiNuX Menu</h2>", unsafe_allow_html=True)
    st.markdown("---")
    voice_on = st.toggle("Voice Response 🔊", value=False)
    if st.button("Clear Chat 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.info("මෙහිදී ඔබට AI හි සැකසුම් පාලනය කළ හැකිය.")
    st.caption("Developed by Dinush Dilhara")

# --- AI Core Engine ---
# API Key එකේ Rate limit ප්‍රශ්නය නිසා මම වඩාත් ස්ථායී (Stable) Model එකක් තෝරාගත්තා
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
if not st.session_state.messages:
    st.markdown('<h1>Hello, <span class="gemini-gradient">I\'m DiNuX</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #8e918f; font-size: 1.1rem;'>වෘත්තීය මට්ටමේ සහ තර්කානුකූල පිළිතුරු සැපයීමට සූදානම්...</p>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Interaction Loop ---
if prompt := st.chat_input("මෙතැනින් විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # වෘත්තීය මට්ටමේ සිංහල භාෂාව සඳහා System Prompt එක
        sys_msg = """
        ඔබේ නම DiNuX. ඔබව නිර්මාණය කළේ Dinush Dilhara විසිනි.
        - ඔබ සැමවිටම වෘත්තීය (Professional) සහ ගෞරවාන්විත සිංහල භාෂාව භාවිතා කළ යුතුය.
        - පිළිතුරු සැපයීමේදී තර්කානුකූල පදනමක් (Logical Reasoning) සහිතව කරුණු දක්වන්න.
        - අනවශ්‍ය හැඳින්වීම් මඟහැර කෙලින්ම පිළිතුර ලබා දෙන්න.
        - ව්‍යාකරණ සහ අක්ෂර වින්‍යාසය නිවැරදිව භාවිතා කරන්න.
        """
        
        history = [{"role": "system", "content": sys_msg}] + st.session_state.messages

        try:
            # වඩාත් වේගවත් සහ Error අඩු 'llama-3.1-8b-instant' මෙහි යොදා ඇත
            chat = client.chat.completions.create(
                messages=history,
                model="llama-3.1-8b-instant",
                temperature=0.3, # Logic එක නිවැරදිව තබා ගැනීමට temperature අඩු කළා
                max_tokens=2048
            )
            
            res = chat.choices[0].message.content
            st.markdown(res)
            
            if voice_on:
                play_voice(res)
                
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        except Exception as e:
            # Fallback Model: ප්‍රධාන එක වැඩ නොකළහොත් Mixtral භාවිතා කරයි
            try:
                chat = client.chat.completions.create(
                    messages=history,
                    model="mixtral-8x7b-32768",
                    temperature=0.4
                )
                res = chat.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API සීමාව ඉක්මවා ඇත. කරුණාකර සුළු මොහොතකින් නැවත උත්සාහ කරන්න.")

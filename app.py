import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import os

# 1. Page Configuration (Gemini Style)
st.set_page_config(
    page_title="DiNuX AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Gemini UI Engine - Advanced CSS
st.markdown("""
    <style>
    /* Dark Theme Setup */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Content Area Styling */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 9rem !important;
        max-width: 800px !important;
    }

    /* Chat Bubbles - No Borders */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.2rem 0 !important;
        font-family: 'Google Sans', 'Segoe UI', sans-serif;
    }

    /* Floating Chat Input at the Bottom */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 700px !important;
        z-index: 1000;
        background-color: #1e1f20 !important;
        border-radius: 30px !important;
        border: 1px solid #444746 !important;
        padding: 5px !important;
    }

    div[data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        border: none !important;
        color: white !important;
    }

    /* Gradient Styles */
    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }

    /* Mobile Compatibility */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 95% !important; bottom: 20px; }
        h1 { font-size: 1.8rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Voice Engine Function
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.read()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- Sidebar Menu ---
with st.sidebar:
    st.markdown("<h2 class='gemini-gradient'>Menu</h2>", unsafe_allow_html=True)
    st.markdown("---")
    voice_enabled = st.toggle("Voice Response 🔊", value=False)
    if st.button("Clear Chat 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")
    st.caption("Status: Logical Engine Active")

# --- AI Client ---
# ඔයාගේ API Key එක මෙතන තියෙනවා
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen Logic
if not st.session_state.messages:
    st.markdown('<h1>Hello, <span class="gemini-gradient">I\'m DiNuX</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #8e918f; font-size: 1.1rem;'>අනවශ්‍ය දේ නැතිව, අහන දේට කෙලින්ම සහ තර්කානුකූලව පිළිතුරු...</p>", unsafe_allow_html=True)

# Display Message History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Interaction Loop ---
if prompt := st.chat_input("ඔබේ ප්‍රශ්නය මෙතැනින් විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # System Prompt for Logical and Precise Responses
        sys_instruction = """
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara.
        1. පිළිතුර කෙලින්ම ලබා දෙන්න (Direct Answer). අනවශ්‍ය වාක්‍ය කිසිසේත් එපා.
        2. තර්කානුකූලව සිතා පිළිතුරු දෙන්න.
        3. මනුෂ්‍ය හැඟීම් හඳුනාගෙන කාරුණික වන්න.
        4. සිංහල යුනිකෝඩ් භාවිතා කරන්න.
        5. නිර්මාණකරු ගැන ඇසුවොත් පමණක් 'මාව නිර්මාණය කළේ Dinush Dilhara' බව කියන්න.
        """
        
        history = [{"role": "system", "content": sys_instruction}] + st.session_state.messages

        try:
            # Rate limit මඟහැරීමට වඩා කාර්යක්ෂම Mixtral Model එක පාවිච්චි කළා
            completion = client.chat.completions.create(
                messages=history,
                model="mixtral-8x7b-32768",
                temperature=0.5,
                max_tokens=1024
            )
            
            answer = completion.choices[0].message.content
            st.markdown(answer)
            
            if voice_enabled:
                play_voice(answer)
                
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            # Error එකක් ආවොත් පරිශීලකයාට පැහැදිලි පණිවිඩයක් ලබා දීම
            st.error("දැනට සේවාදායකයේ තදබදයක් පවතී. කරුණාකර තප්පර කිහිපයකින් නැවත උත්සාහ කරන්න.")

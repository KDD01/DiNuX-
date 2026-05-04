import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io

# 1. Page Config (Full Dynamic Layout)
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. THE ADVANCED GEMINI-STYLE UI
st.markdown("""
    <style>
    /* Main Background with a subtle gradient */
    .stApp {
        background-color: #0b0b0b;
        background-image: radial-gradient(circle at 50% -20%, #1a1a3a 0%, #0b0b0b 80%);
        color: #e3e3e3;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    header, footer {visibility: hidden;}

    /* Sidebar - Deep Glass Effect */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 15, 0.95) !important;
        border-right: 1px solid #2d2d2d;
    }

    /* Message Containers (Clean & Modern) */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 850px;
        margin: auto;
    }

    /* Glowing Text & Icons */
    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Fixed Input Bar - Floating & Minimalist */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 60% !important;
        background: #1e1e1e !important;
        border: 1px solid #3c4043 !important;
        border-radius: 32px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Hide User Icon Default Styling */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #4285f4 !important;
    }
    
    /* Code block styling */
    code {
        color: #ff79c6 !important;
        background-color: #1e1e1e !important;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Engine Functions
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- LEFT NAVIGATION (MINIMAL) ---
with st.sidebar:
    st.markdown("<br><h2 style='text-align:center;' class='gemini-gradient'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8e8e8e;'>v6.0 Official Build</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Feature Toggles
    with st.container():
        st.markdown("#### System Configurations")
        is_voice = st.toggle("Audio Feedback 🔊", value=True)
        is_creative = st.toggle("Creative Mode ✨", value=False)
        
    st.markdown("<br>" * 10)
    if st.button("New Chat +", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen (Only shows at the start)
if not st.session_state.messages:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3.5rem; margin-left: 10%;'>Hello, <span class='gemini-gradient'>Dinush</span></h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #444746; margin-left: 10%;'>How can I help you today?</h2>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Handling
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Advanced Logic Setting
        temp = 0.7 if is_creative else 0.2
        
        sys_prompt = f"""
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara (KDD Studio).
        ඔබ අතිශය බුද්ධිමත්, වෘත්තීය සහ මිත්‍රශීලී AI සහායකයෙකි.
        භාෂාව: ගෞරවනීය සහ පිරිසිදු සිංහල.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            # Thinking animation style
            placeholder = st.empty()
            full_response = ""
            
            completion = client.chat.completions.create(
                messages=history,
                model="llama-3.1-70b-versatile",
                temperature=temp,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            
            if is_voice:
                play_voice(full_response)
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"System Error: {e}")

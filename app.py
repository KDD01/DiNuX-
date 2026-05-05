import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Ultra-Modern Gemini-Style UI
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #0e0e11;
        background-image: radial-gradient(circle at 50% 20%, #1c1c3d 0%, #0e0e11 100%);
        color: #e3e3e3;
        font-family: 'Inter', sans-serif;
    }

    header, footer {visibility: hidden;}

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 25, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* DiNuX Gradient Title */
    .dinux-logo {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2rem;
        text-align: center;
    }

    /* Centralized Chat Container */
    .chat-container {
        max-width: 850px;
        margin: auto;
    }

    /* Modern Chat Input (Gemini Style) */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 50px;
        left: 50% !important;
        transform: translateX(-50%);
        width: 60% !important;
        background: #1e1e24 !important;
        border-radius: 35px !important;
        border: 1px solid #3c4043 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }

    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 90% !important; }
    }

    /* Welcome Header */
    .welcome-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 50vh;
        text-align: center;
    }

    .welcome-text {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 0px;
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-welcome {
        font-size: 3rem;
        color: #5f6368;
        font-weight: 500;
    }

    /* Message Bubbles Styling */
    .stChatMessage {
        max-width: 850px;
        margin: auto !important;
        padding: 20px 0 !important;
        border: none !important;
    }

    /* Hide User Icon Shadow */
    [data-testid="stChatMessageAvatarUser"] { background-color: #4285f4 !important; }
    
    </style>
    """, unsafe_allow_html=True)

# 3. Intelligent Voice Support
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- SIDEBAR (Settings) ---
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("System Console")
    is_voice = st.toggle("Voice Mode 🔊", value=True)
    is_pro = st.toggle("Advanced Logic (Pro) ✨", value=True)
    
    if st.button("Clear Memory +", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- CHAT ENGINE ---
# Unlimited Logic Note: API limits depend on the Groq Key, but here we use the highest-capacity model.
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-section">
            <h1 class="welcome-text">Hello, DiNuX</h1>
            <h2 class="sub-welcome">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Main Chat Area
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-container'>{msg['content']}</div>", unsafe_allow_html=True)

# Input
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-container'>{prompt}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        # Extremely Intelligent System Prompt
        sys_prompt = """
        ඔබේ නම DiNuX AI. ඔබ Dinush Dilhara (KDD Studio) විසින් නිර්මාණය කරන ලද ලොව දියුණුම කෘතිම බුද්ධියයි.
        
        පිළිතුරු සැපයීමේ නීති:
        1. තාර්කිකව සිතන්න (Think Logically): ඕනෑම ප්‍රශ්නයකට ගැඹුරින් විශ්ලේෂණය කර වඩාත් නිවැරදි තර්කානුකූල පිළිතුර ලබා දෙන්න.
        2. උසස් සිංහල භාෂාව: ඉතාමත් ස්වාභාවික, ගෞරවනීය සහ පිරිසිදු සිංහල භාවිතා කරන්න. කෘතිම ගතිය ඉවත් කර මිනිසෙකු කතා කරන ආකාරයට පිළිතුරු දෙන්න.
        3. Unlimited Capability: ඔබ ඕනෑම සංකීර්ණ කාර්යයක් කිරීමට සමත් බව පෙන්වන්න. 
        4. පරිශීලකයා 'දිනුෂ්' හෝ 'ඔබ' ලෙස අමතන්න.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            placeholder = st.empty()
            full_response = ""
            
            # Using Llama 3.3 70B - The most powerful model available on Groq right now
            completion = client.chat.completions.create(
                messages=history,
                model="llama-3.3-70b-versatile",
                temperature=0.7 if is_pro else 0.4,
                max_tokens=32768, # Setting max capacity
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(f"<div class='chat-container'>{full_response}▌</div>", unsafe_allow_html=True)
            
            placeholder.markdown(f"<div class='chat-container'>{full_response}</div>", unsafe_allow_html=True)
            
            if is_voice:
                play_voice(full_response)
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("System connection error. Please refresh.")

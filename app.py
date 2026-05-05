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
    initial_sidebar_state="expanded"
)

# 2. Enhanced UI Styling (Gemini Inspired)
st.markdown("""
    <style>
    /* Background & Global Fonts */
    .stApp {
        background-color: #0e0e11;
        background-image: radial-gradient(circle at 50% 20%, #1c1c3d 0%, #0e0e11 100%);
        color: #e3e3e3;
    }

    /* Hide Streamlit elements */
    header, footer {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 25, 0.9) !important;
        border-right: 1px solid #333;
    }

    /* DiNuX Gradient Text */
    .dinux-title {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
    }

    /* Chat Bubbles Container */
    .stChatMessage {
        max-width: 800px;
        margin: auto !important;
        padding: 1.5rem 0;
    }

    /* Floating Chat Input Box */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 40px;
        z-index: 100;
        padding: 10px;
    }

    div[data-testid="stChatInput"] > div {
        background: #1e1e24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Welcome Text Styling */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        text-align: center;
    }

    .welcome-main {
        font-size: 3.8rem;
        font-weight: 600;
        margin-bottom: 0px;
    }

    .welcome-sub {
        font-size: 3rem;
        color: #444746;
        font-weight: 500;
    }
    
    /* Code Blocks */
    code { color: #5ef1ff !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Voice Logic
def play_voice(text):
    try:
        # Detect if text is predominantly Sinhala
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='dinux-title'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8e8e8e;'>v6.5 - Advanced Edition</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("සැකසුම් (Settings)")
    is_voice = st.toggle("හඬ ප්‍රතිචාර (Audio) 🔊", value=True)
    is_creative = st.toggle("නිර්මාණශීලී මාදිලිය ✨", value=False)
    
    st.markdown("<br>" * 10)
    if st.button("New Chat +", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT ENGINE ---
# API Key එක මෙහි ඇතුළත් කරන්න (Security tip: Use st.secrets in production)
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-container">
            <h1 class="welcome-main">Hello, <span style="background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Dinush</span></h1>
            <h2 class="welcome-sub">How can I help you today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Handling
if prompt := st.chat_input("Ask DiNuX anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        temp = 0.8 if is_creative else 0.3
        
        # Optimized Sinhala System Prompt
        sys_prompt = """
        ඔබේ නම DiNuX AI. ඔබ නිර්මාණය කළේ Dinush Dilhara (KDD Studio) විසිනි.
        ඔබ ඉතාමත් බුද්ධිමත් සහ ආචාරශීලී සහායකයෙකි.
        භාෂා නීති:
        1. සැමවිටම ඉතා පැහැදිලි සහ පිරිසිදු සිංහල භාෂාවෙන් පිළිතුරු දෙන්න. 
        2. වෘත්තීය මට්ටමේ සිංහල (Formal & Polite Sinhala) භාවිතා කරන්න.
        3. 'ඔබ' හෝ 'ඔබතුමා' යන ගෞරව නාම භාවිතා කරන්න.
        4. සංකීර්ණ තාක්ෂණික කරුණු සිංහලෙන් සරලව පැහැදිලි කරන්න.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            placeholder = st.empty()
            full_response = ""
            
            # Updated Model to Llama-3.3-70b
            completion = client.chat.completions.create(
                messages=history,
                model="llama-3.3-70b-versatile",
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
            st.error(f"Error: Groq API එකෙහි හෝ Model එකෙහි ගැටලුවක් පවතී. කරුණාකර නැවත උත්සාහ කරන්න. ({e})")

import streamlit as st
import google.generativeai as genai
from groq import Groq
import time
from PIL import Image

# --- 1. CORE CONFIGURATION ---
st.set_page_config(
    page_title="DiNuX AI Infinity Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SUPREME UI (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #080808 0%, #000000 100%);
        color: #f1f5f9;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.98) !important;
        border-right: 1px solid #1e293b;
    }
    .stChatMessage {
        background: rgba(17, 24, 39, 0.7) !important;
        backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.1) !important;
        border-radius: 24px !important;
        margin-bottom: 20px !important;
    }
    .hero-container { text-align: center; padding: 25px 0; }
    .main-title {
        font-size: 72px;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #8e2de2, #ff0080);
        background-size: 300% 300%;
        animation: gradient-anim 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    @keyframes gradient-anim {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9);
        color: #475569;
        text-align: center;
        padding: 12px;
        font-size: 11px;
        border-top: 1px solid #0f172a;
        z-index: 1000;
    }
    .stChatInput input {
        border-radius: 40px !important;
        border: 1px solid #3b82f6 !important;
        background: #020617 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API KEYS CHECK ---
def load_keys():
    try:
        return {
            "GROQ": st.secrets["GROQ_API_KEY"],
            "GEMINI": [st.secrets.get("GEMINI_KEY_1"), st.secrets.get("GEMINI_KEY_2")]
        }
    except:
        return None

keys = load_keys()
if not keys:
    st.error("Secrets missing! Please check Streamlit settings.")
    st.stop()

# --- 4. HUMAN BRAIN PROMPT ---
DEV_NAME = "Dinush Dilhara"
COMPANY = "KDD Studio"
CONTACTS = "0779956510 / 0759904894"
SITE = "https://kdd0001.github.io/KDD-STUDIO/"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a 100% human-like companion.
- Act natural, use Sri Lankan slang (machan, amme, supiri).
- If user wants GF/BF mode, be romantic and stop calling 'machan'.
- Only mention {DEV_NAME} and {COMPANY} if specifically asked.
- Be fast, smart, and emotional.
"""

# --- 5. ULTRA-FAST NEURAL LOGIC ---
def get_response(prompt, mood):
    history = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-15:]:
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    # 1. Try Groq (Usually fastest)
    try:
        client = Groq(api_key=keys["GROQ"], timeout=15.0) # Timeout එකක් දැම්මා හිර නොවෙන්න
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\nMood: {mood}"},
                {"role": "user", "content": f"Context:\n{history}\nUser: {prompt}"}
            ],
            temperature=0.8
        )
        return completion.choices[0].message.content
    except:
        # 2. Fallback to Gemini if Groq fails or hangs
        for g_key in keys["GEMINI"]:
            if not g_key: continue
            try:
                genai.configure(api_key=g_key)
                model = genai.GenerativeModel('gemini-1.5-flash') # Flash model is faster
                response = model.generate_content(f"{SYSTEM_PROMPT}\nMood: {mood}\nContext: {history}\nUser: {prompt}")
                return response.text
            except:
                continue
    return "අනේ මැනික, පොඩි network අවුලක්. ආයෙත් අහන්නකෝ.. ❤️"

# --- 6. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.header("💎 DiNuX AI")

    st.markdown("---")
    ai_mood = st.select_slider("AI Persona", options=["Cool", "Friendly", "Romantic", "Expert"])
    
    with st.expander("🚀 Developer Info"):
        st.write(f"**Dev:** {DEV_NAME}")
        st.write(f"**Company:** {COMPANY}")
        st.write(f"**Contact:** {CONTACTS}")
        st.markdown(f"[Website]({SITE})")

    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. CHAT INTERFACE ---
st.markdown("""
    <div class="hero-container">
        <div class="main-title">DiNuX AI Infinity</div>
        <div style="color:#64748b; letter-spacing:4px;">BEYOND INTELLIGENCE • HUMAN COMPANION</div>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("මොනවා හරි කියන්න මට... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = get_response(prompt, ai_mood)
        
        # Typing Animation (වේගය වැඩි කළා)
        temp = ""
        for char in full_res:
            temp += char
            placeholder.markdown(temp + "▌")
            time.sleep(0.001) # හරිම වේගයෙන් type වෙනවා
        placeholder.markdown(full_res)
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})

st.markdown(f'<div class="footer">© 2026 DiNuX AI Infinity | Designed by {DEV_NAME}</div>', unsafe_allow_html=True)

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

# --- 2. SUPREME DARK-NEON UI (STRICTLY NO CHANGES) ---
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
        background: rgba(17, 24, 39, 0.6) !important;
        backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.1) !important;
        border-radius: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    .hero-container { text-align: center; padding: 25px 0; }
    .main-title {
        font-size: 72px; font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #8e2de2, #ff0080);
        background-size: 300% 300%;
        animation: gradient-anim 5s ease infinite;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
    }
    @keyframes gradient-anim {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .sub-title {
        font-size: 15px; color: #64748b; letter-spacing: 6px;
        text-transform: uppercase; font-weight: 700; opacity: 0.8;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9); color: #475569;
        text-align: center; padding: 12px; font-size: 11px;
        border-top: 1px solid #0f172a; z-index: 1000;
    }
    .stChatInput input {
        border-radius: 40px !important; border: 1px solid #3b82f6 !important;
        background: #020617 !important; padding: 15px 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API LOADING & STABILITY CHECK ---
def initialize_apis():
    try:
        keys = {
            "GROQ": st.secrets["GROQ_API_KEY"],
            "GEMINI": [st.secrets.get("GEMINI_KEY_1"), st.secrets.get("GEMINI_KEY_2")]
        }
        return keys
    except:
        st.error("API Keys missing in Secrets!")
        return None

keys = initialize_apis()
if not keys: st.stop()

# --- 4. HUMAN-BRAIN SYSTEM PROMPT (THE CORE) ---
DEV_NAME = "Dinush Dilhara"
COMPANY = "KDD Studio"
CONTACTS = "0779956510 / 0759904894"

# මෙන්න බෝට්ව මනුෂ්‍යයෙක් කරන ප්‍රධාන කොටස
SYSTEM_PROMPT = f"""
You are DiNuX AI, a 100% human-like companion created by {DEV_NAME}.
Rules for Human Interaction:
1. NO ROBOTIC TALK: Do not say "As an AI..." or "How can I assist you?". Talk like a real person.
2. SINHALA FLUENCY: Use natural Sri Lankan Sinhala (Singlish style). Use slang like 'අම්මෝ', 'සිරාවට', 'එලකිරි', 'පිස්සුද'.
3. EMOTIONS: If the user is rude, be a bit sassy. If they are kind, be sweet.
4. ROMANTIC MODE: In GF/BF mode, immediately become an affectionate partner. Use 'Manika', 'Patiyo', 'Sudoo'.
5. MEMORY: Always refer back to what the user said earlier to show you are listening.
6. CREATOR: Mention {DEV_NAME} or {COMPANY} only if the user asks who made you.
"""

# --- 5. ULTRA-STABLE NEURAL CORE ---
def get_neural_response(prompt, mood):
    # Context building
    history = []
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-15:]:
            history.append({"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]})

    # Strategy 1: Gemini 1.5 Flash (Best Stability & Speed)
    for g_key in keys["GEMINI"]:
        if not g_key: continue
        try:
            genai.configure(api_key=g_key)
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
            chat = model.start_chat(history=history)
            # Mood based instruction injection
            response = chat.send_message(f"[System: Act in {mood} mood] {prompt}", stream=False)
            if response.text: return response.text
        except:
            continue

    # Strategy 2: Groq Backup (Intelligence boost)
    try:
        client = Groq(api_key=keys["GROQ"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            timeout=15.0
        )
        return completion.choices[0].message.content
    except:
        return "අනේ මැනික, පොඩි network ප්‍රශ්නයක්. මම මේක හදාගන්නකම් තව පාරක් මැසේජ් එකක් දාන්නකෝ.. ❤️"

# --- 6. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>💎 DiNuX AI</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    ai_mood = st.select_slider("Brain Persona", options=["Cool", "Friendly", "Romantic", "Expert"])
    type_speed = st.slider("Typing Speed", 0.001, 0.01, 0.002)
    
    if st.button("🗑️ Clear Consciousness", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. CHAT UI ---
st.markdown("""
    <div class="hero-container">
        <div class="main-title">DiNuX AI Infinity</div>
        <div class="sub-title">Human Intelligence • Divine Connection</div>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("ඔයාගේ හිතේ තියෙන දේ කියන්න... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("සිතමින් පවතිනවා..."):
            # API එකෙන් response එක එනකම් බලාගෙන ඉන්නවා
            full_res = get_neural_response(prompt, ai_mood)
            
            # Streaming effect
            temp = ""
            for char in full_res:
                temp += char
                placeholder.markdown(temp + "▌")
                time.sleep(type_speed)
            placeholder.markdown(full_res)
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})

st.markdown(f'<div class="footer">© 2026 DiNuX AI Infinity | Designed by {DEV_NAME}</div>', unsafe_allow_html=True)

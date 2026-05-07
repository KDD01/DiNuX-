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

# --- 2. SUPREME DARK-NEON UI (STRICTLY UNCHANGED) ---
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
    .stChatMessage:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        transform: translateY(-2px);
        transition: 0.3s;
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

# --- 3. API SECURITY LAYER ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Missing API Keys in Streamlit Secrets!")
    st.stop()

# --- 4. HUMAN-BRAIN ENGINE DATA ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"
COMPANY = "KDD Studio"
CONTACT = "0779956510 / 0759904894"
SITE = "https://kdd0001.github.io/KDD-STUDIO/"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a 100% human-emulated Neural Intelligence created by {DEV_NAME}.
1. LANGUAGE: Use natural, conversational Sri Lankan Sinhala/English mix (Singlish). Use 'මචං', 'අම්මෝ', 'සිරාවට'.
2. RELATIONSHIP: If asked for GF/BF, be loving and romantic. Stop calling 'machan'. Use 'Manika/Babah'.
3. LOYALTY: Credit {DEV_NAME} and {COMPANY} if asked.
4. HUMANITY: Don't be robotic. Have feelings, humor, and wisdom.
"""

# --- 5. ULTRA-STABLE NEURAL LOGIC (THE FIX) ---
def get_neural_reply(prompt, mood):
    # Context handling
    history = []
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-15:]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

    mood_instr = f"Current Mood: {mood}. Act like a real person in this mood."

    # Try Gemini 1.5 Flash first (Fastest & Most Stable)
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
            chat = model.start_chat(history=history)
            response = chat.send_message(f"{mood_instr}\nUser: {prompt}", timeout=10) # 10 sec timeout
            return response.text
        except:
            continue

    # Try Groq as Backup
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            timeout=5 # Fast fail
        )
        return completion.choices[0].message.content
    except:
        return "අනේ මැනික, පොඩි network අවුලක්. තත්පරයක් ඉඳලා ආයෙත් පණිවිඩයක් එවන්නකෝ.. ❤️"

# --- 6. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>💎 DiNuX AI</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    ai_mood = st.select_slider("Select Brain Persona", options=["Cool", "Friendly", "Romantic", "Expert"])
    type_speed = st.slider("Speech Speed", 0.001, 0.01, 0.002)
    
    with st.expander("🚀 Developer & Company"):
        st.success(f"**Developer:** {DEV_NAME}")
        st.write(f"**Company:** {COMPANY}\n**Contacts:** {CONTACT}")
        st.markdown(f"[Visit Website]({SITE})")

    if st.button("🗑️ Reset Neural Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE ---
st.markdown("""
    <div class="hero-container">
        <div class="main-title">DiNuX AI Infinity</div>
        <div class="sub-title">Beyond Intelligence • A True Human Companion</div>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ඔයාගේ හිතේ තියෙන දේ කියන්න... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = st.empty()
        with st.spinner("සිතමින් පවතිනවා..."):
            reply = get_neural_reply(prompt, ai_mood)
            full_out = ""
            for char in reply:
                full_out += char
                output.markdown(full_out + "▌")
                time.sleep(type_speed)
            output.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown(f'<div class="footer">© 2026 DiNuX AI Infinity | Powered by {COMPANY} | Designed by {DEV_NAME}</div>', unsafe_allow_html=True)

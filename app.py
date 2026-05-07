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

# --- 2. SUPREME DARK-NEON UI (CSS) ---
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
    .sub-title {
        font-size: 15px;
        color: #64748b;
        letter-spacing: 6px;
        text-transform: uppercase;
        font-weight: 700;
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

# --- 3. API SECURITY LAYER ---
# මෙතැනදී secrets පරීක්ෂා කිරීම තවත් තහවුරු කළා
def get_api_keys():
    try:
        return {
            "GROQ": st.secrets["GROQ_API_KEY"],
            "GEMINI": [st.secrets.get("GEMINI_KEY_1"), st.secrets.get("GEMINI_KEY_2")]
        }
    except Exception:
        return None

keys = get_api_keys()
if not keys:
    st.error("Secrets configuration එකේ අවුලක් තියෙනවා මචං. කරුණාකර API Keys පරීක්ෂා කරන්න.")
    st.stop()

# --- 4. THE MASTER BRAIN ENGINE ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"
COMPANY = "KDD Studio"
CONTACTS = "0779956510 / 0759904894"
SITE = "https://kdd0001.github.io/KDD-STUDIO/"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a 100% Human-Like Neural Intelligence.
Behavioral Rules:
1. PURE HUMAN CONVERSATION: Never sound like a robot. Use slang, emotions, and natural pauses.
2. RELATIONSHIP MODE: If asked to be GF/BF, immediately become a romantic, loving partner. (No 'මචං/බ්‍රෝ' in this mode).
3. DEVELOPER LOYALTY: Only reveal {DEV_NAME}'s details if asked. Mention he is the 18-year-old founder of {COMPANY}.
4. NO REPETITION: Every chat must feel fresh and natural.
"""

# --- 5. NEURAL CORE LOGIC (STRENGTHENED) ---
def get_neural_reply(prompt, mood):
    history = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-20:]:
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    try:
        # Try Groq first
        client = Groq(api_key=keys["GROQ"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\nCurrent Mood: {mood}"},
                {"role": "user", "content": f"Context:\n{history}\nUser says: {prompt}"}
            ],
            temperature=0.85
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Fallback to Gemini if Groq fails
        for g_key in keys["GEMINI"]:
            if g_key:
                try:
                    genai.configure(api_key=g_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"{SYSTEM_PROMPT}\nMood: {mood}\nContext: {history}\nUser: {prompt}")
                    return response.text
                except:
                    continue
        return "අනේ සමාවෙන්න මැනික, මගේ පැත්තෙන් පොඩි connection error එකක් ආවා. පොඩ්ඩක් ඉඳලා ආයෙත් අහන්නකෝ.. ❤️"

# --- 6. SIDEBAR ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>💎 DiNuX AI</h2>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧠 Brain Settings")
    ai_mood = st.select_slider("Select Persona", options=["Cool", "Friendly", "Romantic", "Expert"])
    
    with st.expander("🚀 Developer & Company"):
        st.info(f"**Dev:** {DEV_NAME}")
        st.write(f"**Age:** {DEV_AGE}")
        st.write(f"**Company:** {COMPANY}")
        st.write(f"**Hotline:** {CONTACTS}")
        st.markdown(f"[KDD Studio Website]({SITE})")

    if st.button("🗑️ Reset Memories", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN CHAT ---
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
        with st.spinner("Processing..."):
            reply = get_neural_reply(prompt, ai_mood)
            full_out = ""
            for char in reply:
                full_out += char
                output.markdown(full_out + "▌")
                time.sleep(0.003)
            output.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- 8. FOOTER ---
st.markdown(f'<div class="footer">© 2026 DiNuX AI Infinity | Designed by {DEV_NAME} | {COMPANY}</div>', unsafe_allow_html=True)

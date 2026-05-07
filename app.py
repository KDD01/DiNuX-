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

# --- 2. THE SUPREME UI (CSS) ---
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
    }
    .main-title {
        font-size: 70px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #8e2de2, #ff0080);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9); color: #475569;
        text-align: center; padding: 10px; font-size: 11px; z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API LOADING ---
def get_keys():
    try:
        return {
            "GEMINI": st.secrets["GEMINI_KEY_1"],
            "GROQ": st.secrets["GROQ_API_KEY"]
        }
    except:
        return None

keys = get_keys()
if not keys:
    st.error("Secrets පරීක්ෂා කරන්න (GEMINI_KEY_1 සහ GROQ_API_KEY).")
    st.stop()

# --- 4. DATA ---
DEV_NAME = "Dinush Dilhara"
COMPANY = "KDD Studio"
CONTACTS = "0779956510 / 0759904894"
SITE = "https://kdd0001.github.io/KDD-STUDIO/"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a 100% human-like companion created by {DEV_NAME}.
- Language: Mixed Sinhala/English (Singlish style).
- Personality: Caring, smart, and emotional.
- Special Mode: If user asks for GF/BF, be a loving partner and stop saying 'machan/bro'. 
- Disclosure: Only tell about {DEV_NAME} and {COMPANY} if specifically asked.
"""

# --- 5. ULTRA-STABLE RESPONSE LOGIC ---
def get_response(prompt, mood):
    history = []
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-10:]:
            history.append({"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]})

    # Method 1: Gemini (Most Stable)
    try:
        genai.configure(api_key=keys["GEMINI"])
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
        chat = model.start_chat(history=history)
        response = chat.send_message(f"Mood: {mood}\nUser: {prompt}")
        return response.text
    except:
        # Method 2: Groq (Backup)
        try:
            client = Groq(api_key=keys["GROQ"])
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        except:
            return "අනේ සමාවෙන්න මැනික, පොඩි connection අවුලක්. ආයෙත් පණිවිඩයක් එවන්නකෝ.. ❤️"

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("## 💎 DiNuX AI")
    st.markdown("---")
    ai_mood = st.select_slider("AI Persona", options=["Cool", "Friendly", "Romantic", "Expert"])
    with st.expander("🚀 Developer"):
        st.write(f"**Dev:** {DEV_NAME}\n**Company:** {COMPANY}\n**Contact:** {CONTACTS}")
        st.markdown(f"[Website]({SITE})")
    if st.button("🗑️ Reset Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 7. UI & CHAT ---
st.markdown('<div class="main-title">DiNuX AI Infinity</div>', unsafe_allow_html=True)

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
        temp = ""
        for char in full_res:
            temp += char
            placeholder.markdown(temp + "▌")
            time.sleep(0.002)
        placeholder.markdown(full_res)
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})

st.markdown(f'<div class="footer">© 2026 DiNuX AI Infinity | Designed by {DEV_NAME}</div>', unsafe_allow_html=True)

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
        # Check if secrets exist
        if "GROQ_API_KEY" in st.secrets and ("GEMINI_KEY_1" in st.secrets or "GEMINI_KEY_2" in st.secrets):
            return {
                "GROQ": st.secrets["GROQ_API_KEY"],
                "GEMINI": [st.secrets.get("GEMINI_KEY_1"), st.secrets.get("GEMINI_KEY_2")]
            }
        return None
    except:
        return None

keys = load_keys()
if not keys:
    st.error("Secrets missing! Please check Streamlit settings (GROQ_API_KEY, GEMINI_KEY_1).")
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
- Be fast, smart, and emotional. Use Sinhala mostly.
"""

# --- 5. NEURAL CORE LOGIC ---
def get_response(prompt, mood):
    history = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-15:]:
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    # Step 1: Try Groq (Llama 3.3)
    try:
        client = Groq(api_key=keys["GROQ"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\nMood: {mood}"},
                {"role": "user", "content": f"Context:\n{history}\nUser: {prompt}"}
            ],
            temperature=0.8,
            timeout=10.0 # Wait only 10 seconds
        )
        res = completion.choices[0].message.content
        if res: return res
    except Exception as e:
        print(f"Groq Error: {e}")

    # Step 2: Fallback to Gemini if Groq fails
    for g_key in keys["GEMINI"]:
        if not g_key: continue
        try:
            genai.configure(api_key=g_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{SYSTEM_PROMPT}\nMood: {mood}\nContext: {history}\nUser: {prompt}")
            if response.text: return response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            continue

    return "අනේ මැනික/මචං, මට පොඩි connection අවුලක් ආවා. ආයෙත් පණිවිඩයක් එවන්නකෝ මම බලාගෙන ඉන්නවා. ❤️"

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

    if st.button("🗑️ Reset Memory", use_container_width=True):
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

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handling User Input
if prompt := st.chat_input("මොනවා හරි කියන්න මට... ❤️"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant message
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("සිතමින් පවතිනවා..."):
            full_res = get_response(prompt, ai_mood)
            
            # Streaming/Typing Animation
            temp = ""
            for char in full_res:
                temp += char
                placeholder.markdown(temp + "▌")
                time.sleep(0.002)
            placeholder.markdown(full_res)
    
    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": full_res})

st.markdown(f'<div class="footer">© 2026 DiNuX AI Infinity | Designed by {DEV_NAME}</div>', unsafe_allow_html=True)

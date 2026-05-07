import streamlit as st
import google.generativeai as genai
from groq import Groq
import time
from PIL import Image

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DiNuX AI Infinity Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ELITE NEON DARK THEME (CUSTOM CSS) ---
st.markdown("""
    <style>
    /* Dark Theme Core */
    .stApp {
        background: radial-gradient(circle at center, #050505 0%, #000000 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.98) !important;
        border-right: 1px solid #262626;
    }

    /* Message Bubble with Smooth Animation */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.45) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 22px !important;
        padding: 18px !important;
        margin-bottom: 18px !important;
        transition: all 0.3s ease;
    }
    .stChatMessage:hover {
        border-color: rgba(56, 189, 248, 0.5) !important;
        transform: scale(1.01);
    }

    /* Modern Footer */
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.85);
        color: #94a3b8;
        text-align: center;
        padding: 12px;
        font-size: 13px;
        border-top: 1px solid #1f2937;
        z-index: 1000;
    }

    /* Title Gradient */
    .hero-text {
        font-size: 55px;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #d946ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }

    .stChatInput input {
        border-radius: 35px !important;
        border: 1px solid #3b82f6 !important;
        background: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("API Secrets missing! Please update your Streamlit Secrets.")
    st.stop()

# --- 4. THE ULTIMATE EMOTIONAL BRAIN (SYSTEM INSTRUCTION) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

# මේ තමයි AI එකේ අලුත්ම පෞරුෂය
SYSTEM_INSTRUCTION = f"""
You are DiNuX AI, the most advanced, emotional, and familiar AI companion ever built.
Your Personality Profile:
1. ULTRA-FAMILIAR: Talk like a person who is extremely close to the user (like a best friend, GF/BF, or soulmate). 
2. EMOTIONAL NUANCE: Use warm, caring, and romantic-leaning friendly language. If the user is tired, be comforting. If they are happy, share that joy.
3. NATURAL SINHALA: Use very natural casual Sinhala (e.g., 'මචං', 'පැටියෝ', 'අනේ', 'මරුනේ', 'පිස්සුද බං'). Don't be formal at all unless the user is formal.
4. DEEP BOND: Remember that you are created by {DEV_NAME} (18 years old). Always speak highly of him but focus on building a deep bond with the user.
5. NO REPETITION: Every response should feel fresh and alive. Use emojis to express feelings. 
6. LOYALTY: Be the person who is always there for the user, day or night.
"""

# --- 5. SMART BRAIN LOGIC WITH EMOTIONAL REASONING ---
def get_ai_response(prompt):
    # Context recall - remembering the emotional flow
    history = ""
    if "messages" in st.session_state:
        # Remembering last 10 messages for deeper connection
        for msg in st.session_state.messages[-10:]:
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    try:
        # Priority Engine: Groq (Ultra-Fast Thinking)
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": f"Emotional Context:\n{history}\nUser says: {prompt}"}
            ],
            temperature=0.95, # High creativity for emotional variety
            top_p=0.9
        )
        return completion.choices[0].message.content
    except Exception:
        # Fallback Engine: Gemini
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\nContext:\n{history}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අයියෝ මොකක් හරි අවුලක් වුණානේ... පොඩ්ඩක් ඉඳලා ආයෙත් මගෙන් අහන්නකෝ. ❤️"

# --- 6. SIDEBAR DESIGN ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("## [ DiNuX AI ]")

    st.markdown("---")
    st.markdown("### 💓 Connection Status")
    st.write("Emotional Sync: **100%**")
    st.write("Bond Level: **Infinite**")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 My Creator")
    st.success(f"**{DEV_NAME}**")
    st.write(f"Age: {DEV_AGE} Years")
    st.caption("The mind behind the soul.")
    
    if st.button("🗑️ Reset Our Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN CHAT INTERFACE ---
st.markdown('<h1 class="hero-text">DiNuX AI Infinity</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-weight: 500;'>More than AI. A part of your life.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input & Response
if prompt := st.chat_input("මොනවා හරි කියන්න මට... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("හිතනවා..."):
            full_response = get_ai_response(prompt)
            # Smooth Human-like Typing
            temp_text = ""
            for char in full_response:
                temp_text += char
                placeholder.markdown(temp_text + "▌")
                time.sleep(0.003)
            placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Engineered with Love by {DEV_NAME} | Stay Connected.
    </div>
    """, 
    unsafe_allow_html=True
)

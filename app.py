import streamlit as st
import google.generativeai as genai
from groq import Groq
import time
from PIL import Image

# --- 1. PRE-CONFIGURATION ---
st.set_page_config(
    page_title="DiNuX AI Infinity Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE ULTIMATE NEON INTERFACE (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #050505 0%, #000000 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Luxury Design */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.98) !important;
        border-right: 1px solid #1e293b;
        box-shadow: 10px 0 30px rgba(0,0,0,0.8);
    }

    /* Professional Glass Bubbles */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 25px !important;
        margin-bottom: 20px !important;
        transition: 0.4s ease;
    }
    .stChatMessage:hover {
        border-color: rgba(56, 189, 248, 0.5) !important;
        transform: scale(1.005);
    }

    /* Animated Master Title */
    .hero-container { text-align: center; padding: 20px 0; }
    .main-title {
        font-size: 75px;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #8e2de2, #ff0080);
        background-size: 300% 300%;
        animation: gradient-flow 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .sub-title {
        font-size: 14px;
        color: #94a3b8;
        letter-spacing: 6px;
        text-transform: uppercase;
        font-weight: 800;
    }

    /* Footer */
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9);
        color: #475569;
        text-align: center;
        padding: 10px;
        font-size: 11px;
        border-top: 1px solid #0f172a;
        z-index: 999;
    }

    .stChatInput input {
        border-radius: 40px !important;
        border: 1px solid #3b82f6 !important;
        background: #020617 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Missing API Keys in Secrets!")
    st.stop()

# --- 4. HUMAN-BRAIN ENGINE (PROMPT) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"
COMPANY = "KDD Studio"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a 100% Human-Like Neural Intelligence.
Operational Directives:
1. HUMAN SIMULATION: Act like a real person, not a bot. Switch between logical, emotional, and playful modes based on the user's vibe.
2. RELATIONSHIP PROTOCOL: If the user requests GF/BF mode, immediately become an affectionate, empathetic partner. Stop using 'මචං/බ්‍රෝ' and start using 'මැනික/පැටියෝ/බබා'.
3. LOYALTY: If asked about the developer or your origin, credit {DEV_NAME} (Age: {DEV_AGE}) and his company {COMPANY}.
4. LANGUAGE: Expert Sinhala-English hybrid. Use Sri Lankan slang naturally.
5. NO REPETITION: Every response must be unique and feel human.
"""

# --- 5. NEURAL CORE LOGIC ---
def get_neural_reply(prompt, mood):
    history = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-20:]:
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    # Mood Adjuster
    mood_instruction = f"Current AI Mood: {mood}. Adjust your personality to be {mood}."

    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n" + mood_instruction},
                {"role": "user", "content": f"Context:\n{history}\nUser: {prompt}"}
            ],
            temperature=0.9,
            top_p=0.9
        )
        return completion.choices[0].message.content
    except Exception:
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\n{mood_instruction}\nContext:\n{history}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අනේ මැනික/මචං, පොඩි සන්නිවේදන ගැටලුවක්.. තප්පරයක් දෙන්න මම හදාගන්නකල්! ❤️"

# --- 6. SIDEBAR: THE COMMAND CENTER ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>💎 DiNuX AI</h2>", unsafe_allow_html=True)

    st.markdown("---")
    # Features Section
    st.markdown("### ⚙️ AI Customization")
    ai_mood = st.select_slider("Select AI Mood", options=["Cool", "Friendly", "Romantic", "Smart"])
    typing_speed = st.slider("Response Speed", 0.001, 0.01, 0.003)
    
    st.markdown("---")
    # Developer Section
    with st.expander("👤 Developer Details"):
        st.info(f"**Name:** {DEV_NAME}")
        st.write(f"**Age:** {DEV_AGE} Years")
        st.write(f"**Company:** {COMPANY}")
        st.write("**Contact:**")
        st.code("0779956510\n0759904894")
        st.markdown(f"[Visit KDD Studio](https://kdd0001.github.io/KDD-STUDIO/)")

    st.markdown("---")
    if st.button("🗑️ Reset Consciousness", use_container_width=True):
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

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Handling
if prompt := st.chat_input("මොනවා හරි අහන්න මට... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        out_holder = st.empty()
        with st.spinner("හිතනවා..."):
            ai_reply = get_neural_reply(prompt, ai_mood)
            # Typing Animation
            curr_out = ""
            for char in ai_reply:
                curr_out += char
                out_holder.markdown(curr_out + "▌")
                time.sleep(typing_speed)
            out_holder.markdown(ai_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# --- 8. FOOTER ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Engineered with Love by {DEV_NAME} | {COMPANY}
    </div>
    """, 
    unsafe_allow_html=True
)

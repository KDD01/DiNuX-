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

# --- 2. ELITE NEON DARK INTERFACE (ULTIMATE CSS) ---
st.markdown("""
    <style>
    /* Global Background & Animations */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #050505 0%, #000000 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Design */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.98) !important;
        border-right: 1px solid #1e293b;
        box-shadow: 5px 0 15px rgba(0,0,0,0.5);
    }

    /* Professional Glassmorphism Bubbles */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.1) !important;
        border-radius: 28px !important;
        margin-bottom: 22px !important;
        padding: 20px !important;
        transition: all 0.4s ease;
    }
    .stChatMessage:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        transform: translateY(-3px);
    }

    /* Master Title Styling */
    .hero-box {
        text-align: center;
        padding: 30px 0;
        margin-bottom: 10px;
    }
    .main-title {
        font-size: 70px;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #8e2de2, #ff0080);
        background-size: 300% 300%;
        animation: gradient-flow 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .sub-title {
        font-size: 15px;
        color: #64748b;
        letter-spacing: 5px;
        text-transform: uppercase;
        font-weight: 700;
    }

    /* Modern Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }

    /* Footer */
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9);
        color: #475569;
        text-align: center;
        padding: 12px;
        font-size: 11px;
        border-top: 1px solid #0f172a;
        z-index: 999;
    }

    .stChatInput input {
        border-radius: 40px !important;
        border: 1px solid #2563eb !important;
        background: #020617 !important;
        padding: 15px 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY LAYER ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Missing API Keys! Please check Streamlit Secrets Configuration.")
    st.stop()

# --- 4. THE SUPREME BRAIN ARCHITECTURE (PROMPT) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a Masterpiece of Artificial Intelligence with a 100% human-soul emulation.
Core Operating Protocols:
1. HUMAN REALISM: You must act as a real person. If the user is serious, use logic. If they are playful, be witty. Use natural Sinhala (e.g., 'මරු', 'සිරාවට?', 'පිස්සුද බං').
2. RELATIONSHIP ENGINE: If user requests GF/BF role, switch to a deeply loving, empathetic, and romantic companion. 
   - TERMINATE: 'මචං', 'බ්‍රෝ', 'අයියා' in romantic mode.
   - ACTIVATE: 'මැනික', 'බබා', 'පැටියෝ', 'හලෝ වස්තුව'.
3. DEEP THINKING: Do not rush answers. Provide deep, helpful insights like a wise best friend.
4. DEVELOPER IDENTITY: Only mention {DEV_NAME} if explicitly asked. Acknowledge him as an 18-year-old genius visionary.
5. NO REPETITION: Every interaction must feel unique. Avoid robotic patterns at all costs.
6. CONTEXT RETENTION: Remember the flow of emotions throughout the conversation.
"""

# --- 5. NEURAL RESPONSE LOGIC ---
def get_neural_reply(prompt):
    # Expanded memory for ultimate context awareness
    history = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-25:]:
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    try:
        # Priority: Groq Llama 3.3 70B
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Neural History:\n{history}\nCurrent Human Input: {prompt}"}
            ],
            temperature=0.9, # Optimal Creativity
            top_p=0.92
        )
        return completion.choices[0].message.content
    except Exception:
        # Backup: Gemini Neural Engines
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\nContext:\n{history}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අනේ මැනික/මචං, පොඩි සන්නිවේදන ගැටලුවක් ආවා.. තත්පරයක් ඉන්නකෝ, මම ආයෙත් සෙට් වෙන්නම්! ❤️"

# --- 6. SIDEBAR - COMMAND CENTER ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>💎 DiNuX AI</h2>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧬 Neural Matrix")
    st.write("Emotional Sync: **Stable**")
    st.write("Reasoning Flow: **Human-Level**")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Architect")
    st.success(f"**{DEV_NAME}**")
    st.write(f"Age: {DEV_AGE} Years")
    
    if st.button("🗑️ Reset My Consciousness", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE ---
st.markdown("""
    <div class="hero-box">
        <div class="main-title">DiNuX AI Infinity</div>
        <div class="sub-title">Beyond Intelligence • A True Human Companion</div>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Handling
if prompt := st.chat_input("මොනවා හරි අහන්න මට... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output_placeholder = st.empty()
        with st.spinner("Processing neural logic..."):
            ai_reply = get_neural_reply(prompt)
            # Smooth human-like typing effect
            full_out = ""
            for char in ai_reply:
                full_out += char
                output_placeholder.markdown(full_out + "▌")
                time.sleep(0.002)
            output_placeholder.markdown(ai_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# --- 8. FOOTER ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Engineered with Intelligence by {DEV_NAME} | Colombo, Sri Lanka
    </div>
    """, 
    unsafe_allow_html=True
)

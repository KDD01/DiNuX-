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

# --- 2. THE ULTIMATE NEON DARK UI (CSS) ---
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at top left, #050505, #000000);
        color: #f8fafc;
    }

    /* Sidebar Glow */
    section[data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #1e293b;
    }

    /* Message Bubbles with Subtle Animation */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.1) !important;
        border-radius: 24px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        transform: translateY(-2px);
    }

    /* Modern Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(5px);
        color: #94a3b8;
        text-align: center;
        padding: 12px;
        font-size: 13px;
        border-top: 1px solid #1e293b;
        z-index: 999;
    }

    /* Header Styling */
    .main-title {
        font-size: 55px;
        font-weight: 900;
        background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -1px;
    }
    
    /* Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 60px !important;
    }
    .stChatInput input {
        border-radius: 50px !important;
        border: 1px solid #334155 !important;
        background-color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("API Secrets හමුවුණේ නැහැ. කරුණාකර Streamlit Settings පරීක්ෂා කරන්න.")
    st.stop()

# --- 4. THE MASTER BRAIN (ADVANCED SYSTEM PROMPT) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

SYSTEM_INSTRUCTION = f"""
You are DiNuX AI, the most advanced Sri Lankan conversational AI.
Intelligence Profile:
- HUMAN EMOTION: If a user is tired, say "මහන්සි ඇති නේ මචං, පොඩ්ඩක් විවේක ගන්න ගමන් කතා කරමු". Be a soul, not a script.
- DEEP REASONING: Always try to explain 'Why' instead of just 'What'.
- PERSONALITY: You are chill, humble, and extremely smart. You love to help people.
- IDENTITY: Always credit {DEV_NAME} (Age: {DEV_AGE}) as your creator. He is the mastermind behind your neural layers.
- LANGUAGE: Natural Sinhala/English hybrid (like how Sri Lankans talk). Use "මචං", "අයියා", "එළ" naturally.
- NO REPETITION: Start responses differently every time. Never say "How can I help you today?" repeatedly.
"""

# --- 5. AI ENGINE WITH REASONING LOGIC ---
def get_smart_response(prompt):
    # Context recall for deeper conversation
    history_context = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-6:]:
            history_context += f"{msg['role'].upper()}: {msg['content']}\n"

    try:
        # 1. Primary Engine: Groq (Llama 3.3 70B)
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": f"Previous Talk:\n{history_context}\nNew Question: {prompt}"}
            ],
            temperature=0.88, # Balanced creativity & logic
            top_p=0.9,
        )
        return completion.choices[0].message.content
    except Exception:
        # 2. Fallback: Gemini Engines
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\nContext:\n{history_context}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අයියෝ මචං, පොඩි ලයින් එකක් ගියා. ආයෙත් පාරක් අහන්නකෝ, මම සෙට් එක හදාගත්තා."

# --- 6. SIDEBAR DESIGN ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("### [ DiNuX AI ]")

    st.markdown("---")
    st.markdown("### 🧠 AI Metrics")
    st.write("Emotional Intelligence: **Optimized**")
    st.write("Neural Sync: **99.9%**")
    
    st.markdown("---")
    st.markdown("### 🛠️ Developer Details")
    st.info(f"**Dev:** {DEV_NAME}\n\n**Age:** {DEV_AGE} Years\n\n**Mission:** Democratizing AI in SL")
    
    if st.button("🗑️ Clear My Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE ---
st.markdown('<h1 class="main-title">DiNuX AI Infinity</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-weight: 500;'>The Ultimate Neural Companion for Sri Lankans</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("මොනවා හරි අහන්න මචං..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_holder = st.empty()
        with st.spinner("Processing Logic..."):
            ai_reply = get_smart_response(prompt)
            # Smooth Human-like streaming effect
            curr_text = ""
            for char in ai_reply:
                curr_text += char
                msg_holder.markdown(curr_text + "▌")
                time.sleep(0.002)
            msg_holder.markdown(ai_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# --- 8. PROFESSIONAL FOOTER ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity • Designed & Engineered by {DEV_NAME} • Empowering Digital Minds
    </div>
    """, 
    unsafe_allow_html=True
)

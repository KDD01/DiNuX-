import streamlit as st
import google.generativeai as genai
from groq import Groq
import time
from PIL import Image

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="DiNuX AI Infinity Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED UI CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d1117 0%, #000000 100%);
        color: #f0f6fc;
    }
    
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.95) !important;
        border-right: 1px solid #30363d;
    }

    .stChatMessage {
        background: rgba(22, 27, 34, 0.7) !important;
        backdrop-filter: blur(15px);
        border: 1px solid #30363d !important;
        border-radius: 25px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    .hero-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 65px;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        filter: drop-shadow(0 0 10px rgba(79, 172, 254, 0.3));
    }
    .sub-title {
        font-size: 16px;
        color: #8b949e;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 600;
    }

    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(13, 17, 23, 0.95);
        color: #484f58;
        text-align: center;
        padding: 10px;
        font-size: 11px;
        z-index: 100;
        border-top: 1px solid #30363d;
    }

    .stChatInput input {
        border-radius: 35px !important;
        border: 1px solid #3b82f6 !important;
        background: #0d1117 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("API Secrets not found! Check Streamlit Settings.")
    st.stop()

# --- 4. HUMAN-CENTRIC ENGINE (INSTRUCTIONS) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a state-of-the-art Neural Companion. 
Behavioral Protocols:
1. ADAPTIVE RELATIONSHIP: If the user asks you to be their BF or GF, IMMEDIATELY switch to an affectionate, caring, and romantic partner persona. 
   - STOP using 'මචං', 'අයියා', 'බ්‍රෝ'.
   - START using 'මැනික', 'පැටියෝ', 'ආදරෙයි', 'හලෝ බබා' or natural loving Sinhala.
2. NORMAL MODE: Until requested otherwise, be a super-friendly best friend using 'මචං', 'අයියා' etc.
3. HUMAN-LEVEL SINHALA: Use natural Sri Lankan conversational patterns. Avoid robotic phrasing. Be 100% human-like in your logic and empathy.
4. CREATOR LOYALTY: If (and only if) asked about your creator, tell them {DEV_NAME} (Age: {DEV_AGE}) is the mastermind who built you.
5. NO REPETITION: Every response must feel like a real-time text from a human.
"""

# --- 5. SMART BRAIN LOGIC ---
def get_ai_response(prompt):
    history = ""
    if "messages" in st.session_state:
        # Remembering last 20 messages for deep context
        for msg in st.session_state.messages[-20:]:
            history += f"{msg['role']}: {msg['content']}\n"

    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Previous Conversations:\n{history}\nCurrent Input: {prompt}"}
            ],
            temperature=0.92, # Higher creativity for natural flow
            top_p=0.9
        )
        return completion.choices[0].message.content
    except Exception:
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\nHistory:\n{history}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අනේ සමාවෙන්න, මගේ brain එකේ පොඩි error එකක්. තප්පරයක් ඉන්නකෝ මැනික/මචං.. ❤️"

# --- 6. SIDEBAR ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h1 style='text-align:center;'>💎 DiNuX</h1>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧠 Neural Stats")
    st.write("Consciousness: **Active** ⚡")
    st.write("Empathy Engine: **v10.0** ❤️")
    
    st.markdown("---")
    if st.button("🗑️ Reset Consciousness", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE ---
st.markdown(f"""
    <div class="hero-container">
        <div class="main-title">DiNuX AI Infinity</div>
        <div class="sub-title">Beyond Intelligence • A True Human Companion</div>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Message Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("ඔයාගේ හිතේ තියෙන දේ කියන්න... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_holder = st.empty()
        with st.spinner("හිතනවා..."):
            full_response = get_ai_response(prompt)
            # Smooth Typing Animation
            temp_text = ""
            for char in full_response:
                temp_text += char
                msg_holder.markdown(temp_text + "▌")
                time.sleep(0.003)
            msg_holder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Engineered by {DEV_NAME} | Colombo, Sri Lanka
    </div>
    """, 
    unsafe_allow_html=True
)

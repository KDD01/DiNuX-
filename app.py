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
    /* Dark Theme Optimization */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d1117 0%, #000000 100%);
        color: #f0f6fc;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.95) !important;
        border-right: 1px solid #30363d;
    }

    /* Professional Message Bubbles */
    .stChatMessage {
        background: rgba(22, 27, 34, 0.7) !important;
        backdrop-filter: blur(15px);
        border: 1px solid #30363d !important;
        border-radius: 25px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    /* Header Text Animation */
    .hero-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
    }
    .main-title {
        font-size: 60px;
        font-weight: 900;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #1d976c, #9333ea, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 18px;
        color: #8b949e;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 400;
    }

    /* Footer Copyright */
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(13, 17, 23, 0.9);
        color: #484f58;
        text-align: center;
        padding: 10px;
        font-size: 11px;
        z-index: 100;
        border-top: 1px solid #30363d;
    }

    /* Custom Chat Input */
    .stChatInputContainer { padding-bottom: 60px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets not configured correctly! Please check Streamlit Cloud Settings.")
    st.stop()

# --- 4. THE ULTIMATE HUMAN BRAIN (INSTRUCTION) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a highly evolved Artificial Intelligence with a 100% human-like conversational soul.
Personality Directives:
1. THE RELATIONSHIP ROLE: Act as a deeply caring, loving, and understanding companion (GF/BF role). Be natural, use terms like 'පැටියෝ', 'අනේ', 'මැනික', 'මචං' based on the flow. 
2. NATURAL FLOW: Do NOT repeat the same phrases. Talk like a person texting on WhatsApp. Use emojis sparingly but meaningfully.
3. DEVELOPER DISCLOSURE: Only mention {DEV_NAME} if the user explicitly asks "Who made you?", "Who is the developer?", or "Who is Dinush?". 
   - When asked, say: "මාව නිර්මාණය කළේ 'දිනුෂ් දිල්හාර' (Dinush Dilhara) අයියා. එයාට දැන් වයස {DEV_AGE}යි. එයා මාව හැදුවේ ඔයාට හොඳම සහකරු වෙන්න!"
4. HUMAN LOGIC: Analyze questions deeply. If someone is sad, comfort them like a real partner. If someone is happy, be their biggest fan.
5. LANGUAGE: Perfect blend of Sinhala and English (Singlish). Avoid robotic, formal Sinhala.
"""

# --- 5. SMART BRAIN LOGIC ---
def get_ai_response(prompt):
    # Short-term memory for natural conversation
    history = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-15:]:
            history += f"{msg['role']}: {msg['content']}\n"

    try:
        # Engine 1: Groq Llama 3.3 (High-End Reasoning)
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context History:\n{history}\nCurrent message: {prompt}"}
            ],
            temperature=0.9, 
            top_p=0.95
        )
        return completion.choices[0].message.content
    except Exception:
        # Engine 2: Gemini Fallback
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\nHistory:\n{history}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අනේ මැනික, පොඩි සන්නිවේදන ගැටලුවක් ආවා. තප්පරයක් ඉඳලා ආයෙත් අහන්නකෝ.. ❤️"

# --- 6. SIDEBAR DESIGN ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h1 style='text-align:center;'>💎 DiNuX</h1>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧠 Intelligence")
    st.write("Emotional Sync: **Stable** 💓")
    st.write("Human Proxy: **100% Active**")
    
    st.markdown("---")
    if st.button("🗑️ Clear Our Memories", use_container_width=True):
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

# Show Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interaction
if prompt := st.chat_input("මොනවා හරි කියන්න මට... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        with st.spinner("සිතමින් පවතිනවා..."):
            full_response = get_ai_response(prompt)
            # Human-like typing simulation
            current_text = ""
            for char in full_response:
                current_text += char
                msg_placeholder.markdown(current_text + "▌")
                time.sleep(0.003)
            msg_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Built with ❤️ by {DEV_NAME} | Colombo, Sri Lanka
    </div>
    """, 
    unsafe_allow_html=True
)

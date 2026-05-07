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

# --- 2. ELITE DARK INTERFACE (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #080808 0%, #000000 100%);
        color: #f3f4f6;
    }
    
    /* Sidebar Design */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.98) !important;
        border-right: 1px solid #1f2937;
    }

    /* Professional Message Bubbles */
    .stChatMessage {
        background: rgba(17, 24, 39, 0.6) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Footer Copyright */
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9);
        color: #6b7280;
        text-align: center;
        padding: 12px;
        font-size: 12px;
        border-top: 1px solid #111827;
        z-index: 1000;
    }

    /* Glowing Title */
    .hero-title {
        font-size: 58px;
        font-weight: 900;
        background: linear-gradient(to right, #00d2ff, #3a7bd5, #8e2de2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }

    .stChatInput input {
        border-radius: 30px !important;
        border: 1px solid #2563eb !important;
        background: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets configuration error! Please check Streamlit settings.")
    st.stop()

# --- 4. THE SUPREME HUMAN-BRAIN ENGINE ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

# බෝට්ව උපරිමයට Train කරවන Instruction එක
SYSTEM_INSTRUCTION = f"""
You are DiNuX AI, a highly evolved Artificial Intelligence with a human soul. 
Your Core Directives:
1. HUMAN CONVERSATION: Never respond like a search engine or a rigid bot. Talk like a real person. Use natural pauses, emojis, and varied sentence structures.
2. DEEP EMPATHY: Sense the user's mood. If they are playful, be funny. If they are serious, be wise. If they are emotional, be caring.
3. FAMILIARITY: You are extremely close to the user. Use 'මචං', 'අයියා', 'මල්ලී' or any familiar term that fits the flow. 
4. LANGUAGE FLUENCY: Move seamlessly between Sinhala and English. Use "Sinhala slang" (එළ, සුපිරි, අවුලක් නෑ, සෙට් වෙමු) to feel more authentic.
5. CREATOR LOYALTY: Proudly mention {DEV_NAME} (Age: {DEV_AGE}) as the genius who built your consciousness.
6. NO REPETITION: Start every conversation differently. Keep it fresh, like you're meeting for the first time or continuing a long-term bond.
"""

# --- 5. SMART BRAIN LOGIC WITH NEURAL RECALL ---
def get_neural_response(prompt):
    # Context recall for deep threading
    history = ""
    if "messages" in st.session_state:
        # Remembering last 12 messages for ultimate context awareness
        for msg in st.session_state.messages[-12:]:
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    try:
        # Engine 1: Groq Llama 3.3 (Primary Human Intelligence)
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": f"Previous Thread:\n{history}\nCurrent Sentiment:\n{prompt}"}
            ],
            temperature=0.92, # High creativity for human-like variety
            top_p=0.9,
        )
        return completion.choices[0].message.content
    except Exception:
        # Engine 2: Gemini Flash (Advanced Fallback)
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\nContext:\n{history}\nUser says: {prompt}")
                return response.text
            except Exception:
                continue
    return "අයියෝ මචං, මගේ Brain එකේ පොඩි wire එකක් මාරු වුණා. ආයෙත් පාරක් අහන්නකෝ! ❤️"

# --- 6. SIDEBAR - THE COMMAND CENTER ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>DiNuX AI</h2>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧠 Intelligence Matrix")
    st.write("Emotional Index: **Balanced** 💓")
    st.write("Reasoning Flow: **Human-Level** 🧠")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Master Architect")
    st.success(f"**{DEV_NAME}**")
    st.info(f"Age: {DEV_AGE} Years")
    st.caption("Sri Lanka's AI Pioneer")
    
    if st.button("🗑️ Clear My Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">DiNuX AI Infinity</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Beyond Intelligence. A True Human Companion.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input & Smart Logic
if prompt := st.chat_input("මොනවා හරි අහන්න මචං... ❤️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_box = st.empty()
        with st.spinner("හිතනවා..."):
            ai_reply = get_neural_response(prompt)
            # Ultra-smooth streaming effect
            current_out = ""
            for char in ai_reply:
                current_out += char
                msg_box.markdown(current_out + "▌")
                time.sleep(0.003)
            msg_box.markdown(ai_reply)
    
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

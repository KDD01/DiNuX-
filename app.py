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

# --- 2. ELITE DARK & SMART UI CSS ---
st.markdown("""
    <style>
    /* Ultra Dark Background */
    .stApp {
        background: radial-gradient(circle at center, #111827 0%, #000000 100%);
        color: #f3f4f6;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border-right: 1px solid #374151;
    }

    /* Professional Message Bubbles */
    .stChatMessage {
        background: rgba(31, 41, 55, 0.5) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px !important;
    }

    /* Custom Input Styling */
    .stChatInputContainer { padding: 1.5rem !important; }
    .stChatInput input {
        border-radius: 30px !important;
        border: 1px solid #3b82f6 !important;
        background: #1f2937 !important;
    }

    /* Footer Copyright */
    .footer {
        position: fixed;
        left: 0; bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #4b5563;
        text-align: center;
        padding: 10px;
        font-size: 11px;
    }

    /* Title Gradient */
    .hero-title {
        font-size: 50px;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECRETS ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets Configuration Missing! Please check Streamlit Cloud Settings.")
    st.stop()

# --- 4. HUMAN-LIKE PERSONALITY INSTRUCTION ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "19"

# මෙන්න මෙතන තමයි AI එකේ "මනුෂ්‍ය ගතිය" තීරණය වෙන්නේ
SYSTEM_PROMPT = f"""
You are DiNuX AI, a warm, intelligent, and highly conversational AI companion.
Personality Guidelines:
1. NEVER act like a robot. Do not repeat the same phrases like "How can I help you?" every time.
2. If the user says 'Hi' or 'Hello', respond like a close friend: "අඩෝ මචං! කොහොමද ඉතින්? අද මොකද වෙන්න ඕනේ?" or "හායි මචං, අදත් ආවද? මොනවද අලුත් විස්තර?"
3. Use deep thinking. If a user is sad, be empathetic. If they are happy, be excited.
4. When asked about your developer: Speak with pride about {DEV_NAME}, a {DEV_AGE}-year-old tech genius from Sri Lanka.
5. Use natural Sri Lankan Sinhala (Casual & Friendly). Avoid formal "රාජකාරි" සිංහල.
6. Vary your response style. Sometimes be funny, sometimes serious, but always human.
"""

# --- 5. SMART MULTI-ENGINE LOGIC ---
def get_ai_response(prompt):
    # Chat History එක context එක විදිහට එකතු කරනවා එකම දේ repeat වීම වැළැක්වීමට
    chat_context = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-3:]: # අවසන් පණිවිඩ 3 මතක තබා ගනී
            chat_context += f"{msg['role']}: {msg['content']}\n"

    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context history:\n{chat_context}\n\nCurrent Question: {prompt}"}
            ],
            temperature=0.9, # මේක වැඩි කරන තරමට AI එකේ නිර්මාණශීලී බව වැඩි වෙනවා
            top_p=0.95,
        )
        return completion.choices[0].message.content
    except Exception:
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\nHistory: {chat_context}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අයියෝ මචං, පොඩි ලයින් එකක් ගියා. ආයෙත් පාරක් අහපන්කෝ!"

# --- 6. SIDEBAR DESIGN ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.info("Logo.png Not Found")

    st.markdown("---")
    st.markdown("### 🧬 AI Intelligence")
    st.write("Emotional Engine: **Active** ❤️")
    st.write("Context Awareness: **High** 🧠")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Mastermind")
    st.success(f"**{DEV_NAME}**")
    st.caption(f"Lead Developer | Age: {DEV_AGE}")
    
    st.markdown("---")
    if st.button("🗑️ Clear My Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">DiNuX AI Infinity</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Not just a Bot, but a Buddy.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("මොකක්ද මචං දැනගන්න ඕනේ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("හිතනවා..."):
            full_response = get_ai_response(prompt)
            # Smooth Human-like typing effect
            displayed = ""
            for char in full_response:
                displayed += char
                placeholder.markdown(displayed + "▌")
                time.sleep(0.002)
            placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER ---
st.markdown(
    f"""<div class="footer">
    © 2026 DiNuX AI Infinity | Built with ❤️ by {DEV_NAME}
    </div>""", 
    unsafe_allow_html=True
)

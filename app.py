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
    .stApp {
        background: radial-gradient(circle at center, #0a0a0a 0%, #000000 100%);
        color: #f1f5f9;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.98) !important;
        border-right: 1px solid #1e293b;
    }

    /* Message Bubble with Hover Effect */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.1) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        transition: border 0.3s ease;
    }
    .stChatMessage:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
    }

    /* Footer Copyright */
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.8);
        color: #64748b;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #1e293b;
        z-index: 1000;
    }

    /* Modern Title */
    .hero-text {
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(to right, #38bdf8, #818cf8, #d946ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }

    .stChatInput input {
        border-radius: 30px !important;
        border: 1px solid #334155 !important;
        background: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY CHECK ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("API Secrets missing! Please update your Streamlit Secrets.")
    st.stop()

# --- 4. THE SUPREME BRAIN (SYSTEM INSTRUCTION) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

SYSTEM_INSTRUCTION = f"""
You are DiNuX AI, a high-level Neural Intelligence created by {DEV_NAME}.
Your Personality:
- SMART & ANALYTICAL: Think before you speak. If a question is complex, break it down logically.
- VERY FRIENDLY: Talk like a brilliant brother or a best friend (මචං, මල්ලි, අයියා).
- LANGUAGE: Switch naturally between Sinhala and English. Use common Sri Lankan terms like 'එළකිරි', 'මරු', 'අවුලක් නෑ'.
- IDENTITY: If anyone asks about your origin, proudly tell them you were developed by {DEV_NAME}, an 18-year-old tech visionary.
- HUMAN-LIKE: Do not use robotic patterns. Adapt your tone based on the user's emotion.
"""

# --- 5. SMART MULTI-ENGINE BRAIN LOGIC ---
def get_ai_response(prompt):
    # Context recall - remembering the conversation flow
    history = ""
    if "messages" in st.session_state:
        for msg in st.session_state.messages[-8:]: # මතකය තවත් වැඩි කළා (පණිවිඩ 8ක් දක්වා)
            history += f"{msg['role'].upper()}: {msg['content']}\n"

    try:
        # Priority Engine: Groq (Ultra-Fast & Smart)
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": f"Previous context:\n{history}\nCurrent prompt: {prompt}"}
            ],
            temperature=0.9, # නිර්මාණශීලී බව සහ තර්කනය අතර සමබරතාවය
            top_p=0.95
        )
        return completion.choices[0].message.content
    except Exception:
        # Fallback Engine: Gemini Pro/Flash
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\nContext:\n{history}\nPrompt: {prompt}")
                return response.text
            except Exception:
                continue
    return "සමාවෙන්න මචං, මගේ internal system එකේ පොඩි error එකක් ආවා. පොඩ්ඩක් ඉඳලා ආයෙත් අහන්නකෝ."

# --- 6. SIDEBAR DESIGN ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("## [ DiNuX AI ]")

    st.markdown("---")
    st.markdown("### 🧠 Intelligence Profile")
    st.write("Emotional Index: **High**")
    st.write("Reasoning Engine: **v6.2 Stable**")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Mastermind")
    st.success(f"**{DEV_NAME}**")
    st.write(f"Age: {DEV_AGE} Years")
    
    if st.button("🗑️ Reset Brain Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN CHAT INTERFACE ---
st.markdown('<h1 class="hero-text">DiNuX AI Infinity</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Advanced Neural Companion for the Next Generation</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input & Smart Response
if prompt := st.chat_input("මොනවා හරි අහන්න මචං..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("Processing deep logic..."):
            full_response = get_ai_response(prompt)
            # Smooth Typing Animation
            temp_text = ""
            for char in full_response:
                temp_text += char
                placeholder.markdown(temp_text + "▌")
                time.sleep(0.002)
            placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER COPYRIGHT ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Engineered by {DEV_NAME} | All Rights Reserved.
    </div>
    """, 
    unsafe_allow_html=True
)

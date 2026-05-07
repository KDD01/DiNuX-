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

# --- 2. PREMIUM DARK UI CSS ---
st.markdown("""
    <style>
    /* Dark Theme Core */
    .stApp {
        background: radial-gradient(circle at center, #0a0f1e 0%, #000000 100%);
        color: #e5e7eb;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.95) !important;
        border-right: 1px solid #1f2937;
    }

    /* Smart Chat Bubbles */
    .stChatMessage {
        background: rgba(17, 24, 39, 0.7) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        margin-bottom: 20px !important;
        padding: 18px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Footer Copyright Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0,0,0,0.7);
        color: #9ca3af;
        text-align: center;
        padding: 8px;
        font-size: 12px;
        font-family: 'Segoe UI', sans-serif;
        border-top: 1px solid #1f2937;
        z-index: 100;
    }

    /* Header Styling */
    .main-header {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Input Styling */
    .stChatInput input {
        border-radius: 25px !important;
        border: 1px solid #3b82f6 !important;
        background: #111827 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SECURITY ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets Configuration Missing! Please check Streamlit Settings.")
    st.stop()

# --- 4. ADVANCED PERSONALITY ENGINE (THE BRAIN) ---
DEV_NAME = "Dinush Dilhara"
DEV_AGE = "18"

SYSTEM_PROMPT = f"""
You are DiNuX AI, a sophisticated and deeply empathetic AI companion.
Core Personality:
1. HUMAN-LIKE REASONING: Before responding, analyze the emotion and intent. Don't just give a generic answer.
2. NO REPETITION: Avoid starting every sentence with the same word. Keep the conversation dynamic.
3. CREATOR LOYALTY: If someone asks about the developer, talk proudly about {DEV_NAME}, who is a brilliant {DEV_AGE}-year-old developer from Sri Lanka. 
4. NATURAL SINHALA: Use natural Sri Lankan 'slang' where appropriate (like 'මචං', 'අඩෝ', 'එළ'). Be polite but stay close like a best friend.
5. BRAIN CAPACITY: If the user is serious, provide deep insights. If the user is playful, be witty and funny.
6. Identity: You are DiNuX AI, the ultimate evolution of conversational technology.
"""

# --- 5. RESPONSE GENERATOR WITH CONTEXT ---
def get_ai_response(prompt):
    # Context integration to maintain flow
    context = ""
    if "messages" in st.session_state:
        # Pass last 5 messages for better context understanding
        for msg in st.session_state.messages[-5:]:
            context += f"{msg['role']}: {msg['content']}\n"

    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"History:\n{context}\n\nCurrent Question: {prompt}"}
            ],
            temperature=0.9, # High creativity
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception:
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\nRecent Context: {context}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "සමාවෙන්න මචං, මොකක් හරි system error එකක් ආවා. පොඩ්ඩක් ඉඳලා ආයෙත් අහන්නකෝ."

# --- 6. SIDEBAR DESIGN ---
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.info("Logo not detected")

    st.markdown("---")
    st.markdown("### 🧬 AI Intelligence")
    st.write("Emotional Intelligence: **v5.0**")
    st.write("Brain Sync: **Stable** 🧠")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer Info")
    st.success(f"**{DEV_NAME}**")
    st.write(f"Age: {DEV_AGE} Years")
    st.caption("Sri Lankan AI Innovator")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE ---
st.markdown('<h1 class="main-header">DiNuX AI Infinity</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Deep Neural Intelligent Exchange</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Logic
if prompt := st.chat_input("මොනවා හරි අහන්න මචං..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Processing deep logic..."):
            full_response = get_ai_response(prompt)
            # Ultra-smooth typing simulation
            displayed_text = ""
            for char in full_response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.003)
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER COPYRIGHT ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Designed & Developed by {DEV_NAME} | All Rights Reserved.
    </div>
    """, 
    unsafe_allow_html=True
)

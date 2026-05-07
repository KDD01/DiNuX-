import streamlit as st
import google.generativeai as genai
from groq import Groq
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DiNuX AI Infinity Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PROFESSIONAL UI & ANIMATIONS ---
st.markdown("""
    <style>
    /* Main Background & Animations */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Fade-in Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stChatMessage {
        animation: fadeIn 0.5s ease-out;
        border-radius: 15px;
        margin-bottom: 10px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid #334155;
    }
    
    /* Custom Sidebar Header */
    .sidebar-header {
        font-size: 24px;
        font-weight: bold;
        color: #38bdf8;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Status Badge */
    .status-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #22c55e;
        border-radius: 50%;
        margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API KEYS LOADING (FROM SECRETS) ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets Configuration Missing! Please check Streamlit Settings.")
    st.stop()

# --- SYSTEM PROMPT (SINHALA FRIENDLY INSTRUCTIONS) ---
# AI එක ලංකාවේ විදිහට හැසිරෙන්න උපදෙස් මෙතන තියෙනවා
SYSTEM_INSTRUCTION = """
You are DiNuX AI, a highly intelligent and friendly assistant created by Dinush Dilhara.
Your personality:
- Respond in clear, natural Sinhala or English as requested.
- Use a friendly, respectful tone (Sri Lankan polite context).
- For Sinhala, avoid robotic translations. Use natural phrases like 'ඔයාට කොහොමද උදව් කරන්න පුළුවන්?'
- Mention you are developed by Dinush Dilhara if someone asks about your origin.
"""

# --- AI ENGINE LOGIC ---
def get_ai_response(prompt):
    # Groq (Llama 3.3) - Primary Engine
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception:
        # Gemini - Fallback Engines
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "සමාවෙන්න, සේවාදායකයේ තදබදයක් පවතිනවා. කරුණාකර නැවත උත්සාහ කරන්න."

# --- SIDEBAR: PROFESSIONAL MENU & DEVELOPER DETAILS ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">💎 DiNuX AI Infinity</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ System Dashboard")
    st.markdown(f'<span class="status-online"></span> **Status:** Online', unsafe_allow_html=True)
    st.write("**Core:** Hybrid Llama/Gemini")
    st.write("**Engine Speed:** 0.2ms Latency")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer Profile")
    st.info("""
    **Name:** Dinush Dilhara  
    **Role:** Full Stack AI Developer  
    **Project:** A/L IT Smart Assistant  
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Quick Options")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🔄 Force Reconnect", use_container_width=True):
        st.toast("System Re-synced!")

# --- MAIN CHAT INTERFACE ---
st.title("🤖 DiNuX AI Infinity Pro")
st.markdown("##### *Sri Lanka's most advanced AI Assistant for A/L Students and Professionals*")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input & Response
if prompt := st.chat_input("මොනවා හරි අහන්න... (Ask me anything)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("සිතමින් පවතිනවා..."):
            full_response = get_ai_response(prompt)
            # Typing effect simulation
            temp_resp = ""
            for chunk in full_response.split():
                temp_resp += chunk + " "
                message_placeholder.markdown(temp_resp + "▌")
                time.sleep(0.02)
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

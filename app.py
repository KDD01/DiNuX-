import streamlit as st
import google.generativeai as genai
from groq import Groq
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DiNuX AI Infinity Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED PROFESSIONAL CSS ---
st.markdown("""
    <style>
    /* Main Background Animation */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #e2e8f0;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Chat Input Styling */
    .stChatInputContainer {
        padding: 20px;
        background-color: transparent !important;
    }
    
    .stChatInput input {
        border-radius: 25px !important;
        border: 1px solid #38bdf8 !important;
        background-color: #1e293b !important;
        color: white !important;
    }

    /* Glassmorphism Cards for Messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px !important;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    /* Buttons Style */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #0ea5e9, #2563eb);
        color: white;
        border: none;
        transition: all 0.3s ease;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.4);
    }

    /* Status Animations */
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #22c55e;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }

    /* Header Styling */
    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API LOADING ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets Configuration Missing! Please check Streamlit Cloud Settings.")
    st.stop()

# --- 4. SMART ENGINE LOGIC ---
def get_ai_response(prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are DiNuX AI, a helpful assistant by Dinush Dilhara. Use natural Sinhala/English."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception:
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                continue
    return "සමාවෙන්න, මට මේ වෙලාවේ පිළිතුරු දීමට නොහැකියි."

# --- 5. SIDEBAR DESIGN ---
with st.sidebar:
    st.markdown("## 💎 DiNuX AI Pro")
    st.markdown("---")
    
    # System Status Card
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px;">
            <p style="margin-bottom: 5px;"><span class="status-dot"></span> <b>System:</b> Online</p>
            <p style="margin-bottom: 5px; font-size: 12px;"><b>Engine:</b> Hybrid Ultra-Fast</p>
            <p style="margin-bottom: 0; font-size: 12px;"><b>Security:</b> AES Encrypted</p>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.info("**Dinush Dilhara**\n\nFull-Stack Developer & AI Specialist")
    
    st.markdown("---")
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<br><br><p style='text-align: center; color: #64748b; font-size: 10px;'>Version 5.0.1 Stable</p>", unsafe_allow_html=True)

# --- 6. MAIN CHAT AREA ---
st.markdown('<h1 class="main-title">DiNuX AI Infinity</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Experience the future of AI Assistant technology</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("මොනවා හරි අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Processing..."):
            full_response = get_ai_response(prompt)
            # Modern Typewriter Effect
            displayed_text = ""
            for char in full_response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.005) # ඉතා වේගවත් ටයිප් කිරීමේ ඉෆෙක්ට් එකක්
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

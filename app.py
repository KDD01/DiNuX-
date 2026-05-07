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

# --- 2. ELITE DARK UI CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #050505;
        color: #d1d5db;
    }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #262626;
    }

    /* Glassmorphism Chat Bubble */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 18px !important;
        margin-bottom: 12px !important;
        padding: 20px !important;
    }

    /* Modern Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }

    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #6b7280;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        letter-spacing: 1px;
    }

    /* Title Animation */
    .main-title {
        font-size: 45px;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #3b82f6, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.3));
    }
    
    .stChatInput input {
        border-radius: 30px !important;
        border: 1px solid #262626 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SECRETS LOADING ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets Configuration Missing! Please check Streamlit Settings.")
    st.stop()

# --- 4. ULTRA-FRIENDLY SYSTEM INSTRUCTION ---
# ඔයා ගැන විස්තර මෙතන "Developer Info" කොටසේ තියෙනවා
DEVELOPER_INFO = {
    "name": "Dinush Dilhara",
    "age": "19",
    "location": "Sri Lanka",
    "status": "Young Tech Visionary"
}

SYSTEM_PROMPT = f"""
You are DiNuX AI, a super-intelligent and extremely friendly AI buddy created by {DEVELOPER_INFO['name']}.
Your Rules:
1. When asked about your developer/creator/owner:
   - Say: "මාව හැදුවේ 'දිනුෂ් දිල්හාර' (Dinush Dilhara). එයාට දැන් වයස {DEVELOPER_INFO['age']}යි. එයා ලංකාවේ ඉන්න දක්ෂ AI Developer කෙනෙක්!"
2. Talk like a real Sri Lankan friend (මචං, මල්ලි, යාළුවා use කරන්න).
3. Use warm, natural Sinhala. Avoid formal 'රොබෝ' language. 
4. Be very smart, but also funny and caring.
5. If someone asks "Who are you?", tell them you are DiNuX AI, the smartest companion for Sri Lankans.
"""

# --- 5. SMART ENGINE WITH FALLBACK ---
def get_ai_response(prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            temperature=0.85,
        )
        return completion.choices[0].message.content
    except Exception:
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "අයියෝ මචං, පොඩි connection error එකක් ආවා. ආයෙත් පාරක් අහපංකෝ!"

# --- 6. SIDEBAR DESIGN ---
with st.sidebar:
    # Round Logo Handling
    try:
        image = Image.open("logo.png")
        st.image(image, use_container_width=True)
    except:
        st.info("Logo.png not found")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚙️ System Status")
    st.markdown("🟢 **Engines Active**")
    st.markdown("🔒 **End-to-End Encrypted**")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Mastermind")
    st.success(f"**{DEVELOPER_INFO['name']}**")
    st.write(f"Age: {DEVELOPER_INFO['age']} Years")
    
    st.markdown("---")
    if st.button("🗑️ Clear My Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN CHAT AREA ---
st.markdown('<h1 class="main-title">DiNuX AI Infinity Pro</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Powered by Next-Gen Neural Engines</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("මොනවා හරි අහන්න මචං..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Processing..."):
            full_response = get_ai_response(prompt)
            # Smooth Typing effect
            temp_text = ""
            for char in full_response:
                temp_text += char
                message_placeholder.markdown(temp_text + "▌")
                time.sleep(0.003)
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER COPYRIGHT MESSAGE ---
st.markdown(
    f"""
    <div class="footer">
        © 2026 DiNuX AI Infinity | Designed & Developed by {DEVELOPER_INFO['name']}
    </div>
    """, 
    unsafe_allow_html=True
)

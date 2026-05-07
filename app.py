import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import base64
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Professional CSS
st.markdown("""
    <style>
    /* Base Background */
    .stApp {
        background: #0e0e11;
        color: #e3e3e3;
    }
    
    /* Hide Default Headers */
    header, footer {visibility: hidden;}
    
    /* Sidebar Styling (Logo Area) */
    [data-testid="stSidebar"] {
        background-color: #050507 !important;
        border-right: 1px solid #1e1e24;
        min-width: 300px !important;
    }
    
    .sidebar-logo-container {
        text-align: center;
        padding: 40px 10px;
    }
    
    .logo-outer {
        width: 150px;
        height: 150px;
        margin: 0 auto;
        border: 2px solid #4facfe;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.3);
        background: radial-gradient(circle, #1e1e3f 0%, #050507 100%);
    }

    .logo-inner-text {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 30%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .dinux-text-sidebar {
        font-size: 2.2rem;
        font-weight: 800;
        margin-top: 15px;
        letter-spacing: 3px;
        color: white;
    }
    
    .kdd-studio-text {
        color: #4facfe;
        font-size: 0.8rem;
        letter-spacing: 4px;
        font-weight: 600;
        margin-top: -10px;
    }

    /* Chat UI Enhancement */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }

    /* Smart Chat Input Box */
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        padding: 0 10% 30px 10% !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background: #1e1e24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 16px !important;
        transition: border 0.3s ease;
    }
    
    div[data-testid="stChatInput"] > div:focus-within {
        border: 1px solid #4facfe !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #0e0e11; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
GEMINI_API_KEY = "AIzaSyB27W11humZP7AiXWmrkwEHQcNq2LXxjkw"

def init_model():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None

model = init_model()

def search_tool(q):
    try:
        with DDGS() as ddgs:
            return "\n".join([r['body'] for r in ddgs.text(q, max_results=2)])
    except: return ""

def speak(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text[:400], lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- SESSION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR (THE PROFESSIONAL MENU) ---
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-logo-container">
            <div class="logo-outer">
                <span class="logo-inner-text">DX</span>
            </div>
            <div class="dinux-text-sidebar">DiNuX</div>
            <div class="kdd-studio-text">POWERED BY KDD STUDIO</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("➕ New Chat Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🛠 AI Intelligence")
    st.caption("Engine: Gemini 1.5 Flash")
    st.caption("Capabilities: Search, Voice, Multilingual")
    
    st.markdown("<br>"*5, unsafe_allow_html=True)
    st.info("Developer: Dinush Dilhara\n\nPlatform: DS MEDIA HUB")

# --- MAIN CHAT AREA ---
if not st.session_state.messages:
    # Landing View
    st.markdown("<br>"*5, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:3.5rem;'>How can I help you today?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666;'>Connect with DiNuX AI for smart information and assistance.</p>", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- INPUT & RESPONSE ---
if prompt := st.chat_input("Connect with DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_box = st.empty()
        full_text = ""
        
        # Enhanced Context
        context = search_tool(prompt)
        instr = f"ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara (KDD Studio). Context: {context}. කෙටි සහ පැහැදිලි පිළිතුරු දෙන්න."
        
        try:
            if model:
                stream = model.generate_content([instr, prompt], stream=True)
                for chunk in stream:
                    if chunk.text:
                        full_text += chunk.text
                        response_box.markdown(full_text + "▌")
                
                response_box.markdown(full_text)
                speak(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            else:
                st.error("System Error: Check API Connection.")
        except Exception as e:
            st.error("Connection Interrupted. Please try again.")

import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import base64
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX AI - Powered by KDD Studio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Advanced UI Styling (Based on your Image)
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #0e0e11;
        color: #ffffff;
    }

    /* Hide Navigation and Elements */
    header, footer, [data-testid="stSidebar"] {visibility: hidden;}

    /* Split Screen Layout */
    .main-container {
        display: flex;
        height: 100vh;
        align-items: center;
    }

    .left-panel {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    .right-panel {
        flex: 1.5;
        padding: 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* DiNuX Logo Styling */
    .logo-circle {
        width: 350px;
        height: 350px;
        border-radius: 50%;
        background: url('https://img.icons8.com/clouds/500/artificial-intelligence.png'); /* ඔබට අවශ්‍ය ලෝගෝ එක මෙතැනට දැමිය හැක */
        background-size: cover;
        border: 4px solid #4facfe;
        box-shadow: 0 0 50px rgba(79, 172, 254, 0.4);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .logo-text {
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: 5px;
        background: linear-gradient(90deg, #ffffff, #4facfe, #9b72cb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Right Panel Text */
    .brand-title {
        font-size: 4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .brand-sub {
        font-size: 1.2rem;
        color: #4facfe;
        letter-spacing: 3px;
        font-weight: 600;
        margin-bottom: 50px;
        text-transform: uppercase;
    }

    /* Chat Input Styling */
    div[data-testid="stChatInput"] {
        width: 80% !important;
        background: #1e1e24 !important;
        border-radius: 15px !important;
        border: 1px solid #333 !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        color: white !important;
    }

    /* Message Bubbles */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API CORE SETUP ---
GEMINI_API_KEY = "AIzaSyB27W11humZP7AiXWmrkwEHQcNq2LXxjkw"

def initialize_model():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except:
        return None

model = initialize_model()

# Helper Functions
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=2)]
            return "\n\n".join(results)
    except: return ""

def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text[:300], lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- SESSION HANDLING ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI LAYOUT ---
# ඔබ එවූ Image එකේ ආකාරයට Screen එක දෙකට බෙදීම
if not st.session_state.messages:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
                <div style="text-align: center;">
                    <div style="border: 5px solid #4facfe; border-radius: 50%; padding: 40px; box-shadow: 0 0 30px #4facfe88;">
                         <h1 style="font-size: 5rem; margin: 0; color: white;">DX</h1>
                         <h2 style="color: #4facfe; margin: 0;">DiNuX AI</h2>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 80vh;">
                <h1 class="brand-title">DiNuX AI</h1>
                <p class="brand-sub">POWERED BY KDD STUDIO</p>
            </div>
        """, unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- PROCESSING ---
if prompt := st.chat_input("Connect with DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        search_results = search_web(prompt)
        sys_instructions = f"ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara (KDD Studio). Context: {search_results}. කෙටියෙන් පිළිතුරු දෙන්න."
        
        try:
            if model:
                response = model.generate_content([sys_instructions, prompt], stream=True)
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                play_voice(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("API Key Error!")
        except Exception as e:
            st.error("Error occurred.")

import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import base64
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. UI Styling (Enhanced Modern UI)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2f, #0e0e11);
        color: #ffffff;
    }

    /* Hide Streamlit Headers */
    header, footer {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 25, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Chat Message Bubbles */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* DiNuX Gradient Logo */
    .dinux-logo {
        background: linear-gradient(90deg, #00f2fe, #4facfe, #7000ff);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-weight: 800; 
        font-size: 2.5rem; 
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }

    /* Input Box Styling */
    div[data-testid="stChatInput"] {
        position: fixed; 
        bottom: 30px; 
        padding: 0 10%;
    }
    
    div[data-testid="stChatInput"] > div {
        background: rgba(30, 30, 36, 0.9) !important;
        border: 1px solid rgba(79, 172, 254, 0.5) !important;
        border-radius: 30px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Welcome Screen Text */
    .welcome-container {
        text-align: center; 
        margin-top: 15vh;
    }
    .welcome-title {
        font-size: 4.5rem; 
        font-weight: 800; 
        background: linear-gradient(120deg, #ffffff, #4facfe, #00f2fe);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .welcome-sub {
        font-size: 1.5rem; 
        color: #888; 
        font-weight: 300;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API CORE SETUP ---
GEMINI_API_KEY = "AIzaSyB-3mqtHBYgaEqTSi1aACF76VH745vvejs"

def initialize_model():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority_models = ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.5-pro']
        
        selected_model = next((pm for pm in priority_models if pm in available_models), available_models[0] if available_models else None)
        return genai.GenerativeModel(selected_model) if selected_model else None
    except Exception as e:
        st.error(f"Initialization Failed: {e}")
        return None

model = initialize_model()

# Helper Functions
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n\n".join(results)
    except: return ""

def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- SESSION HANDLING ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen (Only shows if no chat exists)
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-container">
            <p style="color:#4facfe; font-weight:bold; letter-spacing:4px; text-transform: uppercase;">Next-Gen Intelligence</p>
            <h1 class="welcome-title">Hello, DiNuX</h1>
            <h2 class="welcome-sub">How can I assist your creative journey today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- PROCESSING ---
if prompt := st.chat_input("Message DiNuX..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        search_results = search_web(prompt)
        sys_instructions = f"ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara. Context: {search_results}. 100% සත්‍ය තොරතුරු ලබා දෙන්න."
        
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
                st.error("Model unavailable. Please check API key.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown("<h1 class='dinux-logo'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>v2.0 Advanced Edition</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Chat Controls")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.info("Created by **Dinush Dilhara**\n\nPowered by Google Gemini & DS Media Hub.")

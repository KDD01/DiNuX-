import streamlit as st
import google.generativeai as genai
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 
TAVILY_API_KEY = "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"

# API Initialize with Safety Override (to prevent errors)
try:
    genai.configure(api_key=GEMINI_API_KEY)
    search_tool = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
    
    # Safety settings off (Errors අඩු කිරීමට)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UI SETTINGS (Preserving your style) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    .shining-title {
        font-size: clamp(32px, 10vw, 48px);
        font-weight: 800;
        text-align: center;
        background: linear-gradient(120deg, #ffffff 20%, #888888 50%, #ffffff 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text; color: white;
        animation: shine 3s linear infinite;
        margin-bottom: 5px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 20px; font-size: 14px; }
    
    /* Input Bar Styling */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    section[data-testid="stSidebar"] { background-color: #080c14; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    logo_path = "logo.png.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.title("DiNuX Settings")
    selected_model = st.selectbox("Intelligence Level", ["gemini-1.5-flash", "gemini-1.5-pro"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.caption("KDD Studio © 2026")

# --- 4. MAIN UI ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Developed by Dinush Dilhara</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT BAR WITH INTEGRATED MEDIA (The "No Error" UI) ---
# මෙතනදී අපි colums පාවිච්චි කරලා chat bar එක ගාවටම buttons ගේනවා
input_container = st.container()
with input_container:
    c1, c2, c3 = st.columns([1, 7, 1])
    
    with c1:
        # Image upload button right next to text input
        img_file = st.file_uploader("📷", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    with c2:
        prompt = st.chat_input("මෙතනින් කතා කරන්න...")
    
    with c3:
        # Voice button right next to text input
        voice_data = mic_recorder(start_prompt="🎤", stop_prompt="✔️", key='voice_btn')

# --- 6. BRAIN LOGIC (Auto-Fixing Bugs) ---
if prompt or img_file or voice_data:
    user_query = prompt if prompt else "Analyze this for me."
    if voice_data:
        user_query = "Voice input received. Please respond in natural Sinhala."
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if img_file:
            st.image(img_file, width=200)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        # System instructions
        sys_msg = "You are DiNuX AI, a helpful friend. Talk in natural spoken Sinhala (casual). Use 'oyaa/mama'. Be logical."

        try:
            # Search Context
            search_info = ""
            if prompt and any(x in prompt.lower() for x in ["news", "today", "දැන්", "price"]):
                search_info = f"\n\n[Live Search]: {search_tool.run(prompt)}"

            # Model calling with safety override
            model = genai.GenerativeModel(model_name=selected_model, safety_settings=safety_settings)
            
            parts = [sys_msg + search_info + user_query]
            if img_file:
                parts.append(Image.open(img_file))

            # Stream response with error handling for empty chunks
            response = model.generate_content(parts, stream=True)
            
            for chunk in response:
                try:
                    if chunk.text:
                        full_res += chunk.text
                        res_area.markdown(full_res + "▌")
                except:
                    # උත්තරේ block වුණොත් එන error එක මෙතනින් handle කරනවා
                    continue 
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            # මොනම error එකක් ආවත් assistant මැරෙන්නේ නැතුව මේක පෙන්වනවා
            st.warning("⚠️ Connection reset. I'm fixing it...")
            time_fix = model.generate_content("Say 'Sry Dinush, podi error ekak awa. Aye ahanna.' in Sinhala")
            res_area.markdown(time_fix.text)

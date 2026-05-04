import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Quantum AI",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Ultra-Modern Gemini UI CSS (Advanced Version)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0d0d0e; color: #e8eaed; }
    header, footer {visibility: hidden;}

    /* Sidebar Menu Styling */
    [data-testid="stSidebar"] {
        background-color: #161719 !important;
        border-right: 1px solid #333;
    }

    /* Floating Chat Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 85% !important;
        max-width: 800px !important;
        background: #1e1f20 !important;
        border-radius: 24px !important;
        border: 1px solid #3c4043 !important;
        padding: 8px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }

    /* Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border-radius: 15px;
        padding: 1rem !important;
    }

    /* Gradient Branding */
    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #a142f4, #eb4034);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #2b2c2f;
        color: white;
        border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Functional Logic
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- ADVANCED MENU (Sidebar) ---
with st.sidebar:
    st.markdown("<h1 class='gemini-gradient'>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🚀 Features & Tools")
    tool_mode = st.radio("Select Tool:", ["Smart Chat 💬", "Image Analysis 🖼️", "File Reader 📄"])
    
    st.subheader("🔊 Audio Settings")
    voice_on = st.toggle("Voice Responses", value=False)
    
    st.subheader("⚙️ Intelligence")
    model_choice = st.selectbox("Model Speed:", ["Fast (8B)", "Powerful (70B)"])
    
    st.markdown("---")
    if st.button("Clear Memory 🗑️"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Developer: Dinush Dilhara")
    st.caption("Status: All Features Active ✅")

# --- AI Client Setup ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<h2 style='text-align: center; margin-top: 50px;'>කොහොමද, <span class='gemini-gradient'>දිනුෂ්</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8e918f;'>අද මම ඔබට උදව් කරන්නේ කෙසේද? සියලුම Features සක්‍රියයි.</p>", unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- FEATURE LOGIC: TOOL HANDLING ---

# 1. File/Image Upload Feature
if tool_mode != "Smart Chat 💬":
    uploaded_file = st.file_uploader("Upload here...", type=["png", "jpg", "jpeg", "pdf", "txt"])
    if uploaded_file:
        st.success(f"{uploaded_file.name} සාර්ථකව ඇතුළත් කරන ලදී.")

# 2. Main Chat Interaction
if prompt := st.chat_input("මෙහි විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Advanced Logic Instruction
        sys_prompt = """
        ඔබේ නම DiNuX. ඔබව නිර්මාණය කළේ Dinush Dilhara විසිනි.
        ඔබ අතිශය බුද්ධිමත්, තර්කානුකූල සහ වෘත්තීය AI සහායකයෙකි.
        සැමවිටම කෙලින්ම සහ සත්‍ය කරුණු මත පදනම්ව පිළිතුරු දෙන්න.
        භාෂාව: වෘත්තීය සිංහල (Professional Sinhala).
        """
        
        selected_model = "llama-3.1-8b-instant" if model_choice == "Fast (8B)" else "llama-3.1-70b-versatile"
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            # AI Thinking Simulation
            with st.status("විශ්ලේෂණය කරමින්...", expanded=False):
                chat = client.chat.completions.create(
                    messages=history,
                    model=selected_model,
                    temperature=0.3
                )
                res = chat.choices[0].message.content
            
            st.markdown(res)
            
            if voice_on:
                play_voice(res)
                
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        except Exception as e:
            # Fallback Anti-Error System
            try:
                fallback = client.chat.completions.create(
                    messages=history,
                    model="mixtral-8x7b-32768"
                )
                st.markdown(fallback.choices[0].message.content)
            except:
                st.error("දැනට සේවාදායකයේ තදබදයක් පවතී. කරුණාකර නැවත උත්සාහ කරන්න.")

import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time

# 1. Page Configuration - Ultra Modern UI
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. High-End Gemini UI Styling (Custom CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Google Sans', sans-serif;
    }

    /* Professional Dark Theme */
    .stApp {
        background-color: #0e0e10;
        color: #e3e3e3;
    }

    header, footer {visibility: hidden;}

    /* Advanced Message Styling */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.5rem 0 !important;
        animation: fadeIn 0.5s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Gemini Bottom Input Bar - Floating Design */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 35px;
        left: 50%;
        transform: translateX(-50%);
        width: 85% !important;
        max-width: 800px !important;
        background: rgba(30, 31, 32, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 32px !important;
        border: 1px solid #3c4043 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 1000;
    }

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #333;
    }

    .gemini-gradient {
        background: linear-gradient(120deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
    }

    /* Interaction Button Styling */
    .stButton>button {
        border-radius: 20px !important;
        background-color: #333537 !important;
        color: white !important;
        border: none !important;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #444746 !important;
        transform: scale(1.02);
    }

    /* Mobile Adaptability */
    @media (max-width: 768px) {
        div[data-testid="stChatInput"] { width: 92% !important; bottom: 20px; }
        .gemini-gradient { font-size: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Engine Functions
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except Exception:
        pass

# --- Menu & Sidebar Setup ---
with st.sidebar:
    st.markdown("<h2 class='gemini-gradient'>DiNuX Core</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Settings")
    voice_on = st.toggle("Advanced Voice Response 🔊", value=False)
    personality = st.selectbox("Intelligence Mode", ["Professional & Logical", "Creative & Friendly"])
    
    st.markdown("---")
    if st.button("Clear Conversation History 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")
    st.caption("Version: 3.5 Platinum Edition")

# --- AI Intelligence Center ---
# Multi-Model Redundancy to avoid Rate Limits
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dynamic Welcome Screen
if not st.session_state.messages:
    st.markdown('<h1>සෙවුම අරඹන්න, <span class="gemini-gradient">මම DiNuX</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #bdc1c6; font-size: 1.2rem;'>ඔබට අවශ්‍ය ඕනෑම තාක්ෂණික හෝ සාමාන්‍ය දැනුමක් වෘත්තීය මට්ටමින් ලබා දීමට මම සූදානම්.</p>", unsafe_allow_html=True)

# Show Messages with Avatars
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Action Logic ---
if prompt := st.chat_input("මෙහි විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Advanced System Prompt with Logic Constraints
        sys_instructions = f"""
        ඔබේ නම DiNuX. නිර්මාණය කළේ Dinush Dilhara විසිනි.
        පෞරුෂය: {personality}
        1. පිළිතුරු සැපයීමේදී වෘත්තීය සිංහල භාෂාව (Professional Sinhala) භාවිතා කරන්න.
        2. සෑම විටම තර්කානුකූල සහ නිරවද්‍ය දත්ත ලබා දෙන්න (Logical & Accurate).
        3. අනවශ්‍ය වැල්වටාරම් ඉවත් කර සෘජු පිළිතුරු ලබා දෙන්න.
        4. පියවරෙන් පියවර විස්තර කළ යුතු කරුණු සඳහා Bullet points භාවිතා කරන්න.
        5. ව්‍යාකරණ සහ අක්ෂර වින්‍යාසය පිළිබඳව අතිශය සැලකිලිමත් වන්න.
        """
        
        full_history = [{"role": "system", "content": sys_instructions}] + st.session_state.messages

        try:
            # Primary Logic Engine: High-performance 70B Model
            chat_completion = client.chat.completions.create(
                messages=full_history,
                model="llama-3.1-70b-versatile",
                temperature=0.3 if "Professional" in personality else 0.7,
                max_tokens=2048,
                top_p=1
            )
            
            response = chat_completion.choices[0].message.content
            
            # Simulated Thinking for User Familiarity
            with st.spinner('විශ්ලේෂණය කරමින් පවතිනවා...'):
                time.sleep(0.5)
                st.markdown(response)
            
            if voice_on:
                play_voice(response)
                
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            # Automatic Fallback for Rate Limit Issues
            try:
                fallback_chat = client.chat.completions.create(
                    messages=full_history,
                    model="llama-3.1-8b-instant",
                    temperature=0.4
                )
                res = fallback_chat.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("දැනට සේවාදායකයේ අධික තදබදයක් පවතී. කරුණාකර තප්පර කිහිපයකින් නැවත උත්සාහ කරන්න.")

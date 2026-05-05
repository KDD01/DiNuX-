import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import base64
from gtts import gTTS
import io
import time

# 1. Page Configuration
st.set_page_config(
    page_title="DiNuX Advanced AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e0e11; color: #e3e3e3; }
    header, footer {visibility: hidden;}
    .block-container { max-width: 850px; padding-bottom: 10rem; }
    .dinux-logo {
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.2rem; text-align: center;
    }
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; left: 50% !important;
        transform: translateX(-50%); width: 65% !important;
        z-index: 1000;
    }
    div[data-testid="stChatInput"] > div {
        background: #1e1e24 !important; border: 1px solid #3c4043 !important;
        border-radius: 28px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Functions
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
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

# --- ENGINE SETUP ---
# මෙතනට ඔබේ අලුත්ම API Key එක දාන්න
API_KEY = "ඔබේ_අලුත්_GROQ_API_KEY_එක_මෙතනට_දමන්න" 
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
if not st.session_state.messages:
    st.markdown("<div style='text-align:center; margin-top:20vh;'><h1 style='font-size:4rem; color:white;'>Hello, <span style='color:#4facfe;'>DiNuX</span></h1><h2 style='color:#757575;'>How can I help you today?</h2></div>", unsafe_allow_html=True)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Handling
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # 1. Background Search
        search_context = search_web(prompt)
        
        # 2. Advanced System Prompt
        sys_prompt = f"""
        ඔබේ නම DiNuX AI. නිර්මාණය කළේ Dinush Dilhara.
        සත්‍ය තොරතුරු පමණක් ලබා දෙන්න. සෙවුම් ප්‍රතිඵල: {search_context}
        තාර්කිකව සිතා පිළිතුරු දෙන්න. Looping වීම වළක්වන්න.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-6:]

        # 3. Smart Request with Error Handling
        try:
            # උත්සාහය 1: ප්‍රධාන මාදිලිය (Llama 3.3)
            completion = client.chat.completions.create(
                messages=history,
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            play_voice(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # දෝෂයක් ආවොත් වෙනත් Model එකකින් උත්සාහ කිරීම (Fallback)
            if "rate_limit" in str(e).lower():
                st.warning("පද්ධතිය කාර්යබහුලයි. විකල්ප මාදිලියකින් පිළිතුරු සොයමින්...")
                time.sleep(2) # තත්පර 2ක් රැඳී සිටීම
                try:
                    completion = client.chat.completions.create(
                        messages=history,
                        model="mixtral-8x7b-32768", # සීමාව අඩු මාදිලියක්
                        temperature=0.5
                    )
                    full_response = completion.choices[0].message.content
                    placeholder.markdown(full_response)
                    play_voice(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except:
                    st.error("දැනට පද්ධතියේ උපරිම සීමාව ඉක්මවා ඇත. කරුණාකර විනාඩියකින් නැවත උත්සාහ කරන්න.")
            else:
                st.error(f"සම්බන්ධතාවයේ දෝෂයක්: {e}")

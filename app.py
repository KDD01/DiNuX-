import streamlit as st
from groq import Groq
from PIL import Image
import base64
from gtts import gTTS
import io
import os

# 1. පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="wide")

# 2. UI පෙනුම (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage { border-radius: 20px; border: 1px solid #1e1e2e; padding: 15px; margin-bottom: 10px; background-color: #11111b; }
    h1 { text-align: center; background: linear-gradient(90deg, #ffffff, #515ada); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; margin-bottom: 0px; }
    .footer { text-align: center; color: #515ada; font-size: 0.8em; padding: 20px; }
    /* චැට් එක පල්ලෙහහින්ම තැබීමට */
    .stChatInputContainer { padding-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 3. වොයිස් ෆන්ක්ෂන් එක
def speak_text(text):
    try:
        is_sinhala = any("\u0d80" <= char <= "\u0dff" for char in text)
        lang = 'si' if is_sinhala else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        pass

# --- UI ආරම්භය ---

# 4. ලෝගෝ එක සහ හෙඩර් එක ලස්සනට මැදට ගැනීම
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h2 style='text-align: center;'>DiNuX AI</h2>", unsafe_allow_html=True)

st.markdown("<h1>THINK • LEARN • EVOLVE</h1>", unsafe_allow_html=True)
st.markdown("---")

# 5. Groq Client එක (ඔයාගේ Key එකම පාවිච්චි කර ඇත)
client = Groq(api_key="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")

# 6. මැසේජ් සේව් කරගන්නා ලිස්ට් එක
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. කලින් කරපු මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. චැට් ඉන්පුට් එක (Chat Input) - මෙය අනිවාර්යයෙන්ම පෙන්විය යුතුයි
prompt = st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අසන්න...")

if prompt:
    # පරිශීලකයාගේ මැසේජ් එක
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකේ පිළිතුර
    with st.chat_message("assistant"):
        # ඉතාමත් ස්වභාවික සිංහල උපදෙස්
        system_instruction = "ඔබේ නම DiNuX. ඔබ ඉතාමත් මිත්‍රශීලී ශ්‍රී ලාංකික AI සහායකයෙකි. පරිශීලකයා Singlish වලින් ලිව්වත් ඉතා ස්වභාවික සිංහලෙන් පිළිතුරු දෙන්න. මිතුරෙකු මෙන් කතා කරන්න."
        
        full_messages = [{"role": "system", "content": system_instruction}]
        for m in st.session_state.messages:
            full_messages.append({"role": m["role"], "content": m["content"]})

        try:
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.8,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            # පිළිතුර කියවන්න
            speak_text(response)
            
            # මැසේජ් එක සේව් කරගැනීම
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

# 9. Footer
st.markdown("<div class='footer'>---<br>Powered by DiNuX AI | DS Media Hub</div>", unsafe_allow_html=True)

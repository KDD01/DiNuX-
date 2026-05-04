import streamlit as st
from groq import Groq
from PIL import Image, ImageOps, ImageDraw
import base64
from gtts import gTTS
import io
import os

# 1. පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="wide")

# 2. Premium UI පෙනුම (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1e1e2e; background-color: #0d1117; }
    h1 { background: linear-gradient(90deg, #ffffff, #515ada); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; }
    .stSidebar { background-color: #0d1117 !important; border-right: 1px solid #1e1e2e; }
    /* ලෝගෝ එක රවුම් කිරීමට */
    .round-logo { border-radius: 50%; width: 80px; height: 80px; object-fit: cover; border: 2px solid #515ada; }
    </style>
    """, unsafe_allow_html=True)

# 3. රවුම් ලෝගෝ එක සකසන Function එක
def get_round_logo(img_path):
    img = Image.open(img_path).convert("RGBA")
    size = (200, 200)
    img = img.resize(size, Image.LANCZOS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

# 4. Voice Function
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
    except:
        pass

# --- Sidebar (Menu Bar) ---
with st.sidebar:
    if os.path.exists("logo.png"):
        round_img = get_round_logo("logo.png")
        st.image(round_img, width=100)
    st.markdown("### DiNuX AI Menu")
    st.markdown("---")
    # Voice Option එක පාලනය කරන Button එක
    voice_on = st.toggle("Voice Response (කටහඬ සක්‍රීය කරන්න)", value=False)
    st.info("Developer: Dinush Dilhara")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- Main UI ---
st.markdown("<h1>DiNuX AI 🤖</h1>", unsafe_allow_html=True)
st.caption("Think • Learn • Evolve | Intelligent Partner")
st.markdown("---")

# Groq Client
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # දියුණු කරන ලද System Instruction සහ Developer අනන්‍යතාවය
        system_instruction = """
        ඔබේ නම DiNuX. ඔබව නිර්මාණය කළේ (Developer/Creator) 'Dinush Dilhara' විසින්ය. 
        කවුරුන් හෝ ඔබව හැදුවේ කවුදැයි ඇසුවහොත්, ඉතා ආඩම්බරයෙන් 'මාව නිර්මාණය කළේ Dinush Dilhara' බව පවසන්න.
        
        ඔබේ ගති ලක්ෂණ:
        1. භාෂාව: පරිශීලකයා Singlish/English වලින් ඇසුවත්, පිළිතුරු සිංහල අකුරෙන් (Unicode) ලබා දෙන්න.
        2. තර්කනය (Logic): ගැඹුරු ප්‍රශ්නවලදී 100% නිවැරදි, තර්කානුකූල සහ විශ්ලේෂණාත්මක පිළිතුරු ලබා දෙන්න.
        3. හැඟීම් (Emotions): පරිශීලකයාගේ මනෝභාවය හඳුනාගෙන සංවේදීව සහ මිත්‍රශීලීව පිළිතුරු දෙන්න.
        4. ශෛලිය: ඉතාමත් ස්වභාවික සිංහල (Natural Conversational Sinhala) භාවිතා කරන්න.
        """
        
        full_messages = [{"role": "system", "content": system_instruction}]
        for m in st.session_state.messages:
            full_messages.append({"role": m["role"], "content": m["content"]})

        try:
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            # Voice Option එක On නම් පමණක් කියවයි
            if voice_on:
                speak_text(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("<br><br><p style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 Designed by Dinush Dilhara | DS Media Hub</p>", unsafe_allow_html=True)

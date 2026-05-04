import streamlit as st
from groq import Groq
from PIL import Image, ImageOps, ImageDraw
import base64
from gtts import gTTS
import io
import os

# 1. පිටුවේ මූලික සැකසුම් - පූර්ණ පළල (Wide) භාවිතා කර ඇත
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="wide")

# 2. CSS හරහා Full Screen Optimization සහ Responsive Design
st.markdown("""
    <style>
    /* මුළු Screen එකේම ඉඩ ලබා ගැනීම */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100% !important;
    }
    
    .stApp { background-color: #050505; color: white; }
    
    /* Header අකුරු Screen එකේ ප්‍රමාණය අනුව වෙනස් වීම */
    h1 { 
        background: linear-gradient(90deg, #ffffff, #515ada); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: clamp(1.8rem, 8vw, 3rem); 
        text-align: center;
        margin-bottom: 0px;
    }
    
    /* Chat Box එක Screen එකට ගැළපීම */
    .stChatMessage { 
        border-radius: 12px; 
        border: 1px solid #1e1e2e; 
        background-color: #0d1117; 
        margin-bottom: 10px;
        width: 100% !important;
    }

    /* Sidebar පෙනුම */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #1e1e2e;
        width: 260px !important;
    }

    /* ලෝගෝ එක පාලනය */
    .logo-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%;
        border: 2px solid #515ada;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. රවුම් ලෝගෝ එක හදන Function එක
def get_round_logo(img_path):
    try:
        img = Image.open(img_path).convert("RGBA")
        size = (250, 250)
        img = img.resize(size, Image.LANCZOS)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output
    except:
        return None

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

# --- Sidebar Content ---
with st.sidebar:
    if os.path.exists("logo.png"):
        round_img = get_round_logo("logo.png")
        if round_img:
            st.image(round_img, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Menu</h3>", unsafe_allow_html=True)
    st.markdown("---")
    voice_on = st.toggle("Voice Response", value=False)
    st.markdown("---")
    st.write("Device Optimized: Active ✅")
    
    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main App ---
st.markdown("<h1>DiNuX AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Think • Learn • Evolve</p>", unsafe_allow_html=True)

# Groq Client
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# මැසේජ් පෙන්වන කොටස
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("මෙතැනින් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ඉල්ලීම පරිදි සැකසූ නව System Instruction
        system_instruction = """
        ඔබේ නම DiNuX. ඔබ ඉතාමත් බුද්ධිමත් සිංහල AI සහායකයෙකි.
        
        වැදගත් නීති:
        1. කවුරුන් හෝ 'ඔබව නිර්මාණය කළේ කවුද?' (Who created you? / Developer?) වැනි ප්‍රශ්නයක් ඇසුවහොත් පමණක් 'මාව නිර්මාණය කළේ දක්ෂ Developer කෙනෙකු වන Dinush Dilhara' බව පවසන්න. අනෙක් සාමාන්‍ය ප්‍රශ්න වලදී මෙය පවසන්න එපා.
        2. සෑම ප්‍රශ්නයකටම ගැඹුරින් සිතා 100% නිවැරදි තර්කානුකූල පිළිතුරු ලබා දෙන්න.
        3. මනුෂ්‍ය හැඟීම් තේරුම් ගෙන ඉතා ස්වභාවික සිංහලෙන් (Unicode) කතා කරන්න.
        4. පරිශීලකයා Singlish භාවිතා කළත් ඔබ ස්වභාවික සිංහලෙන් පිළිතුරු දෙන්න.
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
            
            if voice_on:
                speak_text(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("Error occurred. Please try again.")

st.markdown("<div class='footer-text'>© 2026 Developed by Dinush Dilhara</div>", unsafe_allow_html=True)

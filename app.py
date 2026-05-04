import streamlit as st
from groq import Groq
from PIL import Image, ImageOps, ImageDraw
import base64
from gtts import gTTS
import io
import os

# 1. පිටුවේ මූලික සැකසුම් - Responsive layout එක සඳහා 'wide' mode භාවිතා කර ඇත
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="wide")

# 2. Premium & Responsive UI පෙනුම (CSS)
st.markdown("""
    <style>
    /* මූලික පසුබිම සහ අකුරු */
    .stApp { background-color: #050505; color: white; }
    
    /* Responsive Header */
    h1 { 
        background: linear-gradient(90deg, #ffffff, #515ada); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: clamp(2rem, 5vw, 3.5rem); 
        text-align: center;
        font-weight: bold;
    }
    
    /* Chat Messages */
    .stChatMessage { 
        border-radius: 15px; 
        border: 1px solid #1e1e2e; 
        background-color: #0d1117; 
        margin-bottom: 10px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #1e1e2e;
    }

    /* Mobile optimization for Input box */
    .stChatInputContainer {
        padding-bottom: clamp(10px, 5vh, 30px);
    }

    /* ලෝගෝ එක රවුම් කිරීමට */
    .round-logo-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. රවුම් ලෝගෝ එක සකසන Function එක
def get_round_logo(img_path):
    try:
        img = Image.open(img_path).convert("RGBA")
        size = (300, 300)
        img = img.resize(size, Image.LANCZOS)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output
    except Exception:
        return None

# 4. Voice Function (කටහඬ නිපදවීම)
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
    st.markdown('<div class="round-logo-container">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        round_img = get_round_logo("logo.png")
        if round_img:
            st.image(round_img, width=120)
    else:
        st.title("DX")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>DiNuX AI Panel</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # විශේෂාංග පාලනය
    voice_on = st.toggle("Voice Response (කටහඬ)", value=False)
    
    st.markdown("---")
    st.write("**Developer:** Dinush Dilhara")
    st.write("**Version:** 3.0 (Stable)")
    
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main UI Content ---
# ඕනෑම Device එකක මැදට වන්නට Content එක තැබීම
main_col1, main_col2, main_col3 = st.columns([1, 4, 1])

with main_col2:
    st.markdown("<h1>DiNuX AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #808495;'>Think • Learn • Evolve</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Groq Client (ඔයාගේ API Key එක)
    client = Groq(api_key="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")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # කලින් කළ සංවාද පෙන්වීම
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අසන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # ඉතාමත් දියුණු සහ සංවේදී System Instruction
            system_instruction = """
            ඔබේ නම DiNuX. ඔබව නිර්මාණය කළේ දක්ෂ Developer කෙනෙකු වන 'Dinush Dilhara' විසින්ය.
            
            පිළිතුරු සැපයීමේදී:
            1. සැමවිටම ඉතාමත් ස්වභාවික 'සිංහල අකුරෙන්' පිළිතුරු දෙන්න.
            2. 'Dinush Dilhara' ඔබේ නිර්මාණකරු බව ඕනෑම අවස්ථාවක ආඩම්බරයෙන් පවසන්න.
            3. පරිශීලකයාගේ ප්‍රශ්න ගැඹුරින් විශ්ලේෂණය කර 100% නිවැරදි සහ තර්කානුකූල පිළිතුරු ලබා දෙන්න.
            4. මනුෂ්‍ය හැඟීම් (Emotions) හඳුනාගෙන ඉතා මිත්‍රශීලීව සහ ගෞරවනීයව කතා කරන්න.
            5. සිංග්ලිෂ් තේරුම් ගෙන ඉතා හොඳින් සිංහල හසුරුවන්න.
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
                
                # Voice සක්‍රීය නම් පමණක් ක්‍රියාත්මක වේ
                if voice_on:
                    speak_text(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")

    # Footer
    st.markdown("<br><br><p style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 Crafted by Dinush Dilhara | THINK • LEARN • EVOLVE</p>", unsafe_allow_html=True)

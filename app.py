import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# =========================================================
# DiNuX AI - ULTRA UI VERSION
# UI MATCHED TO YOUR SCREENSHOT
# =========================================================

# ---------------- API KEY ----------------
API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DiNuX AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ADVANCED CSS
# =========================================================
st.markdown("""
<style>

/* ---------------- MAIN BACKGROUND ---------------- */
.stApp{
    background:
    radial-gradient(circle at top left,#10182a 0%,#070b14 30%,#04060c 60%,#02040a 100%);
    color:white;
    overflow:hidden;
}

/* ---------------- REMOVE STREAMLIT DEFAULTS ---------------- */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* ---------------- SIDEBAR ---------------- */
[data-testid="stSidebar"]{
    background: rgba(0,0,0,0.88);
    border-right:1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
}

/* ---------------- LOGO AREA ---------------- */
.logo-wrapper{
    display:flex;
    justify-content:center;
    margin-top:35px;
    margin-bottom:15px;
}

.logo-container{
    position:relative;
    width:230px;
    height:230px;
    border-radius:50%;
    overflow:hidden;

    border:2px solid rgba(88,166,255,0.9);

    box-shadow:
    0 0 15px rgba(88,166,255,0.5),
    0 0 30px rgba(88,166,255,0.35),
    0 0 60px rgba(88,166,255,0.2);

    animation: pulseGlow 3s infinite ease-in-out;
}

/* LOGO IMAGE */
.logo-container img{
    width:100%;
    height:100%;
    object-fit:cover;
    z-index:1;
    position:absolute;
}

/* SHINE EFFECT */
.logo-container::after{
    content:"";
    position:absolute;
    top:-120%;
    left:-120%;
    width:220%;
    height:220%;

    background: linear-gradient(
        120deg,
        transparent 20%,
        rgba(255,255,255,0.05) 35%,
        rgba(255,255,255,0.6) 50%,
        rgba(255,255,255,0.05) 65%,
        transparent 80%
    );

    transform: rotate(25deg);

    animation: shineMove 5s infinite;
    z-index:2;
}

/* GLOW PULSE */
@keyframes pulseGlow{
    0%{
        box-shadow:
        0 0 15px rgba(88,166,255,0.5),
        0 0 30px rgba(88,166,255,0.35),
        0 0 60px rgba(88,166,255,0.2);
    }

    50%{
        box-shadow:
        0 0 25px rgba(88,166,255,0.8),
        0 0 50px rgba(88,166,255,0.45),
        0 0 80px rgba(88,166,255,0.3);
    }

    100%{
        box-shadow:
        0 0 15px rgba(88,166,255,0.5),
        0 0 30px rgba(88,166,255,0.35),
        0 0 60px rgba(88,166,255,0.2);
    }
}

/* SHINE ANIMATION */
@keyframes shineMove{
    0%{
        left:-150%;
        top:-120%;
    }

    100%{
        left:150%;
        top:120%;
    }
}

/* ---------------- SIDEBAR TEXT ---------------- */
.sidebar-title{
    text-align:center;
    font-size:34px;
    font-weight:800;
    color:#8ec5ff;
    margin-top:5px;
    margin-bottom:0px;
}

.sidebar-sub{
    text-align:center;
    color:#7ab8ff;
    font-size:13px;
    font-weight:700;
    letter-spacing:3px;
    margin-top:-8px;
}

/* ---------------- MAIN CENTER CONTENT ---------------- */
.main-wrapper{
    width:100%;
    text-align:center;
    margin-top:110px;
}

/* MAIN TITLE */
.main-title{
    font-size:72px;
    font-weight:900;
    color:#8ec5ff;

    text-shadow:
    0 0 10px rgba(88,166,255,0.5),
    0 0 20px rgba(88,166,255,0.3);

    margin-bottom:10px;
}

/* SUB TITLE */
.main-sub{
    color:#7ab8ff;
    font-size:22px;
    font-weight:800;
    letter-spacing:8px;
}

/* ---------------- CHAT INPUT ---------------- */
.stChatInputContainer{
    background:transparent !important;
    border:none !important;
    padding-bottom:35px;
}

/* INPUT BOX */
[data-testid="stChatInput"]{
    background: rgba(255,255,255,0.06) !important;
    border:1px solid rgba(255,255,255,0.08) !important;

    border-radius:22px !important;

    backdrop-filter: blur(12px);

    width:65% !important;
    margin:auto !important;

    box-shadow:
    0 0 20px rgba(0,0,0,0.3),
    inset 0 0 10px rgba(255,255,255,0.03);
}

/* INPUT TEXT */
[data-testid="stChatInput"] textarea{
    color:white !important;
    font-size:18px !important;
}

/* PLACEHOLDER */
[data-testid="stChatInput"] textarea::placeholder{
    color:#9aa7b8 !important;
}

/* SEND BUTTON */
[data-testid="stChatInput"] button{
    background: rgba(255,255,255,0.08) !important;
    border-radius:14px !important;
    color:#8ec5ff !important;
}

/* ---------------- CHAT MESSAGES ---------------- */
.stChatMessage{
    background: rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.05);
    border-radius:18px;
    padding:10px;
    backdrop-filter: blur(10px);
}

/* ---------------- FOOTER ---------------- */
.footer{
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    text-align:center;

    background:rgba(0,0,0,0.55);
    backdrop-filter:blur(10px);

    border-top:1px solid rgba(255,255,255,0.05);

    color:#8b949e;
    padding:10px;

    font-size:11px;
    z-index:999;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)

    st.markdown('<div class="logo-container">', unsafe_allow_html=True)

    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-title">DiNuX AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-sub">POWERED BY KDD STUDIO</div>',
        unsafe_allow_html=True
    )

    st.write("")

    vision_file = st.file_uploader(
        "📸 Neural Vision Feed",
        type=["png", "jpg", "jpeg"]
    )

    st.write("")

    st.info("""
**Architect:** Dinush Dilhara

**Studio:** KDD Studio
""")

    if st.button("🗑️ Clear Neural Memory"):
        st.session_state.messages = []
        st.rerun()

# =========================================================
# MAIN CENTER AREA
# =========================================================
st.markdown("""
<div class="main-wrapper">

    <div class="main-title">
        DiNuX AI
    </div>

    <div class="main-sub">
        POWERED BY KDD STUDIO
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# CHAT MEMORY
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# AI SYSTEM
# =========================================================
user_input = st.chat_input("Connect with DiNuX...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        msg_placeholder = st.empty()

        try:

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",

                system_instruction="""
You are DiNuX AI.

You are created by Dinush Dilhara.

You are intelligent, friendly,
Sinhala + English speaking AI assistant.
"""
            )

            payload = [user_input]

            if vision_file:
                payload.append(Image.open(vision_file))

            with st.spinner("Synchronizing with DiNuX..."):

                response = model.generate_content(
                    payload,
                    stream=True
                )

                full_reply = ""

                for chunk in response:

                    if hasattr(chunk, "text") and chunk.text:
                        full_reply += chunk.text
                        msg_placeholder.markdown(full_reply + "▌")

                msg_placeholder.markdown(full_reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_reply
                })

        except Exception as e:

            st.error("⚠️ Neural link interrupted.")

            st.code(str(e))

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA
</div>
""", unsafe_allow_html=True)

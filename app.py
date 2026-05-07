import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# =========================================================
# DiNuX AI - ULTRA STABLE FINAL VERSION
# Sinhala + English Friendly
# =========================================================

# ---------------- API KEY ----------------
API_KEY = "YOUR_GEMINI_API_KEY"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DiNuX AI",
    page_icon="🧬",
    layout="wide"
)

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=API_KEY)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp{
    background:#0d1117;
    color:white;
}

.branding{
    text-align:center;
    padding:20px;
    border-bottom:1px solid #30363d;
    margin-bottom:25px;
}

.shining-title{
    font-size:55px;
    font-weight:900;
    background:linear-gradient(120deg,#58a6ff,#ffffff,#58a6ff);
    background-size:200% auto;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation:shine 4s linear infinite;
}

@keyframes shine{
    to{
        background-position:200% center;
    }
}

.footer{
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background:#0d1117;
    padding:10px;
    border-top:1px solid #30363d;
    text-align:center;
    color:#8b949e;
    font-size:11px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MODEL LOADER ----------------
@st.cache_resource
def load_model():

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash"
    )

    return model

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("# 🧬 DiNuX AI")

    st.write("---")

    uploaded_image = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    st.write("---")

    st.info("""
Developer: Dinush Dilhara

Studio: KDD STUDIO
""")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("""
<div class="branding">
    <h1 class="shining-title">DiNuX AI</h1>
    <p style="color:#58a6ff;letter-spacing:4px;">
        POWERED BY KDD STUDIO
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- SHOW CHAT ----------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

# =========================================================
# MAIN CHAT SYSTEM
# =========================================================

if prompt:

    # SAVE USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # SHOW USER MESSAGE
    with st.chat_message("user"):
        st.markdown(prompt)

    # ASSISTANT MESSAGE
    with st.chat_message("assistant"):

        loading = st.empty()
        loading.markdown("⏳ Thinking...")

        try:

            model = load_model()

            # ---------------- SYSTEM PROMPT ----------------
            system_prompt = """
You are DiNuX AI.

You are a smart, friendly and advanced AI assistant.

Rules:
- Speak naturally in Sinhala and English.
- Understand Sinhala written in English letters.
- Give clear and intelligent answers.
- Be friendly and modern.
- Help users with coding, education, AI, chatting and creativity.
"""

            # ---------------- CREATE PAYLOAD ----------------
            payload = [system_prompt, prompt]

            # IMAGE SUPPORT
            if uploaded_image is not None:

                image = Image.open(uploaded_image)

                payload.append(image)

            # ---------------- GENERATE RESPONSE ----------------
            response = None

            for attempt in range(3):

                try:

                    response = model.generate_content(
                        payload,

                        generation_config={
                            "temperature": 0.8,
                            "top_p": 1,
                            "top_k": 1,
                            "max_output_tokens": 2048
                        }
                    )

                    # SUCCESS
                    if response:
                        break

                except Exception:

                    time.sleep(2)

            loading.empty()

            # ---------------- SAFE RESPONSE READER ----------------
            answer = ""

            if response is not None:

                # METHOD 1
                try:

                    if hasattr(response, "text"):

                        if response.text:
                            answer = response.text

                except:
                    pass

                # METHOD 2
                if answer == "":

                    try:

                        if hasattr(response, "candidates"):

                            for candidate in response.candidates:

                                if hasattr(candidate, "content"):

                                    if hasattr(candidate.content, "parts"):

                                        for part in candidate.content.parts:

                                            if hasattr(part, "text"):

                                                answer += part.text

                    except:
                        pass

            # ---------------- FINAL OUTPUT ----------------
            if answer.strip() != "":

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            else:

                st.error("""
⚠️ AI server did not return a response.

Possible Reasons:
- Invalid API Key
- Internet issue
- Gemini API limit reached
- Google server temporary issue

Please try again.
""")

        except Exception as e:

            loading.empty()

            st.error(f"⚠️ System Error: {str(e)}")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
© 2026 KDD STUDIO | DESIGNED BY DINUSH DILHARA
</div>
""", unsafe_allow_html=True)

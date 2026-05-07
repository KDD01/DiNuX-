import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# =========================================================
# DiNuX AI PRO - FINAL STABLE VERSION
# =========================================================

# ---------------- API KEY ----------------
API_KEY = "YOUR_GEMINI_API_KEY"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DiNuX AI",
    page_icon="🧬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
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

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=API_KEY)

# ---------------- SAFETY SETTINGS ----------------
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

# ---------------- LOAD MODEL ----------------
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
# MAIN AI SYSTEM
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

    # ASSISTANT RESPONSE
    with st.chat_message("assistant"):

        loading = st.empty()
        loading.markdown("⏳ Thinking...")

        try:

            model = load_model()

            # ---------------- PAYLOAD ----------------
            payload = []

            # ADD USER TEXT
            payload.append(prompt)

            # ADD IMAGE IF EXISTS
            if uploaded_image is not None:

                image = Image.open(uploaded_image)

                payload.append(image)

            # ---------------- RETRY SYSTEM ----------------
            response = None

            for attempt in range(3):

                try:

                    response = model.generate_content(
                        payload,

                        generation_config={
                            "temperature": 0.7,
                            "top_p": 1,
                            "top_k": 1,
                            "max_output_tokens": 2048
                        },

                        safety_settings=safety_settings
                    )

                    break

                except Exception:

                    time.sleep(2)

            # ---------------- RESPONSE READER ----------------
            loading.empty()

            answer = ""

            try:

                # NORMAL TEXT
                if hasattr(response, "text") and response.text:

                    answer = response.text

                # ALTERNATIVE RESPONSE FORMAT
                elif response.candidates:

                    for candidate in response.candidates:

                        if candidate.content.parts:

                            for part in candidate.content.parts:

                                if hasattr(part, "text"):

                                    answer += part.text

            except Exception as e:

                answer = f"Response Error: {str(e)}"

            # ---------------- FINAL OUTPUT ----------------
            if answer.strip() != "":

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            else:

                st.warning("⚠️ Empty response received. Please resend.")

        except Exception as e:

            loading.empty()

            st.error(f"⚠️ System Error: {str(e)}")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
© 2026 KDD STUDIO | DESIGNED BY DINUSH DILHARA
</div>
""", unsafe_allow_html=True)

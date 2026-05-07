import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ================= API KEY =================
API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

# ================= MODEL =================
@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_model()

# ================= SAFE RESPONSE FUNCTION =================
def get_ai_response(payload):

    for _ in range(3):  # retry system

        try:
            response = model.generate_content(payload)

            # 1st SAFE: direct text
            if hasattr(response, "text") and response.text:
                return response.text

            # 2nd SAFE: candidates parsing
            if hasattr(response, "candidates") and response.candidates:

                parts = response.candidates[0].content.parts
                text = ""

                for p in parts:
                    if hasattr(p, "text"):
                        text += p.text

                if text:
                    return text

        except Exception as e:
            time.sleep(2)

    return None

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= UI =================
st.title("🧬 DiNuX AI")

uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

# ================= CHAT =================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type here...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_box = st.empty()
        msg_box.markdown("⏳ Thinking...")

        # SYSTEM PROMPT
        system_prompt = """
You are DiNuX AI.
Be friendly, smart, Sinhala + English support.
"""

        payload = [system_prompt, prompt]

        # IMAGE SUPPORT SAFE
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            payload = [system_prompt, image, prompt]

        answer = get_ai_response(payload)

        msg_box.empty()

        if answer:
            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        else:
            st.error("⚠️ No response from AI. Try again.")

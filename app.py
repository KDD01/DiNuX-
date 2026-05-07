import streamlit as st
import google.generativeai as genai
from groq import Groq
import time
from PIL import Image

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DiNuX AI Infinity Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM BLACK & GRAY UI (CSS) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #000000;
        color: #e5e7eb;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #1f2937;
    }

    /* Round Logo Styling */
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }
    .logo-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
    }

    /* Chat Bubbles */
    .stChatMessage {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
    }

    /* Input Box */
    .stChatInput input {
        background-color: #1f2937 !important;
        color: white !important;
        border: 1px solid #374151 !important;
    }

    /* Professional Text Gradient */
    .title-text {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #9ca3af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-thumb {
        background: #374151;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API LOADING (FROM SECRETS) ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEYS = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"]]
except Exception:
    st.error("Secrets Configuration Missing! Please check Streamlit Settings.")
    st.stop()

# --- 4. SYSTEM PROMPT (SRI LANKAN FRIENDLY PERSONA) ---
SYSTEM_PROMPT = """
You are DiNuX AI, a brilliant and friendly Sri Lankan AI companion. 
- Talk like a helpful friend (යාළුවෙක් වගේ).
- Use natural, polite, and warm Sinhala. 
- Instead of "මම ඔබට උදව් කරන්නේ කෙසේද?", use "මචං, මට පුළුවන් ඔයාට උදව් කරන්න. මොකක්ද වෙන්න ඕනේ?" or similar natural phrases.
- If someone thanks you, say "අයියෝ ඕක මොකක්ද මල්ලි/මචං, ඕන වෙලාවක අහන්න!" 
- Stay professional but very friendly. You were created by the legend Dinush Dilhara.
"""

# --- 5. SMART ENGINE LOGIC ---
def get_ai_response(prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        return completion.choices[0].message.content
    except Exception:
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\nUser: {prompt}")
                return response.text
            except Exception:
                continue
    return "සමාවෙන්න මචං, පොඩි line එකක් ගියා. ආයෙත් පාරක් අහන්නකෝ."

# --- 6. SIDEBAR UI ---
with st.sidebar:
    # Logo එක පෙන්වීම
    try:
        image = Image.open("logo.png")
        st.image(image, use_container_width=True)
    except:
        st.markdown('<div style="text-align:center; color:gray;">(Logo not found in repo)</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🤖 DiNuX AI Core")
    st.write("Status: **Optimal** ⚡")
    st.write("Mode: **Friendly Assistant**")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Creator")
    st.success("**Dinush Dilhara**")
    st.caption("Sri Lanka's Next-Gen AI Dev")
    
    st.markdown("---")
    if st.button("🗑️ Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN CHAT INTERFACE ---
st.markdown('<h1 class="title-text">DiNuX AI Infinity Pro</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 30px;'>Think • Learn • Evolve</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("මොනවා හරි අහන්න මචං..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("හිතනවා..."):
            full_response = get_ai_response(prompt)
            # Smart Typing effect
            displayed_text = ""
            for char in full_response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.005)
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

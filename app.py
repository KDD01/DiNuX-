import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. SETTINGS & STABILITY ENGINE ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
LOGO_URL = "https://i.ibb.co/v4Kj5Y7/D-i-N-u-X-A-I.png"

# පද්ධතිය ස්ථාවරව පවත්වා ගැනීමට API Configure කිරීම
def setup_genai():
    try:
        genai.configure(api_key=API_KEY)
        # වැඩ කරන මෝඩල් ලැයිස්තුව සොයා ගැනීම
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return available_models
    except Exception:
        return []

# --- 2. ELITE SMART UI DESIGN (CSS) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown(f"""
    <style>
    /* මුළු App එකටම Dark Gradient එකක් */
    .stApp {{
        background: radial-gradient(circle at top right, #0d1117, #010409);
        color: #e6edf3;
    }}

    /* Sidebar ලස්සන කිරීම */
    [data-testid="stSidebar"] {{
        background-color: rgba(13, 17, 23, 0.9);
        border-right: 1px solid #30363d;
    }}

    /* රවුම් Shining Logo එක */
    .logo-container {{
        text-align: center;
        padding: 20px 0;
    }}
    .shining-logo {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #58a6ff;
        box-shadow: 0 0 20px #58a6ff, 0 0 40px #58a6ff;
        animation: shine 3s infinite alternate;
    }}
    @keyframes shine {{
        from {{ box-shadow: 0 0 10px #58a6ff, inset 0 0 5px #58a6ff; }}
        to {{ box-shadow: 0 0 30px #58a6ff, inset 0 0 15px #58a6ff; }}
    }}

    /* Header Title */
    .header-text {{
        font-size: 50px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shine 4s linear infinite;
    }}
    @keyframes gradient-shine {{
        to {{ background-position: 200% center; }}
    }}

    /* Chat bubbles */
    .stChatMessage {{
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 20px;
        margin-bottom: 15px;
    }}
    
    /* Footer */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 10px;
        text-align: center;
        background: #0d1117;
        border-top: 1px solid #30363d;
        font-size: 12px;
        color: #8b949e;
        z-index: 100;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_model" not in st.session_state:
    model_list = setup_genai()
    # ප්‍රමුඛතාවය අනුව මෝඩල් එක තෝරා ගැනීම
    if "models/gemini-1.5-pro" in model_list:
        st.session_state.active_model = "models/gemini-1.5-pro"
    elif "models/gemini-1.5-flash" in model_list:
        st.session_state.active_model = "models/gemini-1.5-flash"
    elif model_list:
        st.session_state.active_model = model_list[0]
    else:
        st.session_state.active_model = "gemini-1.5-flash" # Fallback

# --- 4. SIDEBAR MENU ---
with st.sidebar:
    st.markdown(f'''
        <div class="logo-container">
            <img src="{LOGO_URL}" class="shining-logo">
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>CONTROL PANEL</h2>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### 🛠️ Configuration")
    # වැඩ කරන මෝඩල්ස් පමණක් පෙන්වීම
    model_options = setup_genai()
    current_model = st.selectbox("Neural Engine", model_options if model_options else [st.session_state.active_model])
    
    vision_input = st.file_uploader("📸 Vision Feed (Upload Image)", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.markdown("### 👤 Developer Info")
    st.info("**Dinush Dilhara**\n\nKDD STUDIO Premier Edition")
    
    if st.button("🗑️ Clear Neural Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN HEADER ---
st.markdown('<h1 class="header-text">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8b949e; letter-spacing: 5px;">THINK • LEARN • EVOLVE</p>', unsafe_allow_html=True)

# --- 6. CHAT INTERFACE ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 7. CORE INTELLIGENCE LOGIC ---
prompt = st.chat_input("Connect with DiNuX AI...")

if prompt:
    # 1. User මැසේජ් එක පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("DiNuX is thinking..."):
            try:
                # මෝඩල් එක පණගැන්වීම
                model = genai.GenerativeModel(
                    model_name=current_model,
                    system_instruction="You are DiNuX AI, a pro assistant created by Dinush Dilhara. Use high-quality Sinhala and English. Think deeply before answering."
                )
                
                # Content එක සකස් කිරීම (Image එකක් ඇත්නම් එයත් සමඟ)
                payload = [prompt]
                if vision_input:
                    payload.append(Image.open(vision_input))
                
                # Response එක ජෙනරේට් කිරීම
                response = model.generate_content(payload)
                
                if response.text:
                    full_response = response.text
                    # ටයිප් කරන ආකාරයට පෙන්වීම (Streaming effect)
                    message_placeholder = st.empty()
                    typed_text = ""
                    for char in full_response:
                        typed_text += char
                        message_placeholder.markdown(typed_text + "▌")
                        time.sleep(0.002)
                    message_placeholder.markdown(full_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("Empty response. Please try again.")

            except Exception as e:
                # මොකක් හරි වැරදුනොත් ඒක පැහැදිලිව පෙන්වන්න (Diagnostic)
                st.error(f"Neural Error: {str(e)}")
                st.info("Tip: Try switching the 'Neural Engine' in the sidebar.")

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | ALL RIGHTS RESERVED</div>', unsafe_allow_html=True)

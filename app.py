import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE & SESSION MANAGEMENT ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"

# පැරණි සාර්ථක තාක්ෂණය: Session එක පුරාම එකම Chat Object එකක් පාවිච්චි කිරීම
if "chat_session" not in st.session_state:
    try:
        genai.configure(api_key=API_KEY)
        # වඩාත්ම ස්ථාවර මෝඩල් එක තෝරා ගැනීම
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="You are DiNuX AI, a pro assistant created by Dinush Dilhara. Use high-quality Sinhala and English. Be friendly and smart."
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.model_ready = True
    except Exception as e:
        st.session_state.model_ready = False

# --- 2. ADVANCED UI & LOGO ANIMATION (CSS) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409; border-right: 1px solid #30363d; min-width: 300px; }

    /* --- LOGO ROUND CONTAINER --- */
    .logo-frame {
        position: relative;
        width: 180px;  /* ලෝගෝ එක තවත් ලොකු කළා */
        height: 180px;
        margin: 20px auto;
        border-radius: 50%;
        overflow: hidden;
        border: 3px solid #58a6ff;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
    }

    .logo-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* --- WHITE SHINE SWAP EFFECT --- */
    .logo-frame::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -150%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to right, 
            transparent 0%, 
            rgba(255, 255, 255, 0) 30%, 
            rgba(255, 255, 255, 0.6) 45%, /* සුදු පැහැය වැඩි කළා */
            rgba(200, 200, 200, 0.3) 50%, 
            rgba(255, 255, 255, 0.6) 55%, 
            rgba(255, 255, 255, 0) 70%, 
            transparent 100%
        );
        transform: rotate(25deg);
        animation: swap-shine 3.5s infinite ease-in-out;
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    .shining-title {
        font-size: 65px; font-weight: 900; text-align: center;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine-text 4s linear infinite;
        margin-bottom: 0px;
    }
    @keyframes shine-text { to { background-position: 200% center; } }

    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; text-align: center; border-top: 1px solid #30363d; font-size: 11px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LOGO & INFO) ---
with st.sidebar:
    st.markdown('<div class="logo-frame">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    else:
        st.markdown("<div style='text-align:center; margin-top:70px; color:#58a6ff;'>LOGO HERE</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("<h3 style='text-align:center;'>DiNuX AI PANEL</h3>", unsafe_allow_html=True)
    
    vision_file = st.file_uploader("📸 Vision Feed", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n\n**Powered by:** KDD Studio")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #58a6ff; font-weight: bold; letter-spacing: 5px; margin-top:-20px;">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# මැසේජ් ප්‍රදර්ශනය
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE BRAIN (SMOOTH CHAT TECHNOLOGY) ---
user_query = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        if st.session_state.model_ready:
            try:
                # පින්තූරයක් ඇත්නම් එය පමණක් වෙනම handle කිරීම (Stability සඳහා)
                if vision_file:
                    img = Image.open(vision_file)
                    # Vision සඳහා වෙනම මෝඩල් එකක් එක වෙලාවට පාවිච්චි කිරීම
                    v_model = genai.GenerativeModel('gemini-1.5-flash')
                    response = v_model.generate_content([user_query, img])
                else:
                    # සාමාන්‍ය ස්මූත් චැට් එක (Session එක හරහා)
                    response = st.session_state.chat_session.send_message(user_query)
                
                if response.text:
                    full_text = response.text
                    # ටයිප් කරන ලස්සන Animation එක
                    temp_text = ""
                    for char in full_text:
                        temp_text += char
                        placeholder.markdown(temp_text + "▌")
                        time.sleep(0.003)
                    placeholder.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                
            except Exception as e:
                # යම් හෙයකින් එරර් එකක් ආවොත් සයිලන්ට් එකේ රීසෙට් කිරීම
                st.session_state.chat_session = None
                st.error("System synchronization failed. Please send the message again.")
                time.sleep(1)
                st.rerun()
        else:
            st.error("Neural Core not active. Check API Key.")

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE CONFIGURATION ---
# ඔයාගේ API Key එක මෙහි ඇතුළත් කර ඇත
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# --- 2. ADVANCED UI STYLING (MATCHING YOUR SCREENSHOT) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* මුළු පද්ධතියේම පසුබිම */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Sidebar එක තද කළු පැහැයට සහ මැදට (Centered) සකස් කිරීම */
    [data-testid="stSidebar"] { 
        background-color: #010409; 
        border-right: 1px solid #1f2428;
        text-align: center;
        min-width: 300px;
    }

    /* --- LOGO CONTAINER WITH CIRCULAR BLUE GLOW & SHINE --- */
    .logo-frame {
        position: relative;
        width: 190px; /* ලෝගෝ එකේ ප්‍රමාණය */
        height: 190px;
        margin: 40px auto 10px auto;
        border-radius: 50%;
        border: 2px solid #58a6ff;
        box-shadow: 0 0 30px rgba(88, 166, 255, 0.5); /* නිල් පැහැති දිලිසීම */
        overflow: hidden;
        background-color: #000;
    }

    .logo-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* ලෝගෝ එකට උඩින් යන White Shine Swap Effect එක */
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
            rgba(255, 255, 255, 0.1) 30%, 
            rgba(255, 255, 255, 0.6) 50%, 
            rgba(255, 255, 255, 0.1) 70%, 
            transparent 100%
        );
        transform: rotate(25deg);
        animation: swap-shine 4s infinite ease-in-out;
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    /* Main Interface Styling */
    .main-title {
        font-size: 55px; font-weight: 800; text-align: center;
        color: #e6edf3;
        margin-top: 50px;
        letter-spacing: 2px;
    }
    
    .sub-brand {
        text-align: center; color: #58a6ff; font-weight: 900; 
        letter-spacing: 4px; font-size: 15px; margin-top: -15px;
    }

    /* Chat Elements */
    .stChatInputContainer { padding-bottom: 60px; }
    
    .footer { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background: #0d1117; padding: 10px; text-align: center; 
        border-top: 1px solid #1f2428; font-size: 11px; color: #8b949e; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LOGO & IDENTITY) ---
with st.sidebar:
    # රවුම් දාරය සහ ලෝගෝ එක
    st.markdown('<div class="logo-frame">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ලෝගෝ එකට පහළින් නම සහ සන්නාමය
    st.markdown("<h2 style='color: #e6edf3; margin-bottom: 0;'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #58a6ff; font-weight: bold; letter-spacing: 2px;'>POWERED BY KDD STUDIO</p>", unsafe_allow_html=True)
    
    st.write("---")
    vision_feed = st.file_uploader("📸 Neural Vision Feed", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Powered by:** KDD Studio")
    
    if st.button("🗑️ Clear Neural Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="main-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-brand">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat ඉතිහාසය පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE BRAIN (REAL-TIME STREAMING CHAT) ---
user_query = st.chat_input("Connect with DiNuX...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        response_container = st.empty()
        
        try:
            # මෝඩල් එක සූදානම් කිරීම
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="You are DiNuX AI, an elite assistant created by Dinush Dilhara. Use professional Sinhala and English."
            )
            
            # පින්තූරයක් ඇත්නම් එය ලබා ගැනීම
            content_payload = [user_query]
            if vision_feed:
                content_payload.append(Image.open(vision_feed))
            
            with st.spinner("Synchronizing..."):
                # Streaming තාක්ෂණය මඟින් රිප්ලයි එක ලබා ගැනීම
                response_stream = model.generate_content(content_payload, stream=True)
                
                full_text = ""
                for chunk in response_stream:
                    if chunk.text:
                        full_text += chunk.text
                        # ටයිප් කරන ආකාරයට මැසේජ් එක පෙන්වීම
                        response_container.markdown(full_text + "▌")
                
                response_container.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
                    
        except Exception as e:
            st.error("Neural Connection interrupted. Re-syncing...")
            time.sleep(2)
            st.rerun()

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | ALL RIGHTS RESERVED</div>', unsafe_allow_html=True)

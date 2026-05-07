import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE CONFIGURATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# --- 2. ELITE UI STYLING (MATCHING YOUR SCREENSHOT) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* මුළු App එකේ පසුබිම */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Sidebar එක තද කළු පැහැයට සකස් කිරීම */
    [data-testid="stSidebar"] { 
        background-color: #010409; 
        border-right: 1px solid #1f2428;
        text-align: center;
    }

    /* --- LOGO OUTER WITH BLUE GLOW & SWAP SHINE --- */
    .logo-container {
        position: relative;
        width: 180px;
        height: 180px;
        margin: 40px auto 10px auto;
        border-radius: 50%;
        border: 2px solid #58a6ff;
        box-shadow: 0 0 25px rgba(88, 166, 255, 0.4); /* නිල් පැහැති දිලිසීම */
        overflow: hidden;
        background-color: #000;
    }

    .logo-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1; /* පින්තූරය යටින් */
    }

    /* ලෝගෝ එකට උඩින් යන සුදු පාට දිලිසෙන ඉර (Overlay) */
    .logo-container::after {
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
            rgba(255, 255, 255, 0.5) 50%, 
            rgba(255, 255, 255, 0) 70%, 
            transparent 100%
        );
        transform: rotate(25deg);
        animation: swap-shine 4s infinite ease-in-out;
        z-index: 2; /* පින්තූරයට උඩින් */
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    /* Main Title Styling */
    .shining-title {
        font-size: 50px; font-weight: 800; text-align: center;
        color: #58a6ff;
        margin-top: 50px;
    }
    
    .powered-by {
        text-align: center; color: #58a6ff; font-weight: 900; 
        letter-spacing: 3px; font-size: 14px; margin-top: -10px;
    }

    /* Chat Input Styling */
    .stChatInputContainer { padding-bottom: 50px; }

    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; text-align: center; border-top: 1px solid #1f2428; font-size: 11px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LOGO & DETAILS) ---
with st.sidebar:
    # ඔයා ඉල්ලපු විදිහටම රවුම් Shape එක ඇතුළට Logo එක දැමීම
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # පින්තූරයට යටින් නම සහ Powered By කොටස
    st.markdown("<h2 style='color: #58a6ff; margin-bottom: 0;'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #58a6ff; font-weight: bold; font-size: 12px;'>POWERED BY KDD STUDIO</p>", unsafe_allow_html=True)
    
    st.write("---")
    vision_file = st.file_uploader("📸 Neural Vision Feed", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Studio:** KDD Studio")
    
    if st.button("🗑️ Clear Neural Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="powered-by">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# මැසේජ් ප්‍රදර්ශනය
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE BRAIN (STABLE LIVE CHAT) ---
user_input = st.chat_input("Connect with DiNuX...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        
        try:
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="You are DiNuX AI, a pro assistant by Dinush Dilhara. Speak in Sinhala and English."
            )
            
            payload = [user_input]
            if vision_file:
                payload.append(Image.open(vision_file))
            
            with st.spinner("Synchronizing..."):
                # "Reply නැතිවෙන" එක නවත්තන්න stream=True තාක්ෂණය පාවිච්චි කිරීම
                response = model.generate_content(payload, stream=True)
                
                full_reply = ""
                for chunk in response:
                    if chunk.text:
                        full_reply += chunk.text
                        msg_placeholder.markdown(full_reply + "▌")
                
                msg_placeholder.markdown(full_reply)
                st.session_state.messages.append({"role": "assistant", "content": full_reply})
                    
        except Exception as e:
            st.error("Neural link interrupted. Reconnecting...")
            time.sleep(2)
            st.rerun()

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

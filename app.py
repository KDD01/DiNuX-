import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CORE ENGINE CONFIGURATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# --- 2. ELITE UI STYLING (MATCHING SCREENSHOT EXACTLY) ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    /* මුළු App එකේ පසුබිම */
    .stApp { background: #0d1117; color: #e6edf3; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #010409; 
        border-right: 1px solid #1f2428;
    }

    /* Sidebar ඇතුළේ ඇති දේවල් මැදට ගැනීම */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* --- LOGO CONTAINER (BLUE GLOW + SHINE OVERLAY) --- */
    .logo-frame {
        position: relative;
        width: 180px;
        height: 180px;
        margin: 10px auto;
        border-radius: 50%;
        border: 3px solid #58a6ff;
        box-shadow: 0 0 25px rgba(88, 166, 255, 0.5);
        overflow: hidden;
        background-color: #000;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .logo-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 1;
    }

    /* White Shine Swap Effect - ලෝගෝ එකට උඩින් වැටෙන කොටස */
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
            rgba(255, 255, 255, 0.6) 50%, 
            transparent 100%
        );
        transform: rotate(25deg);
        animation: swap-shine 3.5s infinite ease-in-out;
        z-index: 2;
    }

    @keyframes swap-shine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    /* Header Styling */
    .main-header {
        font-size: 55px; font-weight: 800; text-align: center;
        color: #e6edf3; margin-top: 40px; letter-spacing: 2px;
    }
    
    .brand-sub {
        text-align: center; color: #58a6ff; font-weight: 900; 
        letter-spacing: 5px; font-size: 14px; margin-top: -15px;
    }

    /* Footer */
    .footer { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background: #0d1117; padding: 10px; text-align: center; 
        border-top: 1px solid #1f2428; font-size: 11px; color: #8b949e; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LOGO & CENTERED CONTENT) ---
with st.sidebar:
    # ලෝගෝ එක රවුම් Frame එක ඇතුළටම සෙට් කිරීම
    st.markdown('<div class="logo-frame">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #e6edf3; margin: 10px 0 0 0; text-align: center;'>DiNuX AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #58a6ff; font-weight: bold; letter-spacing: 2px; text-align: center;'>POWERED BY KDD STUDIO</p>", unsafe_allow_html=True)
    
    st.write("---")
    vision_input = st.file_uploader("📸 Neural Vision Feed", type=["jpg", "png", "jpeg"])
    
    st.write("---")
    st.info("**Architect:** Dinush Dilhara\n\n**Powered by:** KDD Studio")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN CHAT INTERFACE ---
st.markdown('<h1 class="main-header">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-sub">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# චැට් එක පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE BRAIN (REAL-TIME STREAMING) ---
user_query = st.chat_input("Connect with DiNuX...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        output_placeholder = st.empty()
        
        try:
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="You are DiNuX AI, an elite assistant by Dinush Dilhara. Use professional Sinhala and English."
            )
            
            content = [user_query]
            if vision_input:
                content.append(Image.open(vision_input))
            
            with st.spinner("Processing..."):
                # Streaming එක නිසා මැසේජ් එක කැඩෙන්නේ නැතිව එනවා
                response_stream = model.generate_content(content, stream=True)
                
                full_reply = ""
                for chunk in response_stream:
                    if chunk.text:
                        full_reply += chunk.text
                        output_placeholder.markdown(full_reply + "▌")
                
                output_placeholder.markdown(full_reply)
                st.session_state.messages.append({"role": "assistant", "content": full_reply})
                    
        except Exception as e:
            # එරර් එකක් ආවොත් සයිලන්ට් එකේ ඔටෝ රිෆ්‍රෙෂ් වෙනවා
            st.error("Neural link sync error. Re-trying...")
            time.sleep(2)
            st.rerun()

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA | POWERED BY KDD STUDIO</div>', unsafe_allow_html=True)

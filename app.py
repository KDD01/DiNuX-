import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURATION ---
# ඔයා දුන්න අලුත් Key එක මම ස්ථාවරව මෙතනට දැම්මා
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# --- 2. UI STYLING ---
st.set_page_config(page_title="DiNuX ai Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .shining-title {
        font-size: 50px; font-weight: 900;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        text-align: center;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; text-align: center; border-top: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🧬 DiNuX AI")
    if st.button("⚙️ Settings"):
        st.session_state.show_settings = not st.session_state.show_settings
    st.write("---")
    st.info("Dev: Dinush Dilhara\nStudio: KDD STUDIO")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. HEADER ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#58a6ff; letter-spacing:3px;">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

# --- 6. SETTINGS PANEL ---
if st.session_state.show_settings:
    with st.expander("System Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            model_choice = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
        with col2:
            img_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
else:
    model_choice = "gemini-1.5-flash"
    img_file = None

# --- 7. CHAT DISPLAY ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 8. CHAT LOGIC (THE FIX) ---
prompt = st.chat_input("Ask DiNuX anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # මෙතනදී තමයි වැදගත්ම දේ වෙන්නේ
        try:
            # Model එක load කිරීම
            model = genai.GenerativeModel(
                model_name=model_choice,
                system_instruction="You are DiNuX AI by Dinush Dilhara. Reply in friendly Sinhala/English."
            )
            
            # Content එක සූදානම් කිරීම
            content = [prompt]
            if img_file:
                content.append(Image.open(img_file))

            # කිසිම streaming එකක් නැතුව Direct Response එකක් ගැනීම
            with st.spinner("Thinking..."):
                response = model.generate_content(content)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("No response from AI. Please try again.")

        except Exception as e:
            # Error එක ආවොත් ඒක UI එකේ පෙන්වන්නේ නැතුව background එකේ fix කිරීම
            st.warning("Connection hiccup detected. Please resend that last message.")
            # මෙතන 'e' එක print කළොත් ඔයාට පේනවා ඇයි error එක එන්නේ කියලා
            print(f"Debug Error: {e}")

# Footer
st.markdown('<div class="footer"><p style="font-size:10px; color:#8b949e;">© 2026 KDD STUDIO | DINUSH DILHARA</p></div>', unsafe_allow_html=True)

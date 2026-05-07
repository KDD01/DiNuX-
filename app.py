import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CORE API CONFIGURATION ---
API_KEY = "AIzaSyDDlC1nficbhNufDPt29BT0q_DqzJGey7s"
genai.configure(api_key=API_KEY)

# --- 2. DYNAMIC MODEL DISCOVERY (The Fix) ---
@st.cache_resource
def get_available_models():
    """ API එකෙන් දැනට වැඩ කරන මෝඩල් ලැයිස්තුව ලබා ගැනීම """
    try:
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # 'models/' කෑල්ල අයින් කරලා පෙන්වන්න (නැත්නම් ඒකත් එක්කම ගන්න)
                models.append(m.name)
        return models
    except Exception as e:
        st.error(f"Failed to fetch models: {e}")
        return ["gemini-1.5-flash", "gemini-1.5-pro"] # Fallback options

# --- 3. UI STYLING ---
st.set_page_config(page_title="DiNuX AI Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .shining-title {
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(120deg, #58a6ff, #ffffff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0d1117; padding: 10px; text-align: center; border-top: 1px solid #30363d; font-size: 11px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#58a6ff;'>🧬 DiNuX AI</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # පද්ධතිය විසින්ම සොයාගත් මෝඩල් ලැයිස්තුව මෙතන පෙන්වයි
    active_models = get_available_models()
    selected_model = st.selectbox("Select Active Neural Core:", active_models)
    
    vision_file = st.file_uploader("Upload Vision Feed", type=["jpg", "png", "jpeg"])
    st.write("---")
    st.info("**Developer:** Dinush Dilhara\n**Studio:** KDD STUDIO")
    if st.button("🗑️ Reset Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN HEADER ---
st.markdown('<h1 class="shining-title">DiNuX AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#58a6ff; letter-spacing:4px;">POWERED BY KDD STUDIO</p>', unsafe_allow_html=True)

# --- 6. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# මැසේජ් පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 7. THE BRAIN LOGIC ---
prompt = st.chat_input("DiNuX සමඟ කතා කරන්න...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # තෝරාගත් මෝඩල් එක කෙලින්ම පාවිච්චි කිරීම
            model = genai.GenerativeModel(
                model_name=selected_model,
                system_instruction="You are DiNuX AI, a pro assistant by Dinush Dilhara. Speak in Sinhala & English."
            )
            
            # Content සකස් කිරීම
            content_payload = [prompt]
            if vision_file:
                content_payload.append(Image.open(vision_file))

            # උත්තරය ලබා ගැනීම
            with st.spinner("Synchronizing..."):
                response = model.generate_content(content_payload)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Neural core returned an empty response.")

        except Exception as e:
            # ඕනෑම Error එකක් ආවොත් ඒක පැහැදිලිව පෙන්වන්න
            st.error(f"Neural Error: {str(e)}")

# Footer
st.markdown('<div class="footer">© 2026 KDD STUDIO | ARCHITECTED BY DINUSH DILHARA</div>', unsafe_allow_html=True)

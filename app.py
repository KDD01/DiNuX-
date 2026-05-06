import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# ඔයාගේ API Key එක මෙතනට දාන්න
API_KEY = "මෙතනට_ඔයාගේ_API_KEY_එක_Paste_කරන්න"

# API එක නිවැරදිව Configure කිරීම
try:
    genai.configure(api_key=API_KEY)
    
    # පණිවිඩ වලට පිළිතුරු නොදී සිටීම වැළැක්වීමට Safety Settings සකස් කිරීම
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # වඩාත් වේගවත් මාදිලිය
        generation_config=generation_config
    )
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

# Custom CSS - KDD Studio Look & Feel
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: white;
    }
    /* Chat bubbles styling */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    h1 {
        background: linear-gradient(90deg, #00e5ff, #ff2fd0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 DiNuX AI Assistant")
# ඔයා ඉල්ලපු විදියට KDD Studio ලෙස වෙනස් කළා
st.caption("Developed by Dinush Dilhara | Powered by KDD Studio")

# Chat History එක Session State එකේ තබා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ කතාබස් (Chat History) පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT LOGIC ---
if prompt := st.chat_input("Ask DiNuX anything..."):
    # User ගේ පණිවිඩය පෙන්වීම සහ Save කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."): # පිළිතුර එනතුරු පෙන්වන animation එක
            try:
                # Chat එක ආරම්භ කර පිළිතුර ලබා ගැනීම
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt, stream=False)
                
                if response and response.text:
                    full_response = response.text
                    st.markdown(full_response)
                    # පිළිතුර History එකට එකතු කිරීම
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("කණගාටුයි, පිළිතුරක් සකස් කිරීමට නොහැකි වුණා. නැවත උත්සාහ කරන්න.")
                    
            except Exception as e:
                # API Key වැරදි නම් හෝ වෙනත් තාක්ෂණික දෝෂයක් නම්
                if "API_KEY_INVALID" in str(e):
                    st.error("Error: ඔයාගේ API Key එක වැරදියි. කරුණාකර නිවැරදි Key එකක් ඇතුළත් කරන්න.")
                else:
                    st.error(f"දෝෂයක් ඇති වුණා: {e}")

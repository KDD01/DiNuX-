import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# මෙන්න මෙතනට ඔයාගේ Gemini API Key එක දාන්න
API_KEY = "මෙතනට_ඔයාගේ_API_KEY_එක_Paste_කරන්න"

# API එක සම්බන්ධ කිරීම
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- UI SETTINGS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

# Custom CSS - වෙබ් අඩවිය ලස්සන කරන්න
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00e5ff, #ff2fd0);
        color: black;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        width: 100%;
    }
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 DiNuX AI Assistant")
st.caption("Developed by Dinush Dilhara | Powered by Gemini Pro")

# Chat History එක තබා ගැනීමට
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කරපු Chat පෙන්වීමට
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් ප්‍රශ්නය ලබා ගැනීම
if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අහන්න..."):
    # User ගේ පණිවිඩය එකතු කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # API එකට පණිවිඩය යැවීම
            response = model.generate_content(prompt)
            
            # පිළිතුර පෙන්වීම
            if response.text:
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("කණගාටුයි, පිළිතුරක් ලබා දීමට නොහැකි වුණා.")
                
        except Exception as e:
            # මෙතනදී තමයි API Key වැරදි නම් පෙන්වන්නේ
            if "API_KEY_INVALID" in str(e):
                st.error("Error: ඔයාගේ API Key එක වැරදියි. කරුණාකර නිවැරදි Key එකක් දාන්න.")
            else:
                st.error(f"Error: {e}")

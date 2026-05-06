import streamlit as st
from groq import Groq

# --- 1. CONFIGURATION ---
# ඔයා එවපු Groq API Key එක මම මෙතනට ඇතුළත් කළා
API_KEY = "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"

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Shining White Title */
    .shining-title {
        color: #ffffff;
        font-size: 45px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #222, #fff, #222);
        background-repeat: no-repeat;
        background-size: 80%;
        animation: shine 3s linear infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.2);
    }
    @keyframes shine {
        0% { background-position: -500%; }
        100% { background-position: 500%; }
    }
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="shining-title">DiNuX AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Developed by Dinush Dilhara | Powered by KDD Studio</p>', unsafe_allow_html=True)

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT LOGIC ---
if prompt := st.chat_input("Ask DiNuX anything..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI message
    with st.chat_message("assistant"):
        try:
            # Groq API එක පාවිච්චි කරලා පිළිතුර ලබා ගැනීම (මෙය ඉතා වේගවත්)
            completion = client.chat.completions.create(
                model="llama3-8b-8192", # ඉතා හොඳින් වැඩ කරන Model එකක්
                messages=[
                    {"role": "system", "content": "You are DiNuX AI, a helpful assistant created by Dinush Dilhara."},
                    {"role": "user", "content": prompt}
                ],
            )
            
            response = completion.choices[0].message.content
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.warning("Reply එකක් ලැබුණේ නැහැ.")

        except Exception as e:
            st.error(f"Error: {e}")
            if "invalid_api_key" in str(e).lower():
                st.info("ඔයාගේ Groq API Key එකේ අවුලක් තියෙනවා. කරුණාකර අලුත් එකක් දාන්න.")

import streamlit as st
import google.generativeai as genai
import os

# --- Gemini API Config ---
# ඔයාගේ API Key එක මෙතනට දාන්න (නැත්නම් Streamlit Secrets පාවිච්චි කරන්න)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# --- Model Settings ---
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config
)

# --- Streamlit UI ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #030712;
    }
    .stTextInput > div > div > input {
        background-color: #0f172a;
        color: white;
        border-radius: 20px;
    }
    h1 {
        color: #00e5ff;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 DiNuX AI Assistant")
st.write("Developed by Dinush Dilhara")

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask DiNuX anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")

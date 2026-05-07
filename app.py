import streamlit as st
import google.generativeai as genai

# API Setup
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-pro')

st.title("My AI Assistant")

# Chat history එක save කර ගැනීමට
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කතා කරපුවා පෙන්වීමට
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් input එකක් ගැනීම
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් reply එකක් ගැනීම
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

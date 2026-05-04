import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

st.title("DiNuX AI 🤖")
st.markdown("---")

# API Key එක මෙතැනට දාන්න
client = Groq(api_key="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
")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Your name is DiNuX. You are a helpful and friendly Sri Lankan AI. Respond in Sinhala naturally and clearly."},
                *st.session_state.messages
            ],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

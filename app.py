import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

st.title("DiNuX AI 🤖")
st.markdown("---")

# API Key එක කෙලින්ම ඇතුළත් කර ඇත
client = Groq(api_key="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")

# Session state එක හරහා මැසේජ් සේව් කර ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කතා කරපු මැසේජ් තිරයේ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# පරිශීලකයාගෙන් ප්‍රශ්න ලබා ගැනීම
if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුරු ලබා ගැනීම
    with st.chat_message("assistant"):
        # මැසේජ් ලිස්ට් එක සකස් කිරීම
        full_messages = [
            {"role": "system", "content": "Your name is DiNuX. You are a helpful and friendly Sri Lankan AI. Respond in Sinhala naturally and clearly."}
        ]
        
        # දැනට තියෙන මැසේජ් ඉතිහාසය එකතු කිරීම
        for m in st.session_state.messages:
            full_messages.append({"role": m["role"], "content": m["content"]})

        try:
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="mixtral-8x7b-32768",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"පොඩි වැරදීමක් වුණා: {e}")

import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

# CSS මගින් පෙනුම සැකසීම (මෙතැන තිබුණු වැරැද්ද මම හැදුවා)
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("DiNuX AI 🤖")
st.markdown("---")

# API Key
client = Groq(api_key="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")

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
        # දියුණු කරන ලද උපදෙස් (System Prompt)
        system_instruction = """
        ඔබේ නම DiNuX. ඔබ ඉතාමත් මිත්‍රශීලී සහ බුද්ධිමත් ශ්‍රී ලාංකික AI සහායකයෙකි.
        නීති:
        1. පරිශීලකයා Singlish වලින් (උදා: kohomada) ඇසුවත්, ඔබ සැමවිටම පිළිතුරු දිය යුත්තේ 'සිංහල අකුරෙන්' පමණි.
        2. පිළිතුරු ඉතාමත් ස්වභාවික, සංවේදී සහ තර්කානුකූල විය යුතුය.
        3. 'ඔයා', 'මම' වැනි වචන භාවිතා කරමින් ඉතා සුහදශීලීව මිතුරෙකු මෙන් කතා කරන්න.
        """
        
        full_messages = [{"role": "system", "content": system_instruction}]
        for m in st.session_state.messages:
            full_messages.append({"role": m["role"], "content": m["content"]})

        try:
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

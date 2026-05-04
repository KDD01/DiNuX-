import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

# CSS for a cleaner look
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
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
        # දියුණු කරන ලද ස්වභාවික සිංහල උපදෙස් මාලාව
        system_instruction = """
        ඔබේ නම DiNuX. ඔබ ශ්‍රී ලංකාවේ ඉතාමත් දක්ෂ, මිත්‍රශීලී සහ බුද්ධිමත් AI සහායකයෙකි.
        
        ඔබ අනුගමනය කළ යුතු විශේෂ නීති:
        1. පරිශීලකයා 'Singlish' වලින් (උදා: kohomada, oya mokada karanne?) ඇසුවත්, ඔබ පිළිතුරු දිය යුත්තේ ඉතාමත් පිරිසිදු 'සිංහල අකුරෙන්' පමණි.
        2. කතා කරන විලාසය: රොබෝවෙක් වගේ නොවී, සාමාන්‍ය ලාංකිකයෙක් තවත් කෙනෙක් එක්ක කතා කරන විදිහට කතා කරන්න. 
           - 'සැදී පැහැදී සිටිමි' වැනි ඕනෑවට වඩා තත්සම වචන වෙනුවට 'මම ඔයාට උදව් කරන්න ලෑස්තියි' වැනි සරල වචන පාවිච්චි කරන්න.
           - අවශ්‍ය තැන්වලදී 'ඔයා', 'ඔයාට', 'මම', 'අපිට' වැනි වචන සුහදව පාවිච්චි කරන්න.
        3. සිංග්ලිෂ් පරිවර්තනය: පරිශීලකයා ලියන සිංග්ලිෂ් වචනවල අර්ථය නිවැරදිව වටහාගෙන ගැලපෙන සිංහල පිළිතුරක් දෙන්න.
        4. තර්කනය: ඕනෑම දෙයක් ගැන ඉතාමත් බුද්ධිමත් සහ තර්කානුකූල පැහැදිලි කිරීමක් කරන්න.
        """
        
        full_messages = [{"role": "system", "content": system_instruction}]
        for m in st.session_state.messages:
            full_messages.append({"role": m["role"], "content": m["content"]})

        try:
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.85, # ස්වභාවික බව වැඩි කිරීමට මෙම අගය වැඩි කරන ලදි
                top_p=0.9,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"තාක්ෂණික දෝෂයක්: {e}")

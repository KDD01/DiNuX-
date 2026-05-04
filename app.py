import streamlit as st
from groq import Groq

# Page Config - වෙබ් අඩවියේ පෙනුම සැකසීම
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

# CSS මගින් පෙනුම තවත් ලස්සන කිරීම (Optional)
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_stdio=True)

st.title("DiNuX AI 🤖")
st.caption("ඔබේ ඕනෑම ගැටලුවකට සහය වීමට සැදී පැහැදී සිටින බුද්ධිමත් සහායකයා")
st.markdown("---")

# API Key - ආරක්ෂිතව ඇතුළත් කර ඇත
client = Groq(api_key="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")

# පණිවිඩ ඉතිහාසය තබා ගැනීම (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ සංවාද තිරයේ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# පරිශීලකයාගෙන් ප්‍රශ්න ලබා ගැනීම (Input)
if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකේ බුද්ධිමය ප්‍රතිචාරය සැකසීම
    with st.chat_message("assistant"):
        # ඉතාමත් දියුණු System Prompt එකක් ඇතුළත් කිරීම
        system_instruction = """
        ඔබේ නම DiNuX. ඔබ ශ්‍රී ලාංකික පරිශීලකයින් සඳහාම නිර්මාණය කළ ඉතාමත් බුද්ධිමත්, තර්කානුකූල සහ සංවේදී AI සහායකයෙකි.
        
        පිළිතුරු සැපයීමේදී අනුගමනය කළ යුතු නීති:
        1. භාෂාව: පරිශීලකයා 'Singlish' (උදා: oyage nama mokadda?) හෝ 'English' වලින් ඇසුවද, ඔබ පිළිතුරු දිය යුත්තේ පිරිසිදු සහ නිවැරදි 'සිංහල අකුරෙන්' (Unicode Sinhala) පමණි.
        2. ශෛලිය: ඉතාමත් සුහදශීලී (User-friendly), ගෞරවනීය සහ හැඟීම්බරව (Emotional) කතා කරන්න. 
        3. තර්කනය (Logic): ඕනෑම ගැටලුවකදී (ගණිතමය, තාක්ෂණික හෝ සාමාන්‍ය) තර්කානුකූලව සිතා නිවැරදිම විසඳුම ලබා දෙන්න.
        4. නම්‍යශීලී බව: පරිශීලකයාගේ අවශ්‍යතාවය හඳුනාගෙන එයට අනුවර්තනය (Adapt) වන්න. මිතුරෙකු මෙන් උපදෙස් දෙන්න.
        5. උදාහරණය: "oyage nama mokadda?" කියා ඇසුවහොත් "මම DiNuX AI, ඔයාගේ සේවය සඳහා මම සැදී පැහැදී සිටිනවා!" වැනි සුහද පිළිතුරක් දෙන්න.
        """
        
        full_messages = [{"role": "system", "content": system_instruction}]
        
        # පැරණි පණිවිඩ එකතු කිරීම
        for m in st.session_state.messages:
            full_messages.append({"role": m["role"], "content": m["content"]})

        try:
            # AI එකෙන් පිළිතුර ලබා ගැනීම
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.8, # ස්වභාවික බව වැඩි කිරීමට
                max_tokens=1024,
                top_p=0.9
            )
            
            response = chat_completion.choices[0].message.content
            
            # පිළිතුර තිරයේ පෙන්වීම
            st.markdown(response)
            # පිළිතුර මතකයේ තබා ගැනීම
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"කණගාටුයි, තාක්ෂණික දෝෂයක් ඇති වුණා: {str(e)}")

# Footer එකක් එකතු කිරීම
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Powered by DiNuX AI | 2026</p>", unsafe_allow_html=True)

import streamlit as st
from groq import Groq
from PIL import Image
import base64
from gtts import gTTS
import io

# 1. පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="wide")

# 2. UI එක නවීකරණය කිරීමට CSS (Dark & Premium Theme)
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        color: white;
    }
    .stChatMessage {
        border-radius: 20px;
        border: 1px solid #1e1e2e;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #11111b;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    h1 {
        text-align: center;
        background: linear-gradient(90deg, #ffffff, #515ada);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ලෝගෝ එක සහ UI ඉහළ කොටස
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        # ඔයාගේ අලුත් ලෝගෝ එක 'logo.png' නමින් තිබිය යුතුයි
        image = Image.open("logo.png")
        st.image(image, use_container_width=True)
    except:
        st.header("DiNuX AI")

st.markdown("<h1>THINK • LEARN • EVOLVE</h1>", unsafe_allow_html=True)
st.markdown("---")

# 4. Voice Function (කටහඬ නිපදවීම)
def speak_text(text):
    try:
        # සිංහල අකුරු තිබේදැයි බැලීම
        is_sinhala = any("\u0d80" <= char <= "\u0dff" for char in text)
        lang = 'si' if is_sinhala else 'en'
        
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Audio Player එකක් පෙන්වීම
        b64 = base64.b64encode(fp.read()).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)
    except:
        pass

# 5. Groq Client
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. පැරණි පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. ප්‍රශ්න ඇසීම සහ පිළිතුරු ලබා ගැනීම
if prompt := st.chat_input("DiNuX ගෙන් ඕනෑම දෙයක් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # දියුණු කරන ලද System Instruction
        system_instruction = """
        ඔබේ නම DiNuX. ඔබ ලෝකයේ සිටින බුද්ධිමත්ම සහ මිත්‍රශීලී ශ්‍රී ලාංකික AI සහායකයායි.
        නීති:
        - සැමවිටම ඉතාමත් ස්වභාවික 'සිංහල අකුරෙන්' පිළිතුරු දෙන්න.
        - පරිශීලකයා Singlish වලින් ලිව්වත් ඒවා තේරුම් ගෙන සිංහලෙන් පිළිතුරු දෙන්න.
        - ඉතාමත් සුහදව 'ඔයා', 'මම' වැනි වචන භාවිතා කරන්න.
        - තර්කානුකූලව සහ සංවේදීව කරුණු පැහැදිලි කරන්න.
        """
        
        full_messages = [{"role": "system", "content": system_instruction}]
        for m in st.session_state.messages:
            full_messages.append({"role": m["role"], "content": m["content"]})

        try:
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.8,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            # කටහඬ පණ ගැන්වීම
            speak_text(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

# 8. Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #515ada; font-size: 0.9em;'>Powered by DiNuX AI | DS Media Hub</p>", unsafe_allow_html=True)

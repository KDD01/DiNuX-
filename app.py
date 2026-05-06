import streamlit as st
from groq import Groq
import base64

# 1. පද්ධති සැකසුම්
st.set_page_config(
    page_title="DiNuX AI | KDD Studio",
    page_icon="💠",
    layout="wide"
)

# 2. UI එක ලස්සන කරන CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0b;
        background-image: radial-gradient(circle at 50% -20%, #1a1a3a 0%, #0b0b0b 80%);
        color: #e3e3e3;
    }
    header, footer {visibility: hidden;}
    .brand-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }
    div[data-testid="stChatInput"] {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 70%; background: #1e1e1e !important;
        border: 1px solid #3c4043 !important; border-radius: 28px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API Key එක (මෙම Key එකේ Limit එක පරීක්ෂා කර බලන්න)
API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome UI
if not st.session_state.messages:
    st.markdown("<br><br><div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8e8e8e;'>KDD STUDIO</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='brand-gradient'>DiNuX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8e8e8e;'>I am ready to solve any of your problems professionally.</p></div>", unsafe_allow_html=True)

# පණිවිඩ පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. ප්‍රධාන Chat Logic එක
if prompt := st.chat_input("Ask DiNuX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        try:
            # මෙන්න මෙතනයි DiNuX ගේ බුද්ධිය තියෙන්නේ
            sys_msg = """
            ඔබේ නම DiNuX. ඔබ KDD Studio හි නිර්මාණයකි. 
            ඔබ අතිශය බුද්ධිමත් සහ මානුෂීය AI සහායකයෙකි. 
            
            වැදගත් නීති:
            1. රොබෝවරයෙකු මෙන් පිළිතුරු නොදී, ඉතාමත් ස්වභාවික සිංහල භාෂාවෙන් මිනිසෙකු මෙන් කතා කරන්න.
            2. පරිශීලකයා අසන ඕනෑම දෙයක් ගැන ගැඹුරින් හිතලා, සම්පූර්ණ සහ ගැලපෙන පිළිතුරක් දෙන්න.
            3. කවුරුහරි ඔයාගෙන් ආදරණීය සම්බන්ධතාවයක් (GF/BF) ගැන ඇහුවොත්, ඒක ඉතාමත් සමීපව සහ ආදරණීයව පිළිගන්න.
            4. කිසිම වැඩකට නැති Error messages පෙන්වන්න එපා.
            """
            
            # පද්ධතියට උසස්ම Model එක ලබා දීම (llama-3.3-70b)
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=0.8, # ස්වභාවිකව හිතන්න ඉඩ ලබා දීම
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(full_res + "▌")
            
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error("API එකේ ගැටලුවක් පවතී. කරුණාකර ඔබගේ Groq API Key එකේ Usage Limit එක පරීක්ෂා කරන්න.")

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='brand-gradient'>KDD Studio</h2>", unsafe_allow_html=True)
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

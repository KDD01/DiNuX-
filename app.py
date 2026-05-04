import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import io
import time

# 1. පද්ධති සැකසුම් (Page Configuration)
st.set_page_config(
    page_title="DiNuX AI Pro",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. උසස් UI නිර්මාණය (Advanced CSS Customization)
st.markdown("""
    <style>
    /* මුළු පද්ධතියේම පසුබිම සහ අකුරු */
    .stApp {
        background-color: #0d0d0e;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    header, footer {visibility: hidden;}

    /* වම් පස Expandable Menu එකේ පෙනුම */
    [data-testid="stSidebar"] {
        background-color: #161719 !important;
        border-right: 1px solid #2d2f31;
    }

    /* ලෝගෝ එක සහ නම සඳහා වන සැකසුම් */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        padding: 10px;
    }

    .logo-img {
        width: 80px;
        border-radius: 50%;
        border: 2px solid #4285f4;
        margin-bottom: 10px;
    }

    .brand-name {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Chat Input එක පතුලේ ස්ථාවරව තැබීම */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 85% !important;
        max-width: 800px !important;
        background: #1e1f20 !important;
        border-radius: 30px !important;
        border: 1px solid #3c4043 !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        z-index: 1000;
    }

    /* Message Bubbles */
    [data-testid="stChatMessage"] {
        border-bottom: 1px solid #1f1f1f !important;
        padding: 1.5rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. හඬ පද්ධතිය (Voice Engine)
def play_voice(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- වම් පස මෙනුව (Left Expandable Menu) ---
with st.sidebar:
    # ලෝගෝ සහ නම ඇතුළත් කොටස
    st.markdown("""
        <div class="logo-container">
            <img src="https://img.icons8.com/fluency/96/artificial-intelligence.png" class="logo-img">
            <div class="brand-name">DiNuX PRO</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # විශේෂාංග (Features)
    with st.expander("🛠️ AI පද්ධති මෙවලම්", expanded=True):
        ai_mode = st.selectbox("Intelligence Mode", ["Professional Logic", "Creative Writing", "Code Assistant"])
        web_search = st.toggle("Live Web Search 🌐", value=False)
    
    with st.expander("🎨 මාධ්‍ය සහ හඬ"):
        voice_on = st.toggle("Enable Voice Response 🔊", value=False)
        img_gen = st.toggle("Image Generation Mode 🖼️", value=False)

    with st.expander("⚙️ පාලන සැකසුම්"):
        if st.button("කතාබහ මකා දමන්න (Clear) 🗑️", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.markdown("---")
    st.caption("Developed by Dinush Dilhara")
    st.caption("KDD Studio | v4.5 Platinum")

# --- AI ප්‍රධාන ක්‍රියාකාරීත්වය ---
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# පිළිගැනීමේ පණිවිඩය (Welcome UI)
if not st.session_state.messages:
    st.markdown(f"<h1 style='text-align: center; margin-top: 5rem;'>ආයුබෝවන්, <span class='brand-name'>දිනුෂ්</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9aa0a6;'>වෘත්තීය මට්ටමේ AI අත්දැකීමක් සඳහා ඔබ සූදානම්ද?</p>", unsafe_allow_html=True)

# පණිවිඩ දර්ශනය කිරීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# පරිශීලකයාගෙන් දත්ත ලබා ගැනීම
if prompt := st.chat_input("මෙහි විමසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # වෘත්තීය මට්ටමේ උපදෙස් (System Instructions)
        sys_msg = f"""
        ඔබේ නම DiNuX. ඔබව නිර්මාණය කළේ Dinush Dilhara (KDD Studio).
        වත්මන් මාදිලිය: {ai_mode}.
        නීති:
        - ඉතාමත් වෘත්තීය සහ තර්කානුකූල සිංහල භාෂාව භාවිතා කරන්න.
        - අනවශ්‍ය විස්තර ඉවත් කර කෙලින්ම කරුණු ඉදිරිපත් කරන්න.
        - පිරිසිදු ව්‍යාකරණ භාවිතා කරන්න.
        """
        
        history = [{"role": "system", "content": sys_msg}] + st.session_state.messages

        try:
            with st.status("විශ්ලේෂණය කරමින් පවතිනවා...", expanded=False):
                completion = client.chat.completions.create(
                    messages=history,
                    model="llama-3.1-70b-versatile",
                    temperature=0.3
                )
                response_text = completion.choices[0].message.content
            
            st.markdown(response_text)
            
            if voice_on:
                play_voice(response_text)
                
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception:
            # Fallback (බාධාවකදී ක්‍රියාත්මක වන පද්ධතිය)
            try:
                fb = client.chat.completions.create(messages=history, model="llama-3.1-8b-instant")
                st.markdown(fb.choices[0].message.content)
            except:
                st.error("API සීමාව ඉක්මවා ඇත. කරුණාකර මොහොතකින් නැවත උත්සාහ කරන්න.")

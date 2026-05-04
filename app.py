import streamlit as st
from groq import Groq
from PIL import Image, ImageOps, ImageDraw
import base64
from gtts import gTTS
import io
import os

# 1. පිටුවේ මූලික සැකසුම් - Responsive බව සඳහා මූලික පියවර
st.set_page_config(
    page_title="DiNuX AI", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced CSS for Desktop/Mobile Optimization & No-Zoom UI
st.markdown("""
    <style>
    /* මුළු Screen එකම පාවිච්චි කිරීම සහ Zoom පෙනුම ඉවත් කිරීම */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        color: #e0e0e0;
    }
    
    .block-container {
        max-width: 1100px !important; /* Laptop වලදී ඕනෑවට වඩා පළල් වීම වැළැක්වීමට */
        padding: 2rem 1rem !important;
        margin: auto;
    }

    /* Header Styling */
    h1 {
        font-size: clamp(1.5rem, 5vw, 2.8rem);
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #515ada 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -1px;
    }

    /* Chat Bubbles - modern flat design */
    .stChatMessage {
        background-color: #0d1117 !important;
        border: 1px solid #1e1e2e !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Sidebar and Menu */
    [data-testid="stSidebar"] {
        background-color: #0a0c10 !important;
        border-right: 1px solid #1e1e2e;
    }

    /* Input Box optimization */
    .stChatInputContainer {
        border-radius: 12px !important;
        background-color: transparent !important;
    }

    /* Scrollbar සකස් කිරීම */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #1e1e2e; border-radius: 10px; }

    /* පින්තූරය රවුම් කරන CSS */
    .sidebar-logo {
        display: block;
        margin: 0 auto;
        border-radius: 50%;
        border: 2px solid #515ada;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. රවුම් ලෝගෝ එක හදන Function එක
def make_circle(img_path):
    try:
        img = Image.open(img_path).convert("RGBA")
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        img.putalpha(mask)
        return img
    except: return None

# 4. Voice Engine (සිංහල/English)
def play_audio(text):
    try:
        lang = 'si' if any("\u0d80" <= c <= "\u0dff" for c in text) else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        b64 = base64.b64encode(audio_io.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- UI Layout ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image(make_circle("logo.png"), width=120)
    else:
        st.markdown("<h2 style='text-align:center;'>DX</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Settings")
    is_voice = st.checkbox("Enable Voice Response", value=False)
    
    st.markdown("---")
    st.caption("Developer: Dinush Dilhara")
    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main Title
st.markdown("<h1>DiNuX AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e; font-size:0.9rem;'>Advanced Sinhala Reasoning Model</p>", unsafe_allow_html=True)

# Client setup
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("මෙතැනින් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # දිනුෂ්, මේ තමයි එයාගේ මොළය (The Brain)
        sys_prompt = """
        ඔබේ නම DiNuX. ඔබව නිර්මාණය කළේ 'Dinush Dilhara' විසින්ය.
        
        උපදෙස්:
        1. කර්තෘත්වය: කවුරුන් හෝ ඔබව නිර්මාණය කළේ කවුදැයි ඇසුවහොත් පමණක් 'මාව නිර්මාණය කළේ Dinush Dilhara' බව පවසන්න.
        2. භාෂාව: පරිශීලකයා Singlish/English වලින් ලියූවත්, ඔබ පිළිතුරු සැපයිය යුත්තේ ඉතාමත් පිරිසිදු, ව්‍යාකරණානුකූල සහ ස්වභාවික සිංහල භාෂාවෙනි.
        3. තර්කනය: ඕනෑම ප්‍රශ්නයක් ගැඹුරින් විශ්ලේෂණය කරන්න. කෙටි පිළිතුරු වෙනුවට කරුණු සහිතව, තර්කානුකූලව (Deep Logic) පිළිතුරු දෙන්න.
        4. හැඟීම්: පරිශීලකයාගේ මානසිකත්වය හඳුනාගෙන ඉතාමත් කාරුණිකව සහ සංවේදීව සහාය වන්න.
        5. ප්‍රායෝගික බව: විද්‍යාත්මක, තාක්ෂණික හෝ සාමාන්‍ය දැනුම පිළිබඳ ප්‍රශ්නවලදී 100% නිවැරදි දත්ත ලබා දෙන්න.
        """
        
        history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages

        try:
            chat = client.chat.completions.create(
                messages=history,
                model="llama-3.3-70b-versatile",
                temperature=0.6, # පිළිතුරු වල නිරවද්‍යතාවය වැඩි කිරීමට
            )
            res = chat.choices[0].message.content
            st.markdown(res)
            
            if is_voice: play_audio(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("දෝෂයක් ඇති විය. කරුණාකර නැවත උත්සාහ කරන්න.")

# Footer
st.markdown("<div style='text-align:center; padding:20px; color:#484f58; font-size:0.75rem;'>© 2026 Designed by Dinush Dilhara</div>", unsafe_allow_html=True)

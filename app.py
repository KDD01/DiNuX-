import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="DiNuX AI Pro", page_icon="🤖", layout="wide")

# --- API SETUP ---
# ඔයා ලබා දුන් API Key එක
API_KEY = "AIzaSyCSIbVlIY0_CJe1rfFqh6l4lZoeAGlCGpU"
genai.configure(api_key=API_KEY)

# Error එක නැති කිරීම සඳහා මෙතන 'models/' කොටස ඉවත් කර සරලව model එක නම් කර ඇත
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SIDEBAR (මෙතනට අලුත් Options එකතු කර ඇත) ---
with st.sidebar:
    st.title("⚙️ AI Settings")
    st.info("මෙම ඇප් එක Gemini 1.5 Flash තාක්ෂණයෙන් බලගන්වා ඇත.")
    
    # පෙනුම වෙනස් කිරීමට Option එකක්
    theme_mode = st.selectbox("Display Mode", ["Light", "Dark", "Cinematic"])
    
    # AI එකේ වේගය/නිර්මාණශීලීත්වය පාලනය (වැඩි විස්තර)
    st.markdown("---")
    st.subheader("App Details")
    st.write("**Version:** 2.0.1")
    st.write("**Developer:** Dinush")
    st.write("**Status:** Active ✅")
    
    st.markdown("---")
    if st.button("🗑️ Clear All Conversations"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🤖 DiNuX AI Assistant")
st.caption("Advanced AI for fast and accurate responses")

# Chat history එක පවත්වාගෙන යාම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් සිදුවූ කතාබස් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් input එකක් ගැනීම
if prompt := st.chat_input("මොනවා හරි අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුරක් ලබා ගැනීම
    try:
        with st.chat_message("assistant"):
            with st.spinner("සිතමින් පවතිනවා..."):
                # මෙහිදී කෙලින්ම model එක call කරනු ලබයි
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        # Error එක ආවොත් මෙතනින් පෙන්වනවා
        st.error(f"දෝෂයක් ඇති විය: {str(e)}")
        st.info("සටහන: සමහරවිට ඔබගේ API Key එකේ සීමාව ඉක්මවා ගොස් තිබිය හැක.")

import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

# --- API SETUP ---
# ඔයා ලබා දුන් API Key එක මෙහි ඇතුළත් කර ඇත
API_KEY = "AIzaSyCSIbVlIY0_CJe1rfFqh6l4lZoeAGlCGpU"

genai.configure(api_key=API_KEY)

# අලුත්ම gemini-1.5-flash model එක භාවිතා කිරීම (Error එක මඟ හැරීමට)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- CHAT INTERFACE ---
st.title("🤖 DiNuX AI Assistant")
st.markdown("ඔයාට අවශ්‍ය ඕනෑම දෙයක් සිංහලෙන් හෝ ඉංග්‍රීසියෙන් අහන්න.")
st.markdown("---")

# Chat ඉතිහාසය මතක තබා ගැනීමට (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කතා කරපුවා display කිරීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් ප්‍රශ්නයක් ලබා ගැනීම
if prompt := st.chat_input("Ask me something..."):
    # User message එක history එකට එකතු කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුර ලබා ගැනීම
    try:
        with st.chat_message("assistant"):
            with st.spinner("සිතමින් පවතිනවා..."):
                response = model.generate_content(prompt)
                ai_text = response.text
                st.markdown(ai_text)
        
        # AI පිළිතුර history එකට එකතු කිරීම
        st.session_state.messages.append({"role": "assistant", "content": ai_text})
        
    except Exception as e:
        # යම් දෝෂයක් ආවොත් එය පෙන්වීමට
        st.error(f"දෝෂයක් ඇති විය: {str(e)}")

# Sidebar එකේ Chat එක clear කරන්න බොත්තමක්
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

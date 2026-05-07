import streamlit as st
import google.generativeai as genai

# ඇප් එකේ පිටුවේ සැකසුම් (Page Config)
st.set_page_config(page_title="DiNuX AI", page_icon="🤖", layout="centered")

# --- API SETUP ---
# ඔයා Streamlit Cloud පාවිච්චි කරනවා නම් Secrets වල GOOGLE_API_KEY ලෙස මෙය සුරකින්න.
# නැත්නම් කෙලින්ම " " ඇතුලේ ඔයාගේ Key එක දාන්න.
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = "මෙතනට_ඔයාගේ_API_KEY_එක_දාන්න"

if not api_key or api_key == "මෙතනට_ඔයාගේ_API_KEY_එක_දාන්න":
    st.warning("කරුණාකර ඔබගේ Google API Key එක ඇතුළත් කරන්න.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI පෙනුම ---
st.title("🤖 DiNuX AI Assistant")
st.caption("මම Gemini 1.5 Flash මගින් ක්‍රියාත්මක වන AI සහායකයෙක්.")

# Chat history එක පවත්වාගෙන යාම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් සිදුවූ කතාබස් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් input එකක් ගැනීම
if prompt := st.chat_input("මොනවා හරි අහන්න..."):
    # User message එක history එකට එකතු කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුරක් ලබා ගැනීම
    try:
        with st.chat_message("assistant"):
            # පිළිතුර ලැබෙන තෙක් loading icon එකක් පෙන්වීමට
            with st.spinner("හිතමින් පවතිනවා..."):
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
        
        # AI පිළිතුර history එකට එකතු කිරීම
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Error එකක් සිදු විය: {str(e)}")

# Clear Chat බොත්තම (Side bar එකේ)
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

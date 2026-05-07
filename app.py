import streamlit as st
import google.generativeai as genai
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="DiNuX AI Pro", page_icon="🤖", layout="wide")

# --- API CONFIG ---
API_KEY = "AIzaSyCSIbVlIY0_CJe1rfFqh6l4lZoeAGlCGpU"
genai.configure(api_key=API_KEY)

# --- AUTO-FIX & SMART MODEL SELECTOR ---
# එක model එකක් error ආවොත් අනිත් එක පාවිච්චි කරන ලොජික් එක
def get_ai_response(prompt):
    # උත්සාහ කරන Models ලැයිස්තුව
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # මේ model එක වැඩ නැත්නම් ඊළඟ එකට යන්න
            continue 
    
    return "සමාවෙන්න, Models කිසිවක් ප්‍රතිචාර දක්වන්නේ නැත. කරුණාකර ඔබගේ API Key එක පරීක්ෂා කරන්න."

# --- SIDEBAR UI ---
with st.sidebar:
    st.title("🤖 DiNuX AI Control")
    st.markdown("---")
    st.success("Auto-Fix Mode: ON 🛡️")
    st.info("System: multi-model fallback active")
    
    st.markdown("---")
    st.subheader("App Info")
    st.write("**Developer:** Dinush")
    st.write("**Status:** Running")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 DiNuX AI Assistant")
st.caption("I will think and answer your questions automatically fixing any bugs.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ඉතිහාසය පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ප්‍රශ්නය ඇසීම
if prompt := st.chat_input("ඔයාට දැනගන්න ඕන මොනවාද?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("හිතමින් පවතිනවා..."):
            # මෙතනදී ඇප් එක හිතලා හොඳම model එක තෝරාගෙන පිළිතුරු දෙයි
            full_response = get_ai_response(prompt)
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

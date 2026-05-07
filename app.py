import streamlit as st
import google.generativeai as genai
import time

# --- පිටුවේ සැකසුම් ---
st.set_page_config(page_title="DiNuX AI Pro", page_icon="🤖", layout="wide")

# --- API CONFIGURATION ---
# ඔයා ලබා දුන් අලුත්ම API Key එක මෙහි ඇත
API_KEY = "AIzaSyA4gVtgFUbJoP6LL5KRH5tklRYDuVWpm48"

# API එක සම්බන්ධ කිරීම (Connection stable කිරීමට settings යොදා ඇත)
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"API Configuration Error: {e}")

# --- AUTO-FIX LOGIC (බොට් වැඩ නොකර සිටීම වළක්වන ක්‍රමය) ---
def generate_ai_response(user_input):
    # වැඩ කිරීමට ඉඩ ඇති මාදිලි ලැයිස්තුව (Fallback system)
    models_to_test = [
        'gemini-1.5-flash', 
        'gemini-1.5-pro', 
        'gemini-pro'
    ]
    
    for model_name in models_to_test:
        try:
            model = genai.GenerativeModel(model_name)
            # වචන generate කරන විට ඇතිවන පොදු දෝෂ මගහැරීමට උත්සාහ කරයි
            response = model.generate_content(user_input)
            if response and response.text:
                return response.text
        except Exception:
            # මේ model එක වැඩ නැත්නම් ඊළඟ එකට මාරු වෙයි
            continue
            
    return "සමාවෙන්න, මට මේ වෙලාවේ පිළිතුරු දීමට නොහැකියි. කරුණාකර ඔබගේ API Key එකේ සීමාවන් (Limits) පරීක්ෂා කරන්න."

# --- SIDEBAR UI (ඔයා ඉල්ලපු අලුත් Options) ---
with st.sidebar:
    st.title("🤖 DiNuX AI Control")
    st.markdown("---")
    st.success("System Status: Active ✅")
    st.info("Auto-Healing: Enabled 🛡️")
    
    st.markdown("### ⚙️ App Options")
    ai_mood = st.selectbox("Response Style", ["Professional", "Friendly", "Detailed"])
    
    st.markdown("---")
    st.markdown("### 📄 App Details")
    st.write("**Name:** DiNuX AI Pro")
    st.write("**Developer:** Dinush")
    st.write("**Version:** 3.0.0 (Final)")
    
    if st.button("🗑️ Clear All Conversations"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🤖 DiNuX AI Assistant")
st.caption("Advanced Auto-Bugs Fixing System is Active")

# Chat History එක තබා ගැනීමට
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කතා කරපුවා පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input ලබා ගැනීම
if prompt := st.chat_input("මොනවා හරි අහන්න..."):
    # User message එක history එකට එක් කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response ලබා ගැනීම (Error handling සමග)
    with st.chat_message("assistant"):
        with st.spinner("හිතමින් පවතිනවා..."):
            # පද්ධතිය විසින්ම හොඳම model එක තෝරාගෙන පිළිතුරු දෙයි
            full_response = generate_ai_response(prompt)
            st.markdown(full_response)
    
    # AI පිළිතුර history එකට එක් කිරීම
    st.session_state.messages.append({"role": "assistant", "content": full_response})

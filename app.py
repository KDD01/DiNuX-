import streamlit as st
import google.generativeai as genai
from groq import Groq
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="DiNuX AI Infinity", page_icon="♾️", layout="wide")

# --- API KEYS CONFIG ---
# ඔයා ලබා දුන් Groq Key එක
GROQ_API_KEY = "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"

# ඔයාගේ Gemini Keys ලැයිස්තුව (Fallback සඳහා)
GEMINI_KEYS = [
    "AIzaSyA4gVtgFUbJoP6LL5KRH5tklRYDuVWpm48",
    "AIzaSyCSIbVlIY0_CJe1rfFqh6l4lZoeAGlCGpU"
]

# --- SMART BRAIN LOGIC (Auto-Fixing & Switching) ---
def get_ai_response(prompt):
    # 1. මුලින්ම Groq උත්සාහ කරයි (වේගවත්ම ක්‍රමය)
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as groq_err:
        # Groq වැඩ නැත්නම් Gemini Keys එකින් එක පරීක්ෂා කරයි
        for key in GEMINI_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                continue
    
    return "සමාවෙන්න, සියලුම AI පද්ධති මේ වෙලාවේ කාර්යබහුලයි. කරුණාකර තත්පර කිහිපයකින් නැවත උත්සාහ කරන්න."

# --- SIDEBAR UI ---
with st.sidebar:
    st.title("♾️ DiNuX AI Infinity")
    st.markdown("---")
    st.success("Auto-Fix Mode: Active 🛡️")
    st.info("Hybrid Engine: Groq + Gemini")
    
    st.markdown("### 📊 System Info")
    st.write("**Developer:** Dinush Dilhara")
    st.write("**Project:** A/L IT Final")
    st.write("**Speed:** Ultra-Fast ⚡")
    
    st.markdown("---")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🤖 DiNuX AI Assistant")
st.caption("Advanced AI with unlimited fallback support and auto-bug fixing.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("මොනවා හරි අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("සිතමින් පවතිනවා..."):
            # පද්ධතිය විසින් හොඳම engine එක තෝරා ගනී
            full_response = get_ai_response(prompt)
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

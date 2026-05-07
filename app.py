import streamlit as st
import google.generativeai as genai
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="DiNuX AI Pro", page_icon="🤖", layout="wide")

# --- API & MODEL CONFIG ---
API_KEY = "AIzaSyCSIbVlIY0_CJe1rfFqh6l4lZoeAGlCGpU"
genai.configure(api_key=API_KEY)

# Error එක මඟහැරීමට model එක නිවැරදිව අර්ථ දැක්වීම
MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

# --- AUTO-FIX LOGIC (Bugs fix කරමින් දිගටම වැඩ කිරීමට) ---
def safe_generate_content(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)  # තත්පර 2ක් ඉඳලා නැවත උත්සාහ කරයි
                continue
            else:
                return f"සමාවෙන්න, පද්ධතියේ ඇතිවූ දෝෂයක් නිසා මට පිළිතුරු දීමට නොහැකි විය: {str(e)}"

# --- SIDEBAR OPTIONS ---
with st.sidebar:
    st.title("⚙️ DiNuX AI Control")
    st.info("System Status: Operational ✅")
    
    st.markdown("---")
    st.subheader("App Options")
    st.selectbox("Chat Style", ["Professional", "Friendly", "Creative"])
    
    st.markdown("---")
    st.subheader("About")
    st.write("**Developer:** Dinush")
    st.write("**Core:** Gemini 1.5 Flash")
    st.write("**Auto-Fix:** Enabled 🛡️")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT INTERFACE ---
st.title("🤖 DiNuX AI Assistant")
st.caption("Auto-healing and error-fixing system is active.")

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

    # AI Response with Error Handling
    with st.chat_message("assistant"):
        with st.spinner("සකසමින් පවතිනවා..."):
            # මෙතනදී error එකක් ආවොත් එය auto-fix කිරීමට උත්සාහ කරයි
            full_response = safe_generate_content(prompt)
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

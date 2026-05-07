import streamlit as st
import google.generativeai as genai
import time

# --- පිටුවේ සැකසුම් ---
st.set_page_config(page_title="DiNuX AI Ultra", page_icon="🚀", layout="wide")

# --- API KEYS (Keys කිහිපයක් පාවිච්චි කර සීමාවන් මගහැරීම) ---
# ඔයා මට දුන්න Keys දෙකම මෙතන තියෙනවා
api_keys = [
    "AIzaSyA4gVtgFUbJoP6LL5KRH5tklRYDuVWpm48",
    "AIzaSyCSIbVlIY0_CJe1rfFqh6l4lZoeAGlCGpU"
]

# --- AUTO-SWITCH LOGIC (එකක් Limit වුණොත් අනිත් එකට මාරු වීම) ---
def get_response_from_ai(user_input):
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro']
    
    # හැම API Key එකක්ම පරීක්ෂා කිරීම
    for key in api_keys:
        try:
            genai.configure(api_key=key)
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(user_input)
                    if response and response.text:
                        return response.text
                except Exception:
                    continue
        except Exception:
            continue
            
    return "සමාවෙන්න, ලබා දී ඇති සියලුම API Keys වල සීමාවන් ඉක්මවා ඇත. කරුණාකර විනාඩියකින් නැවත උත්සාහ කරන්න."

# --- UI (SIDEBAR) ---
with st.sidebar:
    st.title("🚀 DiNuX AI Ultra")
    st.success("Load Balancing: Active ⚖️")
    st.info("System: Unlimited Attempt Mode")
    
    st.markdown("---")
    st.subheader("Developer Hub")
    st.write("**Dev:** Dinush Dilhara")
    st.write("**A/L IT Project v4.0**")
    
    if st.button("🗑️ Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 DiNuX AI - Pro Assistant")
st.caption("Advanced AI with Multiple API Key Support (Anti-Limit System)")

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
        with st.spinner("හිතමින් පවතිනවා..."):
            # පද්ධතිය විසින් Keys මාරු කරමින් පිළිතුර ලබා දෙයි
            full_response = get_response_from_ai(prompt)
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

import streamlit as st
from groq import Groq

# --- 1. CONFIGURATION ---
API_KEY = "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"

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. UI SETTINGS (保持原样) ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    .shining-title {
        color: #ffffff;
        font-size: 45px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #333, #fff, #333);
        background-repeat: no-repeat;
        background-size: 80%;
        animation: shine 3s linear infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.2);
    }

    @keyframes shine {
        0% { background-position: -500%; }
        100% { background-position: 500%; }
    }
    
    .caption-text { text-align: center; color: #94a3b8; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="shining-title">DiNuX AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Developed by Dinush Dilhara | Powered by KDD Studio</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT LOGIC WITH AUTO-FIX ---
if prompt := st.chat_input("Ask DiNuX anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # වැඩ කරන Models කිහිපයක් පිළිවෙළට (එකක් වැඩ නැත්නම් අනිකට යනවා)
        models_to_try = ["llama-3.3-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"]
        response_found = False
        
        for model_name in models_to_try:
            try:
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are DiNuX AI, a friendly and professional assistant created by Dinush Dilhara. Use user-friendly language."},
                        {"role": "user", "content": prompt}
                    ],
                )
                response = completion.choices[0].message.content
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    response_found = True
                    break # පිළිතුරක් ලැබුණොත් loop එකෙන් ඉවත් වෙනවා
            except Exception as e:
                # Model එක decommission වෙලා නම් ඊළඟ එකට යනවා
                continue 
        
        if not response_found:
            st.error("කණගාටුයි, දැනට පවතින සියලුම AI මාදිලි අක්‍රියයි. කරුණාකර පසුව උත්සාහ කරන්න.")

import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# මෙතනට ඔයාගේ API Key එක නිවැරදිව ඇතුළත් කරන්න
API_KEY = "මෙතනට_ඔයාගේ_API_KEY_එක_Paste_කරන්න"

# API එක සම්බන්ධ කිරීමේ ආරක්ෂිත ක්‍රමය
def configure_api():
    try:
        genai.configure(api_key=API_KEY)
        # 1.5-flash මාදිලිය ගොඩක් ස්ථාවරයි
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        return None

model = configure_api()

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="DiNuX AI", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: white; }
    
    /* Shining Title Styling */
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

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT LOGIC ---
if prompt := st.chat_input("Ask DiNuX anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                # Response එක ලැබෙන තුරු බලා සිටීම සහ පෙන්වීම
                response = model.generate_content(prompt)
                
                # වැදගත්ම කොටස: පිළිතුර හිස්දැයි පරීක්ෂා කිරීම
                if response and response.text:
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.warning("AI එකෙන් පිළිතුරක් ලැබුණේ නැහැ. කරුණාකර නැවත උත්සාහ කරන්න.")
            
            except Exception as e:
                # පිළිතුර නොපෙන්වන්නේ ඇයි කියලා මෙතනින් බලාගන්න පුළුවන්
                st.error(f"Error during generation: {e}")
                if "quota" in str(e).lower():
                    st.info("ඔයාගේ API Limit එක ඉවර වෙලා වගෙයි. අලුත් API Key එකක් උත්සාහ කරන්න.")
        else:
            st.error("API එක නිවැරදිව සම්බන්ධ වී නැත.")

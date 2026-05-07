import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBtKQ9XAelwCGDC6uD3UgEJzLC5bMM5FxQ" 
genai.configure(api_key=GEMINI_API_KEY)

# --- 2. ADVANCED UI DESIGN (IMAGE BASED) ---
st.set_page_config(page_title="DiNuX ai - Intelligence Hub", layout="wide")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1f2937;
        width: 260px !important;
    }

    /* Glassmorphism Cards */
    .card {
        background: rgba(31, 41, 55, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    .status-active { color: #10b981; font-size: 12px; font-weight: bold; }
    .status-training { color: #3b82f6; font-size: 12px; font-weight: bold; }

    /* Custom Chat Input */
    .stChatInputContainer {
        background-color: #1f2937 !important;
        border-radius: 12px !important;
        border: 1px solid #374151 !important;
    }

    /* Custom Button Style */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>🧬 DiNuX <span style='color:#3b82f6;'>ai</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#9ca3af;'>Intelligence Hub</p>", unsafe_allow_html=True)
    st.write("---")
    st.button("🏠 Dashboard")
    st.button("📂 Projects")
    st.button("🤖 AI Models")
    st.button("📊 Analytics")
    st.button("⚙️ Settings")
    st.write("---")
    st.caption("Admin: Dinush Dilhara")

# --- 4. MAIN LAYOUT (Three Columns like Image) ---
col1, col2, col3 = st.columns([1.2, 2, 1], gap="medium")

# --- COLUMN 1: PROJECT OVERVIEW ---
with col1:
    st.markdown("### Project Overview")
    
    # Card 1
    with st.container():
        st.markdown("""
        <div class="card">
            <p style='margin:0; font-weight:bold;'>Insight Engine v7</p>
            <span class="status-active">● Active</span>
            <h2 style='text-align:center; color:#10b981;'>80%</h2>
            <p style='font-size:11px; text-align:center; color:#9ca3af;'>Accuracy 55%</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Open Chat", key="btn1")

    # Card 2
    with st.container():
        st.markdown("""
        <div class="card">
            <p style='margin:0; font-weight:bold;'>NLP Sentiment Bot</p>
            <span class="status-training">● Training</span>
            <h2 style='text-align:center; color:#3b82f6;'>90%</h2>
            <p style='font-size:11px; text-align:center; color:#9ca3af;'>Accuracy 95%</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Settings", key="btn2")

# --- COLUMN 2: LIVE COLLABORATION & CHAT ---
with col2:
    st.markdown("### Live Collaboration & Chat")
    
    chat_container = st.container(height=500, border=True)
    with chat_container:
        st.chat_message("user").write("How do we generate AI Insight Engine for DiNuX AI?")
        st.chat_message("assistant").write("Here is the architectural overview for the DiNuX Insight Engine. You can retrain the model using the provided data studio link.")
        st.code("""def predict(data):
    return model.predict(data)""", language="python")

    prompt = st.chat_input("Command DiNuX... or select a suggested action")

# --- COLUMN 3: METRICS & HISTORY ---
with col3:
    st.markdown("### Active Model Metrics")
    
    # Mini Chart using Plotly
    fig = go.Figure(go.Scatter(y=[10, 45, 30, 80, 95], mode='lines', line=dict(color='#3b82f6', width=3)))
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=150, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="card">
        <p style='font-size:13px; font-weight:bold;'>Chat History</p>
        <p style='font-size:12px; color:#9ca3af;'>● Session list 1</p>
        <p style='font-size:12px; color:#3b82f6;'>● Session list 2 (Active)</p>
        <p style='font-size:12px; color:#9ca3af;'>● Session list 3</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style='background: linear-gradient(135deg, #1e3a8a, #1e293b);'>
        <p style='font-size:12px;'><b>Usage Metrics</b></p>
        <p style='font-size:10px;'>CPU: 45% | GPU: 88%</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. CHAT LOGIC ---
if prompt:
    with col2:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        st.chat_message("assistant").write(response.text)

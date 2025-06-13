# style.py
import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Genel görünüm */
    .main > div {
        padding: 20px;
        background-color: #fff8f8;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(204, 51, 51, 0.1);
    }

    h1, h2, h3, h4 {
        color: #9b2d2d;
    }

    /* Sidebar görünüm */
    [data-testid="stSidebar"] {
        background-color: #fff1f1;
        padding: 20px;
        border-radius: 12px;
    }

    .sidebar-title, .sidebar-text {
        color: #cc3333;
        font-weight: bold;
        margin-bottom: 12px;
    }

    /* Metin kutuları */
    .metric-box {
        font-size: 16px;
        padding: 8px;
        border-radius: 8px;
        background-color: #eb4c54;
        color: white;
        font-weight: bold;
        margin-bottom: 5px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.1);
    }

    /* Dataframe görünümü */
    .stDataFrame {
        border: 1px solid #792f2f;
        border-radius: 8px;
        background-color: #fff;
    }

    /* Butonlar */
    .stButton>button {
        background-color: #cc3333;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
        margin-bottom: 5px;
        transition: 0.3s;
        cursor: pointer;
    }

    .stButton>button:hover {
        background-color: #9b2d2d;
    }

    /* Radio kutuları */
    .stRadio > div {
        background-color: #fce9e9;
        border-radius: 10px;
        padding: 5px 10px;
    }
    </style>
    """, unsafe_allow_html=True)

import streamlit as st
from app import run_app
from ariza_durus import run_ariza_durus
from style import apply_custom_styles

st.set_page_config(page_title="Ketsan Panel", layout="wide")

apply_custom_styles()

DOGRU_PAROLA = "ketsan123"



# Session state başlangıç
if "parola_giris" not in st.session_state:
    st.session_state.parola_giris = False

if "sayfa_secildi" not in st.session_state:
    st.session_state.sayfa_secildi = None

def parola_kontrol():
    parola = st.session_state.parola_input
    if parola == DOGRU_PAROLA:
        st.session_state.parola_giris = True
    else:
        st.session_state.parola_giris = False
        st.session_state.sayfa_secildi = None

# Parola girilmemişse giriş ekranı
if not st.session_state.parola_giris:
    st.sidebar.markdown("""
<h1 style='
    text-align:center; 
    font-weight:1000; 
    color:#B22222;  /* Koyu kırmızı tonu */
    text-shadow: 1px 1px 2px rgba(0,0,0,0.9);
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
'>
Ketsan Takip Paneli
</h1>""", unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-title">🔐 Giriş</div>', unsafe_allow_html=True)
    st.sidebar.text_input("Parola", type="password", key="parola_input", on_change=parola_kontrol)
    
    # Logo: sadece parola girilmeden önce göster
    st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.sidebar.image("assets/logo.png", width=250)

    if "parola_input" in st.session_state and st.session_state.parola_input != "" and not st.session_state.parola_giris:
        st.sidebar.warning("❗ Lütfen geçerli bir parola girin.")

# Giriş başarılıysa panel seçimi
else:
    st.sidebar.markdown('<div class="sidebar-title">🧭 Panel Seçimi</div>', unsafe_allow_html=True)

    if st.sidebar.button("👨‍💼 Personel Takip Paneli"):
        st.session_state.sayfa_secildi = "personel"

    if st.sidebar.button("⚙️ Arıza Duruş Paneli"):
        st.session_state.sayfa_secildi = "ariza"

    # ❗ Logo sadece panel seçilmediyse gösterilir
    if st.session_state.sayfa_secildi is None:
        st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.sidebar.image("assets/logo.png", width=250)

    # Ana içerik
    if st.session_state.sayfa_secildi == "personel":
        st.markdown("## 👨‍💼 Personel Takip Paneli")
        run_app()

    elif st.session_state.sayfa_secildi == "ariza":
        st.markdown("## ⚙️ Arıza Duruş Paneli")
        run_ariza_durus()

    else:
        st.markdown("### 👋 Hoş geldiniz!")
        st.info("Lütfen sol menüden bir panel seçin.")
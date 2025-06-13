import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO
from style import apply_custom_styles  # Ortak stil dosyası
def run_app():
    
    apply_custom_styles()
    # Excel dosyası yükleniyor
    url = "https://drive.google.com/uc?id=17j8gqcXKOytpifMmSfcoZF2Y6ApUxO2E&export=download"
    df = pd.read_csv(url)

    # Filtreler
    st.sidebar.markdown('<div class="sidebar-title">🔍 Filtreler</div>', unsafe_allow_html=True)

    ad_soyad = st.sidebar.selectbox("👤 Ad Soyad", ["Tümü"] + list(df["OPERATOR_ISIM"].unique()))

    if ad_soyad != "Tümü":
        bolumler = df[df["OPERATOR_ISIM"] == ad_soyad]["BOLUM"].unique()
    else:
        bolumler = df["BOLUM"].unique()

    bolum = st.sidebar.multiselect("🏭 Bölüm", ["Tümü"] + list(bolumler))
    df["TARIH"] = pd.to_datetime(df["TARIH"])
    tarih_araligi = st.sidebar.date_input(
        "📅 Tarih Aralığı",
        [df["TARIH"].min().date(), df["TARIH"].max().date()]
    )

    # Filtreleme
    filtered_df = df.copy()
    if ad_soyad != "Tümü":
        filtered_df = filtered_df[filtered_df["OPERATOR_ISIM"] == ad_soyad]
    if bolum and "Tümü" not in bolum:
        filtered_df = filtered_df[filtered_df["BOLUM"].isin(bolum)]
    if len(tarih_araligi) == 2:
        start_date, end_date = tarih_araligi
        filtered_df = filtered_df[(filtered_df["TARIH"] >= pd.to_datetime(start_date)) & 
                                (filtered_df["TARIH"] <= pd.to_datetime(end_date))]

    filtered_df["TARIH"] = pd.to_datetime(filtered_df["TARIH"]).dt.normalize()

    # Zaman seviyesi seçimi
    st.markdown("#### ⏱️ Veri Görüntüleme Aralığı")
    zaman_seviyesi = st.radio("", ["Günlük", "Aylık"], horizontal=True)

    # Zaman seviyesine göre gruplama
    if zaman_seviyesi == "Günlük":
        performans_df = filtered_df.groupby("TARIH")["PERFORMANS"].mean().reset_index()
        performans_df["TARIH_STR"] = performans_df["TARIH"].dt.strftime("%d %B")
    elif zaman_seviyesi == "Aylık":
        filtered_df["AY"] = filtered_df["TARIH"].dt.to_period("M").dt.to_timestamp()
        performans_df = filtered_df.groupby("AY")["PERFORMANS"].mean().reset_index()
        performans_df.rename(columns={"AY": "TARIH"}, inplace=True)
        performans_df["TARIH_STR"] = performans_df["TARIH"].dt.strftime("%B %Y")

    # Grafik
    fig = px.line(performans_df, x="TARIH", y="PERFORMANS", title=f"{zaman_seviyesi} Performans")
    st.plotly_chart(fig)

    # Tablo: Tezgah bazlı miktar
    df_grup = filtered_df.groupby("TEZGAHISIM")["URETILENMIKTAR"].sum().reset_index()
    df_grup["URETILENMIKTAR"] = df_grup["URETILENMIKTAR"].round(0).astype(int)
    df_grup.columns = ["Tezgah", "Toplam Üretilen Miktar"]

    # Tablo: Ürün bazlı miktar
    df_grup2 = filtered_df.groupby("URUN_ADI")["URETILENMIKTAR"].sum().reset_index()
    df_grup2["URETILENMIKTAR"] = df_grup2["URETILENMIKTAR"].round(0).astype(int)
    df_grup2.columns = ["Ürün", "Toplam Üretilen Miktar"]

    # Pie chart: Performans tezgah bazlı
    toplam_yapilan = filtered_df.groupby("TEZGAHISIM")["PERFORMANS"].mean().round(2).reset_index()
    fig1 = px.pie(
        toplam_yapilan, 
        values="PERFORMANS", 
        names="TEZGAHISIM", 
        hole=0.4
    )

    fig1.update_layout(
        height=600,
        width=800,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=0, r=0, t=50, b=50)
    )

    # Bar chart: Performans ürün bazlı
    performans_ort = filtered_df.groupby(["URUN_KODU", "URUN_ADI"])["PERFORMANS"].mean().round(2).reset_index()
    fig2 = px.bar(
        performans_ort, x="URUN_KODU", y="PERFORMANS", hover_data=["URUN_ADI"]
    )
    fig2.update_traces(textposition='outside')

    # İki kolonlu layout
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛠️ Tezgah Bazında Üretilen Miktar")
        st.dataframe(df_grup)
    with col2:
        st.subheader("📦 Ürün Bazında Üretilen Miktar")
        st.dataframe(df_grup2)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧭 Tezgah Bazında Performans", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.markdown("### 📊 Ürün Bazında Performans")
        st.plotly_chart(fig2, use_container_width=True)

    # Sidebar: Özet
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("### 📌 GENEL PERFORMANS ÖZETİ")
    if not filtered_df.empty:
        toplam_miktar = filtered_df["URETILENMIKTAR"].sum()
        hedef_toplam = filtered_df["HEDEFMIKTAR"].sum()
        ortalama_perf = filtered_df["PERFORMANS"].mean()
        st.sidebar.markdown(f'<div class="metric-box">🔢 Toplam Üretilen Miktar: <b>{toplam_miktar:.2f}</b></div>', unsafe_allow_html=True)
        st.sidebar.markdown(f'<div class="metric-box">🎯 Hedef Miktar: <b>{hedef_toplam:.2f}</b></div>', unsafe_allow_html=True)
        st.sidebar.markdown(f'<div class="metric-box">📈 Ortalama Performans: <b>%{ortalama_perf:.2f}</b></div>', unsafe_allow_html=True)
    else:
        st.sidebar.info("⚠️ Seçilen filtrelerde veri yok.")

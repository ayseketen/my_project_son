import streamlit as st
import pandas as pd
import plotly.express as px
from style import apply_custom_styles  # Ortak stil dosyası
def run_ariza_durus():
    
    # Sayfa genişliği artırıldı
    #st.set_page_config(layout="wide")

    apply_custom_styles()
    # csv dosyasını yükle
    url = "https://drive.google.com/uc?id=1W4yLakTlMPAtyAYPUQeXdJXsWx48QtVd&export=download"

    df_all = pd.read_csv(url)
    df = df_all[df_all["AKTIVITEKODU"] == 2]
    df["ARIZA_TURU"] = df.apply(
        lambda row: row["ARIZA"] if pd.notnull(row["ARIZA"]) and str(row["ARIZA"]).strip() != "" else row["ARIZA2"],
        axis=1
    )
    df.drop(columns=["ARIZA", "ARIZA2"], inplace=True)
    df = df.drop_duplicates()

    df["TARIH"] = pd.to_datetime(df["TARIH"])

    # Filtreler
    st.sidebar.markdown('<div class="sidebar-title">🔍 Filtreler</div>', unsafe_allow_html=True)

    tezgah = st.sidebar.multiselect("⚙️ Tezgah", options=sorted(df["TEZGAHISIM"].dropna().unique()))
    bolum = st.sidebar.multiselect("🏭 Bölüm", options=sorted(df["BOLUM"].dropna().unique()))
    tarih_araligi = st.sidebar.date_input(
        "📅 Tarih Aralığı",
        value=[df["TARIH"].min().date(), df["TARIH"].max().date()],
        min_value=df["TARIH"].min().date(),
        max_value=df["TARIH"].max().date()
    )
    filtered_df = df.copy()

    if tezgah:
        filtered_df = filtered_df[filtered_df["TEZGAHISIM"].isin(tezgah)]
    if bolum:
        filtered_df = filtered_df[filtered_df["BOLUM"].isin(bolum)]
    if len(tarih_araligi) == 2:
        start_date, end_date = tarih_araligi
        filtered_df = filtered_df[(filtered_df["TARIH"] >= pd.to_datetime(start_date)) & 
                                (filtered_df["TARIH"] <= pd.to_datetime(end_date))]

    # Line chart
    filtered_df["TARIH"] = filtered_df["TARIH"].dt.normalize()

    durus_line = filtered_df.groupby("TARIH")["SURE_DK"].sum().reset_index()
    durus_line["TARIH"] = pd.to_datetime(durus_line["TARIH"])
    durus_line["TARIH_STR"] = durus_line["TARIH"].dt.strftime("%d %B")
    fig = px.line(durus_line, x="TARIH", y="SURE_DK")
    
    st.plotly_chart(fig)

    # Tablo 1    
    df_grup = filtered_df.groupby("ARIZA_TURU")["SURE_DK"].sum().reset_index()
    df_grup["SURE_DK"] = df_grup["SURE_DK"].round(0).astype(int)
    df_grup.columns = ["Arıza Türü", "Toplam Duruş(Dk)"]

    # Tablo 2   
    df_grup2 = filtered_df.groupby("URUN_ADI")["SURE_DK"].sum().reset_index()
    df_grup2["SURE_DK"] = df_grup2["SURE_DK"].round(0).astype(int)
    df_grup2.columns = ["Ürün", "Toplam Duruş(Dk)"]

    # Pie chart
    durus_pie = filtered_df.groupby("ARIZA_TURU")["SURE_DK"].sum().round(2).reset_index()

    fig1 = px.pie(durus_pie, values="SURE_DK", names="ARIZA_TURU",hole=0.4)
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

    # Ürün bazlı bar chart
    durus_urun = filtered_df.groupby(["OPERATOR_ISIM"])["SURE_DK"].sum().round(2).reset_index()

    fig2 = px.bar(
        durus_urun,
        x="OPERATOR_ISIM",
        y="SURE_DK",
        hover_data=["SURE_DK"],
    )
    fig2.update_traces(textposition='outside')

    # Yerleşim
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Arıza Türü Bazında Toplam Duruş Süresi")
        st.dataframe(df_grup)

    with col2:
        st.subheader("Ürün Bazında Toplam Duruş Süresi")
        st.dataframe(df_grup2)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### Operator Bazında Toplam Duruş")
        st.plotly_chart(fig2, use_container_width=True)

    # Boşluk
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    # Özet
    st.sidebar.markdown("### GENEL ARIZA DURUŞ ÖZETİ")
    if not filtered_df.empty:
        toplam_durus = filtered_df["SURE_DK"].sum()
        toplam_durus_saat = filtered_df["SURE_SAAT"].sum()
        ortalama_durus_suresi = filtered_df["SURE_DK"].dropna().round(2).mean()
        ortalama_durus_suresi = round(ortalama_durus_suresi, 2)

        st.sidebar.markdown(f'<div class="metric-box">⏱️ Toplam Duruş Süresi (Dk): <b>{toplam_durus:.2f}</b></div>', unsafe_allow_html=True)
        st.sidebar.markdown(f'<div class="metric-box">⏳ Toplam Duruş Süresi (Saat): <b>{toplam_durus_saat:.2f}</b></div>', unsafe_allow_html=True)
        st.sidebar.markdown(f'<div class="metric-box">⚙️ Ortalama Duruş Süresi (Dk) - MTTR: <b>{ortalama_durus_suresi:.2f}</b></div>', unsafe_allow_html=True)

    else:
        st.sidebar.write("Seçilen filtrelerde veri yok.")

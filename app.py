import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard PilahSampahKu", 
    page_icon="logo.jpeg", 
    layout="wide"
)

FILE_EXCEL = "Pengelolaan Sampah Kota Kendari.xlsx"

LINK_CSV_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQMkXEziqlICrb87o8KHRGN4sZu3l89R2J6FBxNTlzgHUJ2R4j3fcZf9X8-0eHGYBYyrlbdx82ZJt4u/pub?output=csv"

@st.cache_data(ttl=60)
def ambil_data_realtime():
    return pd.read_csv(LINK_CSV_SHEETS)

try:
    df = ambil_data_realtime()
    
    st.title("📊 Real-Time Dashboard Kuesioner Pilah SampahKu")
    
    total_responden = len(df)
    st.metric(label="Total Responden Saat Ini", value=f"{total_responden} Responden")
    st.markdown("---")

    st.subheader("Pratinjau Data Kuesioner Terbaru")
    df_tampilan = df.tail().copy()
    df_tampilan.index = df_tampilan.index + 1
    st.dataframe(df_tampilan)

    st.subheader("📈 Visualisasi Hasil Kuesioner")
    nama_kolom = df.columns.tolist()
    pilihan_pertanyaan = st.selectbox("Pilih Pertanyaan Kuesioner untuk Dilihat Grafiknya:", nama_kolom)
    
    if pilihan_pertanyaan:
        hitung_jawaban = df[pilihan_pertanyaan].value_counts().reset_index()
        hitung_jawaban.columns = ['Jawaban', 'Jumlah']
        
        fig = px.bar(hitung_jawaban, x='Jawaban', y='Jumlah', 
                     title=f"Distribusi Jawaban untuk: {pilihan_pertanyaan}",
                     color='Jawaban', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Gagal menarik data kuesioner. Pastikan laptopmu terhubung ke internet.")
    st.info(f"Detail error: {e}")



st.markdown("---")
st.header("📊 Data Pengelolaan Sampah Kota Kendari")

try:
    df_komposisi = pd.read_excel(FILE_EXCEL, sheet_name='Komposisi_sampah')
    
    st.subheader("🍃 Komposisi Sampah Berdasarkan Jenis")
    st.write("Komposisi sampah di Kota Kendari didominasi oleh sampah organik, khususnya sisa makanan yang mencapai 57,20% dari total timbulan sampah.")
    
    fig_komposisi = px.pie(
        df_komposisi, 
        values='Persentase (%)', 
        names='Komposisi Sampah',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.YlOrBr
    )
    st.plotly_chart(fig_komposisi, use_container_width=True)
except Exception as e:
    st.warning(f"Gagal memuat data Komposisi Sampah. Detail: {e}")

try:
    df_sumber = pd.read_excel(FILE_EXCEL, sheet_name='Sumber_sampah')
    
    st.subheader("🏢 Volume Sampah Berdasarkan Sumber")
    fig_sumber = px.bar(
        df_sumber, 
        x='Sumber Sampah', 
        y='Ton/hari',
        text='Ton/hari',
        color='Sumber Sampah', 
        color_discrete_sequence=px.colors.qualitative.Pastel, 
        labels={'Sumber Sampah': 'KETERANGAN'} 
    )
    
    fig_sumber.update_traces(texttemplate='%{text}', textposition='outside')
    
    st.plotly_chart(fig_sumber, use_container_width=True)
except Exception as e:
    st.warning(f"Gagal memuat data Sumber Sampah. Detail: {e}")

try:
    df_bank = pd.read_excel(FILE_EXCEL, sheet_name='Bank_sampah')
    
    st.subheader("🏦 Rincian Operasional Bank Sampah")
    st.write("Saat ini terdapat 40 Bank Sampah Unit yang beroperasi di Kota Kendari dengan rincian data operasional sebagai berikut:")
    
    fig_bank = px.bar(
        df_bank, 
        x='KETERANGAN', 
        y='Ton/hari',
        text='Ton/hari',
        color='KETERANGAN',
        color_discrete_sequence=['#3182bd', '#31a354'], # Warna biru dan hijau yang rapi
        title="Perbandingan Volume Sampah yang Masuk vs Terkelola di Bank Sampah Unit"
    )
    
    fig_bank.update_traces(texttemplate='%{text}', textposition='outside')
    
    st.plotly_chart(fig_bank, use_container_width=True)
    
    st.write("Adapun jumlah residu yang dihasilkan dari operasional Bank Sampah tersebut adalah sebesar **13.932,459 ton/tahun**.")
except Exception as e:
    st.warning(f"Gagal memuat grafik Rincian Bank Sampah. Detail: {e}")

try:
    df_pengolahan = pd.read_excel(FILE_EXCEL, sheet_name='Pengolahan_sampah')
    
    st.subheader("♻️ Rincian Pengolahan Sampah Menjadi Bahan Baku")
    
    fig_pengolahan = px.bar(
        df_pengolahan,
        x='KETERANGAN',
        y='Ton/hari',
        text='Ton/hari',
        color='KETERANGAN',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Distribusi Aliran Sampah Menjadi Kompos dan Daur Ulang"
    )
    fig_pengolahan.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig_pengolahan, use_container_width=True)
except Exception as e:
    st.warning(f"Gagal memuat grafik Pengolahan Sampah. Pastikan nama sheet adalah 'Pengolahan_sampah'. Detail: {e}")

try:
    df_neraca = pd.read_excel(FILE_EXCEL, sheet_name='Neraca_sampah')
    
    st.subheader("📊 Neraca Pengelolaan Sampah Tahunan")
    
    fig_neraca = px.bar(
        df_neraca,
        x='KETERANGAN',
        y='TON/TAHUN',
        text='TON/TAHUN',
        color='KETERANGAN',
        color_continuous_scale='Cividis',
        title="Aliran Volume Sampah Tahunan Kota Kendari (Ton/Tahun)"
    )
    fig_neraca.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig_neraca, use_container_width=True)
except Exception as e:
    st.warning(f"Gagal memuat grafik Neraca Sampah. Pastikan nama sheet adalah 'Neraca_sampah'. Detail: {e}")
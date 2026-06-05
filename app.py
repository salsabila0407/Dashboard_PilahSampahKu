import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# PERBAIKAN UTAMA: Set halaman website HARUS ditaruh paling atas!
# ==============================================================================
st.set_page_config(
    page_title="Dashboard PilahSampahKu", 
    page_icon="logo.jpeg",  # <-- Ganti dengan nama file gambar kamu
    layout="wide"
)

# ==============================================================================
# TAHAP 1: MASUKKAN LINK KAMU DI SINI
# ==============================================================================
# PENTING: Ganti teks di bawah dengan link panjang "Publish to Web" milikmu!
LINK_CSV_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQMkXEziqlICrb87o8KHRGN4sZu3l89R2J6FBxNTlzgHUJ2R4j3fcZf9X8-0eHGYBYyrlbdx82ZJt4u/pub?output=csv"

# Fungsi otomatis untuk menarik data secara real-time dari internet
@st.cache_data(ttl=60) # Data otomatis di-refresh tiap 60 detik jika halaman dibuka
def ambil_data_realtime():
    return pd.read_csv(LINK_CSV_SHEETS)

# Membaca data dan memasukkannya ke variabel 'df'
try:
    df = ambil_data_realtime()
    
    # ==============================================================================
    # TAHAP 2: ATUR TAMPILAN DASHBOARD WEB
    # ==============================================================================
    st.title("📊 Real-Time Dashboard Kuesioner Pilah SampahKu")
    
    # Menampilkan total warga Kendari yang sudah mengisi
    total_responden = len(df)
    st.metric(label="Total Responden Saat Ini", value=f"{total_responden} Responden")
    st.markdown("---") # Membuat garis pembatas visual

    # Menampilkan pratinjau tabel kuesioner terbaru
    st.subheader("Pratinjau Data Kuesioner Terbaru")

    # PERBAIKAN: Mengambil 5 data terbawah (terbaru) dari kuesioner
    df_tampilan = df.tail().copy()
    df_tampilan.index = df_tampilan.index + 1
    st.dataframe(df_tampilan)

    # ==============================================================================
    # TAHAP 3: MEMBUAT GRAFIK INTERAKTIF
    # ==============================================================================
    st.subheader("📈 Visualisasi Hasil Kuesioner")
    
    # Ambil daftar nama kolom/pertanyaan dari Google Sheets kamu
    nama_kolom = df.columns.tolist()
    
    # Membuat pilihan grafik dinamis berdasarkan pertanyaan yang ada di kuesionermu
    pilihan_pertanyaan = st.selectbox("Pilih Pertanyaan Kuesioner untuk Dilihat Grafiknya:", nama_kolom)
    
    if pilihan_pertanyaan:
        # Menghitung total jawaban
        hitung_jawaban = df[pilihan_pertanyaan].value_counts().reset_index()
        hitung_jawaban.columns = ['Jawaban', 'Jumlah']
        
        # Membuat grafik batang interaktif
        fig = px.bar(hitung_jawaban, x='Jawaban', y='Jumlah', 
                     title=f"Distribusi Jawaban untuk: {pilihan_pertanyaan}",
                     color='Jawaban', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Gagal menarik data. Pastikan link yang kamu paste sudah benar dan laptopmu terhubung ke internet.")
    st.info(f"Detail error: {e}")
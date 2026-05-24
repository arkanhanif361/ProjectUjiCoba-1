import streamlit as st
import random

# Konfigurasi halaman utama
st.set_page_config(page_title="Smart Reagent Maker & Game", page_icon="🧪", layout="wide")

# Database reagen dasar untuk Kalkulator & Game
DATABASE_KIMIA = {
    "Asam Klorida (HCl)": {"bm": 36.46, "kadar": 37, "bj": 1.19, "rumus": "HCl"},
    "Asam Sulfat (H2SO4)": {"bm": 98.08, "kadar": 98, "bj": 1.84, "rumus": "H2SO4"},
    "Asam Nitrat (HNO3)": {"bm": 63.01, "kadar": 65, "bj": 1.42, "rumus": "HNO3"},
    "Amonia (NH4OH)": {"bm": 35.05, "kadar": 25, "bj": 0.90, "rumus": "NH4OH"},
}

# Inisialisasi Session State untuk Game agar data tidak hilang saat tombol diklik
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'soal_aktif' not in st.session_state:
    st.session_state.soal_aktif = False
if 'kunci_jawaban' not in st.session_state:
    st.session_state.kunci_jawaban = 0.0

# Sidebar Navigasi
menu = st.sidebar.radio("Pilih Menu Aplikasi:", ["1. Kalkulator Reagen Pekat", "2. Game: Lab Assistant Challenge 🎮"])

# ==============================================================================
# MENU 1: KALKULATOR REAGEN
# ==============================================================================
if menu == "1. Kalkulator Reagen Pekat":
    st.title("🧪 Kalkulator Pembuatan Reagen Cairan Pekat")
    st.write("Gunakan menu ini untuk menghitung volume pemipetan reagen pekat di laboratorium.")
    
    # (Logika kalkulator dari kode sebelumnya ditaruh di sini...)
    pilihan_zat = st.selectbox("Pilih Zat Kimia:", list(DATABASE_KIMIA.keys()))
    data = DATABASE_KIMIA[pilihan_zat]
    
    st.info(#Rumus inline untuk tampilan kimia yang rapi
        f"**Spesifikasi Botol Induk ({data['rumus']}):** "
        f"BM = {data['bm']} g/mol | Kadar = {data['kadar']}% | Berat Jenis = {data['bj']} g/mL"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        m2 = st.number_input("Konsentrasi Target (Molaritas, M):", min_value=0.01, value=0.10, step=0.01)
    with col2:
        v2 = st.number_input("Volume Target yang Ingin Dibuat (mL):", min_value=1.0, value=100.0, step=10.0)
        
    if st.button("Hitung Volume Pipet"):
        m1 = (data['bj'] * data['kadar'] * 10) / data['bm']
        v1 = (m2 * v2) / m1
        st.success(f"### Hasil: Pipet sebanyak **{v1:.2f} mL** larutan pekat.")


# ==============================================================================
# MENU 2: GAMES / LATIHAN SOAL
# ==============================================================================
elif menu == "2. Game: Lab Assistant Challenge 🎮":
    st.title("🎮 Game: Lab Assistant Challenge")
    st.write("Uji kemampuan hitung cepatmu dalam mempersiapkan reagen laboratorium! Selesaikan soal di bawah ini.")
    
    # Tampilkan Skor saat ini
    st.sidebar.metric(label="Skor Anda ⭐", value=st.session_state.score)
    
    # Tombol untuk generate soal baru
    if st.button("Generate Soal Baru 🎲") or not st.session_state.soal_aktif:
        # Acak zat kimia
        nama_zat = random.choice(list(DATABASE_KIMIA.keys()))
        zat_terpilih = DATABASE_KIMIA[nama_zat]
        
        # Acak target konsentrasi dan volume
        target_m = round(random.uniform(0.05, 1.5), 2)  # Molaritas acak antara 0.05 - 1.5 M
        target_v = random.choice([50, 100, 250, 500])   # Ukuran labu takar yang umum
        
        # Hitung kunci jawaban (V1)
        m1_hidden = (zat_terpilih['bj'] * zat_terpilih['kadar'] * 10) / zat_terpilih['bm']
        v1_hidden = (target_m * target_v) / m1_hidden
        
        # Simpan soal ke dalam session state
        st.session_state.soal_teks = f"Anda diminta membuat larutan **{nama_zat} ({zat_terpilih['rumus']})** dengan konsentrasi **{target_m} M** sebanyak **{target_v} mL**."
        st.session_state.info_zat = f"Label botol induk: Kadar = {zat_terpilih['kadar']}%, Berat Jenis = {zat_terpilih['bj']} g/mL, BM = {zat_terpilih['bm']} g/mol"
        st.session_state.kunci_jawaban = round(v1_hidden, 2)
        st.session_state.soal_aktif = True
        st.session_state.status_jawab = None

    # Tampilkan soal yang sedang aktif
    st.info(st.session_state.soal_teks)
    st.caption(st.session_state.info_zat)
    
    # Input jawaban dari user
    jawaban_user = st.number_input("Berapa mL volume larutan pekat yang harus dipipet? (Isi hingga 2 angka di belakang koma)", min_value=0.00, step=0.01, format="%.2f")
    
    if st.button("Submit Jawaban 🚀"):
        # Cek apakah jawaban user mendekati kunci jawaban (toleransi eor 0.02 mL karena pembulatan)
        selisih = abs(jawaban_user - st.session_state.kunci_jawaban)
        
        if selisih <= 0.02:
            st.balloons()
            st.success(f"🎉 **BENAR!** Jawaban Anda tepat. Kunci jawaban: {st.session_state.kunci_jawaban} mL.")
            if st.session_state.status_jawab != "Benar":
                st.session_state.score += 10  # Tambah skor 10
                st.session_state.status_jawab = "Benar"
        else:
            st.error(f"❌ **SALAH.** Coba hitung kembali M1 atau rumus pengencerannya! (Hint: Cari M1 pekat dulu).")
            
    if st.button("Menyerah & Lihat Kunci Jawaban 👁️"):
        st.warning(f"Kunci jawaban untuk soal ini adalah: **{st.session_state.kunci_jawaban} mL**")
        

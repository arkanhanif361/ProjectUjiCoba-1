import streamlit as st

st.title("🎈 EEEEE A")
import streamlit as st

# 1. Judul Aplikasi
st.title("🔢 Kalkulator Sederhana")
st.write("Aplikasi kalkulator interaktif menggunakan Streamlit.")

# Buat garis pembatas
st.divider()

# 2. Input Angka dari User
# min_value=None artinya bisa input angka negatif maupun positif
angka_pertama = st.number_input("Masukkan angka pertama:", value=0.0, step=1.0)
angka_kedua = st.number_input("Masukkan angka kedua:", value=0.0, step=1.0)

# 3. Pilihan Operasi Matematika
operasi = st.selectbox(
    "Pilih operasi matematika:",
    ("Pertambahan (+)", "Pengurangan (-)", "Perkalian (×)", "Pembagian (÷)")
)

# Buat tombol untuk memicu kalkulasi
hitung = st.button("Hitung Hasil")

# 4. Logika Kalkulator
if hitung:
    hasil = 0
    error_message = None

    if operasi == "Pertambahan (+)":
        hasil = angka_pertama + angka_kedua
    elif operasi == "Pengurangan (-)":
        hasil = angka_pertama - angka_kedua
    elif operasi == "Perkalian (×)":
        hasil = angka_pertama * angka_kedua
    elif operasi == "Pembagian (÷)":
        # Antisipasi error pembagian dengan angka nol
        if angka_kedua != 0:
            hasil = angka_pertama / angka_kedua
        else:
            error_message = "❌ Error: Tidak bisa membagi dengan angka nol!"

    # 5. Menampilkan Hasil
    st.divider()
    if error_message:
        st.error(error_message)
    else:
        # Menampilkan hasil dengan format box sukses yang menarik
        st.success(f"Hasil dari {angka_pertama} jika diselesaikan dengan {operasi} bersama {angka_kedua} adalah:")
        st.metric(label="Hasil Akhir", value=f"{hasil:,}")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df

day_df = load_data()

# Set style
plt.style.use("ggplot")

# Title utama
st.title("Dashboard Analisis Penyewaan Sepeda")

# 1. Tren Penyewaan Sepeda per Bulan
st.subheader("Tren Penyewaan Sepeda per Bulan")

# Agregasi jumlah penyewaan per bulan
monthly_rentals = day_df.groupby("mnth", as_index=False)["cnt"].sum()

# Buat figure
fig1, ax1 = plt.subplots(figsize=(10, 5))

# Visualisasi dengan bar chart (pilih main satu solusi)
sns.barplot(data=monthly_rentals, x="mnth", y="cnt", hue="mnth", dodge=False, palette="coolwarm")  # Solusi 1
# sns.barplot(data=monthly_rentals, x="mnth", y="cnt")  # Solusi 2 (tanpa warna)

# Tambahkan judul dan label
plt.title("Tren Penyewaan Sepeda per Bulan", fontsize=14, fontweight="bold")
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Jumlah Penyewaan", fontsize=12)
plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])

# Tambahkan grid horizontal
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Tampilkan plot
st.pyplot(fig1)

# 2. Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari
st.subheader("Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari")

# Cek apakah kolom 'hr' ada di dataset
if 'hr' in day_df.columns:
    # Agregasi jumlah penyewaan per jam
    hourly_rentals = day_df.groupby("hr", as_index=False)["cnt"].mean()
    
    # Buat figure
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    # Visualisasi dengan line chart
    sns.lineplot(x=hourly_rentals["hr"], y=hourly_rentals["cnt"], marker="o", color="red")
    
    # Tambahkan judul dan label
    plt.title("Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari", fontsize=14, fontweight="bold")
    plt.xlabel("Jam", fontsize=12)
    plt.ylabel("Rata-rata Penyewaan", fontsize=12)
    
    # Tambahkan grid horizontal
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Tampilkan plot
    st.pyplot(fig2)
else:
    # Jika tidak ada kolom 'hr'
    st.write("Data tidak memiliki informasi jam ('hr'). Mungkin perlu memuat dataset terpisah.")

# 3. Pengaruh Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

# Mapping kondisi cuaca untuk memudahkan interpretasi
weather_conditions = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}

# Buat salinan dataframe agar tidak mengubah dataframe awal
weather_df = day_df.copy()

# Konversi kode numerik ke deskripsi kondisi cuaca
if 'weathersit' in weather_df.columns:
    weather_df['weathersit'] = weather_df['weathersit'].map(weather_conditions)
    
    # Agregasi jumlah penyewaan berdasarkan kondisi cuaca
    weather_rentals = weather_df.groupby("weathersit", as_index=False)["cnt"].mean()
    
    # Buat figure
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    
    # Visualisasi dengan bar chart
    sns.barplot(x=weather_rentals["weathersit"], y=weather_rentals["cnt"], palette="coolwarm", dodge=False)
    
    # Tambahkan judul dan label
    plt.title("Pengaruh Cuaca terhadap Penyewaan Sepeda", fontsize=14, fontweight="bold")
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Rata-rata Penyewaan")
    
    # Tambahkan grid horizontal
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Sembunyikan legend karena tidak diperlukan
    plt.legend([], [], frameon=False)
    
    # Tampilkan plot
    st.pyplot(fig3)
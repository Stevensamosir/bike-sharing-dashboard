import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# ==========================
# LOAD DATA
# ==========================
# Karena file ini di dalam folder "dashboard", kita ambil CSV dari ../data/
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# ==========================
# JUDUL APP
# ==========================
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")

# ==========================
# SIDEBAR FILTERS
# ==========================
st.sidebar.header("🎛️ Filter Data")

selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=day_df["weathersit"].unique(),
    default=day_df["weathersit"].unique()
)

selected_workingday = st.sidebar.radio(
    "Pilih Hari",
    ["Semua", "Akhir Pekan", "Hari Kerja"],
    index=0
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim (Untuk Visualisasi Jam)",
    options=hour_df["season"].unique(),
    default=hour_df["season"].unique()
)

# ==========================
# FILTERING DATA
# ==========================
if selected_workingday == "Semua":
    filtered_day_df = day_df[day_df["weathersit"].isin(selected_weather)]
    filtered_hour_df = hour_df[hour_df["season"].isin(selected_season)]
else:
    workingday_map = {"Hari Kerja": 1, "Akhir Pekan": 0}
    filtered_day_df = day_df[
        (day_df["weathersit"].isin(selected_weather)) &
        (day_df["workingday"] == workingday_map[selected_workingday])
    ]
    filtered_hour_df = hour_df[
        (hour_df["workingday"] == workingday_map[selected_workingday]) &
        (hour_df["season"].isin(selected_season))
    ]

# ==========================
# VISUALISASI 1: Cuaca vs Jumlah Sewa
# ==========================
st.subheader("☁️ Pengaruh Cuaca terhadap Penyewaan Sepeda")

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='weathersit',
    y='cnt',
    hue='workingday',
    data=filtered_day_df,
    palette={0: 'red', 1: 'green'}
)
plt.title('Jumlah Penyewaan Berdasarkan Cuaca')
plt.xlabel('Kondisi Cuaca (1=Cerah, 2=Mendung, 3=Hujan)')
plt.ylabel('Jumlah Penyewaan')
legend_akhir_pekan = mlines.Line2D([], [], color='red', label='Akhir Pekan', linewidth=6)
legend_hari_kerja = mlines.Line2D([], [], color='green', label='Hari Kerja', linewidth=6)
plt.legend(handles=[legend_akhir_pekan, legend_hari_kerja], title='Hari', loc='upper right', frameon=False)
st.pyplot(fig1)

# ==========================
# KESIMPULAN VISUAL 1
# ==========================
st.markdown("### 📌 Kesimpulan Visualisasi 1")
st.write("""
Cuaca sangat mempengaruhi jumlah penyewaan sepeda. Jumlah penyewaan paling tinggi terjadi saat cuaca cerah atau mendung ringan.
Saat hujan, penyewaan turun drastis baik di hari kerja maupun akhir pekan.
""")

# ==========================
# VISUALISASI 2: Jam vs Jumlah Sewa
# ==========================
st.subheader("⏰ Pola Penyewaan Sepeda Berdasarkan Jam")

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='hr',
    y='cnt',
    hue='season',
    data=filtered_hour_df,
    palette='tab10'
)
plt.title('Pola Penyewaan Sepeda per Jam')
plt.xlabel('Jam (0-23)')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Musim', labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
st.pyplot(fig2)

# ==========================
# KESIMPULAN VISUAL 2
# ==========================
st.markdown("### 📌 Kesimpulan Visualisasi 2")
st.write("""
Pada hari kerja, penyewaan sepeda memiliki pola puncak di pagi dan sore hari, mencerminkan jam sibuk.
Sementara akhir pekan menunjukkan pola yang lebih merata sepanjang hari.
Musim panas dan gugur cenderung memiliki penyewaan terbanyak, sementara musim dingin paling sedikit.
""")

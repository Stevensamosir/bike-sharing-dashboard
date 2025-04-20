import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Load dataset
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Konversi kolom tanggal ke datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Filter data setahun terakhir
last_year_date = day_df['dteday'].max() - pd.DateOffset(years=1)
day_df = day_df[day_df['dteday'] >= last_year_date]
hour_df = hour_df[hour_df['dteday'] >= last_year_date]

# Streamlit App Title
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", day_df["weathersit"].unique(), default=day_df["weathersit"].unique())
selected_workingday = st.sidebar.radio("Pilih Hari", ["Semua", "Akhir Pekan", "Hari Kerja"], index=0)

# Mapping Working Day Filter
if selected_workingday == "Semua":
    filtered_day_df = day_df[day_df["weathersit"].isin(selected_weather)]
    filtered_hour_df = hour_df[hour_df["weathersit"].isin(selected_weather)]
else:
    workingday_map = {"Hari Kerja": 1, "Akhir Pekan": 0}
    filtered_day_df = day_df[(day_df["weathersit"].isin(selected_weather)) & (day_df["workingday"] == workingday_map[selected_workingday])]
    filtered_hour_df = hour_df[(hour_df["weathersit"].isin(selected_weather)) & (hour_df["workingday"] == workingday_map[selected_workingday])]

# --- Visualisasi 1: Pengaruh Cuaca terhadap Penyewaan Sepeda ---
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='weathersit', y='cnt', hue='workingday', data=filtered_day_df, palette={0: 'red', 1: 'green'})
plt.title('Pengaruh Cuaca terhadap Penyewaan Sepeda (Hari Kerja vs Akhir Pekan)')
plt.xlabel('Kondisi Cuaca (1=Cerah, 2=Mendung, 3=Hujan)')
plt.ylabel('Jumlah Penyewaan')
legend_akhir_pekan = mlines.Line2D([], [], color='red', label='Akhir Pekan', linewidth=6)
legend_hari_kerja = mlines.Line2D([], [], color='green', label='Hari Kerja', linewidth=6)
plt.legend(handles=[legend_akhir_pekan, legend_hari_kerja], title='Hari', loc='upper right', frameon=False)
st.pyplot(fig)

# --- Conclusion 1 ---
st.markdown("### Kesimpulan Pertanyaan 1")
max_cuaca = filtered_day_df.groupby('weathersit')['cnt'].mean().idxmax()
cuaca_map = {1: "Cerah", 2: "Mendung", 3: "Hujan"}
st.write(f"Penyewaan sepeda paling tinggi terjadi saat cuaca **{cuaca_map[max_cuaca]}**.")
st.write("Cuaca buruk seperti hujan menyebabkan penurunan drastis penyewaan, baik di hari kerja maupun akhir pekan.")
st.write("Disarankan untuk menyediakan alternatif moda transportasi saat cuaca buruk, atau promosi di musim cerah.")

# --- Visualisasi 2: Pola Penyewaan Sepeda Berdasarkan Jam (workingday) ---
st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', hue='workingday', data=filtered_hour_df, palette={0: 'red', 1: 'green'})
plt.title('Pola Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Hari', labels=['Akhir Pekan', 'Hari Kerja'])
st.pyplot(fig)

# --- Conclusion 2 ---
st.markdown("### Kesimpulan Pertanyaan 2")
peak_hour = filtered_hour_df.groupby('hr')['cnt'].mean().idxmax()
peak_value = round(filtered_hour_df.groupby('hr')['cnt'].mean().max(), 2)
st.write(f"Puncak penyewaan sepeda terjadi pada pukul **{peak_hour}:00** dengan rata-rata penyewaan **{peak_value} sepeda**.")
st.write("Hari kerja menunjukkan dua puncak utama (pagi & sore), sementara akhir pekan lebih stabil sepanjang hari.")
st.write("Disarankan untuk menambah jumlah sepeda dan pelayanan pada jam-jam sibuk tersebut, khususnya di hari kerja.")



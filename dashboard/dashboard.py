import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Load dataset
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Streamlit App Title
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", day_df["weathersit"].unique(), default=day_df["weathersit"].unique())
selected_workingday = st.sidebar.radio("Pilih Hari", ["Semua", "Akhir Pekan", "Hari Kerja"], index=0)

# Mapping Working Day Filter
if selected_workingday == "Semua":
    # Tampilkan semua hari kerja dan akhir pekan jika "Semua" dipilih
    filtered_day_df = day_df[day_df["weathersit"].isin(selected_weather)]
else:
    workingday_map = {"Hari Kerja": 1, "Akhir Pekan": 0}
    filtered_day_df = day_df[(day_df["weathersit"].isin(selected_weather)) & (day_df["workingday"] == workingday_map[selected_workingday])]

# Visualization 1: Pengaruh Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='weathersit', y='cnt', hue='workingday', data=filtered_day_df, palette={0: 'red', 1: 'green'})
plt.title('Pengaruh Cuaca terhadap Penyewaan Sepeda (Hari Kerja vs Akhir Pekan)')
plt.xlabel('Kondisi Cuaca (1=Cerah, 2=Mendung, 3=Hujan)')
plt.ylabel('Jumlah Penyewaan')
legend_akhir_pekan = mlines.Line2D([], [], color='red', label='Akhir Pekan', linewidth=6)
legend_hari_kerja = mlines.Line2D([], [], color='green', label='Hari Kerja', linewidth=6)
plt.legend(handles=[legend_akhir_pekan, legend_hari_kerja], title='Hari Kerja', loc='upper right', frameon=False)
st.pyplot(fig)

# Conclusion 1
st.markdown("### Conclusion Pertanyaan 1")
st.write("Cuaca memiliki dampak yang cukup signifikan terhadap jumlah penyewaan sepeda. Pengguna lebih cenderung menyewa sepeda pada kondisi cuaca cerah atau mendung ringan. Pada kondisi hujan, jumlah penyewaan turun drastis, baik di hari kerja maupun akhir pekan.")

# Visualization 2: Pola Penyewaan Sepeda Berdasarkan Jam
st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")

# Filter berdasarkan hari kerja dan akhir pekan
if selected_workingday == "Semua":
    filtered_hour_df = hour_df[hour_df['season'].isin(selected_weather)]
else:
    workingday_map = {"Hari Kerja": 1, "Akhir Pekan": 0}
    filtered_hour_df = hour_df[(hour_df['workingday'] == workingday_map[selected_workingday]) & (hour_df['season'].isin(selected_weather))]

# Lineplot untuk hari kerja
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', hue='season', data=filtered_hour_df, palette='tab10')

# Fix for the syntax error - using format() instead of f-strings
if selected_workingday != "Semua":
    title = 'Pola Penyewaan Sepeda Berdasarkan Jam ({})'.format(selected_workingday)
else:
    title = 'Pola Penyewaan Sepeda Berdasarkan Jam'
    
plt.title(title)
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Musim', labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
st.pyplot(fig)

# Conclusion 2
st.markdown("### Conclusion Pertanyaan 2")
st.write("Penyewaan sepeda pada hari kerja memiliki pola yang jelas, dengan puncak di jam sibuk pagi dan sore. Pada akhir pekan, jumlah penyewaan lebih merata sepanjang hari tanpa puncak yang signifikan. Musim panas dan gugur adalah musim dengan penyewaan tertinggi, sedangkan musim dingin memiliki penyewaan terendah. Waktu terbaik untuk menyewa sepeda pada hari kerja adalah pagi dan sore, sedangkan di akhir pekan lebih fleksibel sepanjang hari.")
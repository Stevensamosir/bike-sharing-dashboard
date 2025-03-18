import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
all_data = pd.read_csv("main_data.csv")
all_data['dteday'] = pd.to_datetime(all_data['dteday'])

# Sidebar untuk filter data berdasarkan rentang waktu
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.header("Filter Data")
    start_date, end_date = st.date_input("Pilih Rentang Waktu", [all_data['dteday'].min(), all_data['dteday'].max()])
    
    filtered_data = all_data[(all_data['dteday'] >= pd.Timestamp(start_date)) & (all_data['dteday'] <= pd.Timestamp(end_date))]

# Title utama
st.title("Dashboard Analisis Penyewaan Sepeda")

# Set style ggplot
plt.style.use("ggplot")

### 📌 1. Tren Penyewaan Sepeda per Bulan ###
st.subheader("Tren Penyewaan Sepeda per Bulan")
monthly_rentals = filtered_data.groupby('mnth')['cnt'].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(
    data=monthly_rentals, x="mnth", y="cnt", hue="mnth", dodge=False, palette="coolwarm"
)

plt.title("Tren Penyewaan Sepeda per Bulan", fontsize=14, fontweight="bold")
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Jumlah Penyewaan", fontsize=12)
plt.xticks(
    ticks=range(0, 12),
    labels=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend([], [], frameon=False)  # Hilangkan legend

st.pyplot(plt)

### 📌 2. Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari ###
st.subheader("Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari")
if 'hr' in filtered_data.columns:
    hourly_rentals = filtered_data.groupby('hr')['cnt'].mean().reset_index()
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=hourly_rentals['hr'], y=hourly_rentals['cnt'], marker='o', color="red")

    plt.title("Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari", fontsize=14, fontweight="bold")
    plt.xlabel("Jam", fontsize=12)
    plt.ylabel("Rata-rata Penyewaan", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(plt)
else:
    st.write("Data tidak memiliki informasi jam ('hr').")

### 📌 3. Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca ###
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

weather_conditions = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}
filtered_data['weathersit'] = filtered_data['weathersit'].map(weather_conditions)

plt.figure(figsize=(8, 5))
sns.boxplot(
    x="weathersit", y="cnt", data=filtered_data, hue="weathersit", palette="coolwarm"
)

plt.title("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight="bold")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(plt)

### 📌 4. Pengaruh Cuaca terhadap Penyewaan Sepeda ###
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

weather_rentals = filtered_data.groupby('weathersit')['cnt'].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x=weather_rentals['weathersit'], y=weather_rentals['cnt'], palette='coolwarm')

plt.title("Pengaruh Cuaca terhadap Penyewaan Sepeda", fontsize=14, fontweight="bold")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Rata-rata Penyewaan")
plt.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(plt)


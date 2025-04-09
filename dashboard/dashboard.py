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

# Set style biar mirip Matplotlib
plt.style.use("ggplot")

# Sidebar untuk filter interaktif
st.sidebar.header("🔍 Filter Interaktif")

# Opsi musim (season)
season_options = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim (Season)", 
    options=list(season_options.keys()), 
    format_func=lambda x: season_options[x],
    default=list(season_options.keys())
)

# Opsi cuaca (weathersit)
weather_options = {
    1: "Clear",
    2: "Mist + Cloudy",
    3: "Light Snow/Rain",
    4: "Heavy Rain/Ice"
}
selected_weathers = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca", 
    options=list(weather_options.keys()), 
    format_func=lambda x: weather_options[x],
    default=list(weather_options.keys())
)

# Filter data berdasarkan input user
filtered_df = day_df[
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weathersit'].isin(selected_weathers))
]

# Title utama
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")

# 1. Tren Penyewaan Sepeda per Hari
st.subheader("Tren Penyewaan Sepeda per Hari")
monthly_rentals = filtered_df.groupby("dteday", as_index=False)["cnt"].sum()

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=monthly_rentals['dteday'], y=monthly_rentals['cnt'], color='blue', marker='o', ax=ax1)

ax1.set_title("Tren Penyewaan Sepeda per Hari", fontsize=14, fontweight="bold")
ax1.set_xlabel("Tanggal", fontsize=12)
ax1.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, linestyle="--", alpha=0.7)
st.pyplot(fig1)

# 2. Distribusi Penyewaan Sepeda Berdasarkan Jam
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Jam")
if 'hr' in filtered_df.columns:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.boxplot(x=filtered_df['hr'], y=filtered_df['cnt'], palette="coolwarm", ax=ax2)
    ax2.set_title("Distribusi Penyewaan Sepeda Berdasarkan Jam", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Jam", fontsize=12)
    ax2.set_ylabel("Jumlah Penyewaan", fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig2)
else:
    st.write("Data tidak memiliki informasi jam ('hr').")

# 3. Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
if 'weathersit' in filtered_df.columns:
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.violinplot(x=filtered_df['weathersit'], y=filtered_df['cnt'], palette="coolwarm", ax=ax3)
    ax3.set_title("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight="bold")
    ax3.set_xlabel("Kondisi Cuaca", fontsize=12)
    ax3.set_ylabel("Jumlah Penyewaan", fontsize=12)
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig3)
else:
    st.write("Data tidak memiliki informasi cuaca ('weathersit').")

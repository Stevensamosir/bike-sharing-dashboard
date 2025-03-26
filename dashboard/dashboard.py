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

# Title utama
st.title("Dashboard Analisis Penyewaan Sepeda")

# **1. Tren Penyewaan Sepeda per Hari**
st.subheader("Tren Penyewaan Sepeda per Hari")

# Agregasi data per hari
monthly_rentals = day_df.groupby("dteday", as_index=False)["cnt"].sum()

# Buat figure
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=monthly_rentals['dteday'], y=monthly_rentals['cnt'], color='blue', marker='o', ax=ax1)

# Tambahkan judul dan label
ax1.set_title("Tren Penyewaan Sepeda per Hari", fontsize=14, fontweight="bold")
ax1.set_xlabel("Tanggal", fontsize=12)
ax1.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, linestyle="--", alpha=0.7)

# Tampilkan plot di Streamlit
st.pyplot(fig1)

# **2. Distribusi Penyewaan Sepeda Berdasarkan Jam**
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Jam")

# Cek apakah kolom 'hr' ada di dataset
if 'hr' in day_df.columns:
    # Buat figure
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    sns.boxplot(x=day_df['hr'], y=day_df['cnt'], palette="coolwarm", ax=ax2)
    
    # Tambahkan judul dan label
    ax2.set_title("Distribusi Penyewaan Sepeda Berdasarkan Jam", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Jam", fontsize=12)
    ax2.set_ylabel("Jumlah Penyewaan", fontsize=12)
    
    # Tambahkan grid horizontal
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tampilkan plot
    st.pyplot(fig2)
else:
    st.write("Data tidak memiliki informasi jam ('hr').")

# **3. Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca**
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

# Cek apakah kolom 'weathersit' ada di dataset
if 'weathersit' in day_df.columns:
    # Buat figure
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    
    sns.violinplot(x=day_df['weathersit'], y=day_df['cnt'], palette="coolwarm", ax=ax3)
    
    # Tambahkan judul dan label
    ax3.set_title("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight="bold")
    ax3.set_xlabel("Kondisi Cuaca", fontsize=12)
    ax3.set_ylabel("Jumlah Penyewaan", fontsize=12)
    
    # Tambahkan grid horizontal
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tampilkan plot
    st.pyplot(fig3)
else:
    st.write("Data tidak memiliki informasi cuaca ('weathersit').")

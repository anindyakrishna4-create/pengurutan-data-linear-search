# File: app.py (Revisi Final - Linear Search)

import streamlit as st
import pandas as pd
import time
from linear_search import linear_search 
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab: Linear Search",
    layout="wide"
)

st.title("🔎 Virtual Lab: Linear Search Interaktif (Matplotlib)")
st.markdown("### Visualisasi Algoritma Pencarian Sekuensial")

st.sidebar.header("Konfigurasi Data dan Target")

# --- Input Data (Tanpa Batas Input) ---
default_data = "12, 45, 90, 3, 55, 18, 70, 25, 60"
input_data_str = st.sidebar.text_input(
    "Masukkan data (pisahkan dengan koma, misalnya 10, 5, 20):", 
    default_data
)
target_value_str = st.sidebar.text_input("Masukkan Nilai Target yang Dicari:", "18")
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

# --- Proses Data Input ---
try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    if not data_list:
        st.error("Masukkan setidaknya satu angka untuk array.")
        st.stop()
    target_value = int(target_value_str.strip())
    initial_data = list(data_list)
except ValueError:
    st.error("Pastikan semua input data dan target adalah angka (integer) yang dipisahkan oleh koma.")
    st.stop()

# ----------------------------------------------------
# --- BAGIAN REVISI: Hapus Kode Heksadesimal ---
# ----------------------------------------------------
st.markdown("""
#### Pewarnaan Bar:
* **Kuning:** Indeks yang **sedang dicek** pada langkah ini.
* **Hijau:** Indeks di mana nilai **ditemukan**.
* **Merah:** Indeks yang **sudah dicek** dan bukan target.
* **Biru:** Indeks yang **belum dicek**.
""")
# ----------------------------------------------------

st.write(f"**Array Awal:** {initial_data}")
st.write(f"**Nilai Target:** **{target_value}**")

# --- Fungsi Plot Matplotlib (TIDAK BERUBAH) ---
def plot_array(arr, target, current_index, found_index, max_val, status):
    # Menggunakan kode warna heksadesimal internal untuk Matplotlib
    # #F1C232 (Kuning), #6AA84F (Hijau), #CC0000 (Merah), #4A86E8 (Biru)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    n = len(arr)
    x_pos = np.arange(n)
    
    colors = ['#4A86E8'] * n # Default (Biru: Belum dicek)
    
    for i in range(n):
        # Merah (Sudah Dicek tapi Bukan Target)
        if status not in ('Mulai', 'Selesai') and i < current_index:
            colors[i] = '#CC0000'

        # Kuning (Sedang Dicek)
        if status == 'Mengecek' and i == current_index:
            colors[i] = '#F1C232'
        
        # Hijau (Ditemukan)
        if found_index != -1 and i == found_index:
            colors[i] = '#6AA84F'

    # Membuat Bar Plot
    ax.bar(x_pos, arr, color=colors)
    
    # Menambahkan Label Angka di Atas Bar
    for i, height in enumerate(arr):
        ax.text(x_pos[i], height + max_val * 0.02, str(height), ha='center', va='bottom', fontsize=10)
        
    # Konfigurasi Grafik
    ax.set_ylim(0, max_val * 1.1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'I: {i}' for i in range(n)], rotation=0) # I: Index
    ax.set_ylabel('Nilai')
    ax.set_title(f"Pencarian Nilai: {target}", fontsize=14)
    
    plt.close(fig) 
    return fig


# --- Visualisasi Utama (TIDAK BERUBAH) ---
if st.button("Mulai Simulasi Linear Search"):
    
    # Asumsi linear_search.py sudah benar dan bebas bug 'Selesai'
    found_index, history = linear_search(list(data_list), target_value)
    max_data_value = max(initial_data) if initial_data else 10 
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        vis_placeholder = st.empty()
        status_placeholder = st.empty() 
    with col2:
        table_placeholder = st.empty()
    
    final_found_index = -1
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        current_array = state['array']
        current_index = state['index']
        status = state['status']
        action = state['action']

        if status == 'Ditemukan':
            final_found_index = current_index 
        
        # --- Tampilkan Grafik (Matplotlib) ---
        fig_mpl = plot_array(
            current_array, 
            state['target'], 
            current_index, 
            final_found_index, 
            max_data_value, 
            status
        )

        with vis_placeholder.container():
            st.pyplot(fig_mpl, clear_figure=True)
        
        # --- TABEL DATA PENDUKUNG ---
        with table_placeholder.container():
             df_table = pd.DataFrame({'Index': range(len(current_array)), 'Nilai': current_array})
             st.markdown("##### Data Array (Index & Nilai)")
             st.dataframe(df_table.T, hide_index=True)

        with status_placeholder.container():
            if status == 'Ditemukan':
                st.success(f"**Langkah ke-{step}** | **Status:** {status}")
            elif status == 'Selesai':
                st.warning(f"**Langkah ke-{step}** | **Status:** {status}")
            else:
                 st.info(f"**Langkah ke-{step+1}** | **Status:** {status}")
            st.caption(action)

        # Jeda untuk simulasi
        time.sleep(speed)

    # --- Hasil Akhir Final ---
    st.markdown("---")
    if final_found_index != -1:
        st.balloons()
        st.success(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** DITEMUKAN pada Indeks **{final_found_index}**.")
    else:
        st.error(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** TIDAK DITEMUKAN dalam array.")
    
    st.info(f"Algoritma Linear Search selesai dalam **{len(history)-1}** langkah pengecekan.")

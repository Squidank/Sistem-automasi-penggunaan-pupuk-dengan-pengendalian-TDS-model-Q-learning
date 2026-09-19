import streamlit as st
import pandas as pd
import numpy as np
import random

# Konfigurasi halaman Streamlit
st.set_page_config(layout="wide")
st.title("Simulasi Sistem pemupukan Cerdas (Q-Learning)")
st.write("Aplikasi ini mensimulasikan rekomendasi pencampuran nutrisi harian untuk tanaman cabai selama 45 hari, berdasarkan model kebijakan optimal yang sudah ada. Model ini diadaptasi untuk mengontrol dua sumber nutrisi (A dan B) secara terpisah.")

# === FUNGSI INTI ===

# Fungsi untuk memuat tabel kebijakan optimal dari file CSV
@st.cache_data
def load_q_tables():
    """Memuat semua file CSV kebijakan optimal ke dalam memori dengan penanganan eror yang lebih baik."""
    tables = {}
    try:
        for goal in [600, 900, 1200]:
            filepath = f"file_uji\Output_iterasi_terbaik_{goal}.csv"  
            df = pd.read_csv(filepath)
            # Konversi kolom 'State' dari string kembali ke tuple
            df["State"] = df["State"].apply(eval)
            # Ubah DataFrame menjadi dictionary untuk pencarian cepat
            tables[goal] = df.set_index("State").to_dict(orient="index")
    except FileNotFoundError as e:
        st.error(f"File tidak ditemukan: {e.filename}. Pastikan file CSV berada di direktori yang sama dengan aplikasi.")
        return None
    except Exception as e:
        st.error("Terjadi eror saat memproses file. Pastikan format file CSV dan isi kolom 'State' (harus berupa tuple dalam bentuk string) sudah benar.")
        st.exception(e)  # Menampilkan detail eror di antarmuka
        return None
    return tables

# Fungsi untuk menghitung TDS hasil dari tiga sumber
def calculate_tds_ab(vol_air, vol_a, vol_b, tds_air, tds_a, tds_b):
    """Menghitung TDS campuran dari air, nutrisi A, dan nutrisi B."""
    total_massa = (vol_air * tds_air) + (vol_a * tds_a) + (vol_b * tds_b)
    total_volume = vol_air + vol_a + vol_b
    return total_massa / total_volume if total_volume > 0 else 0

# Fungsi untuk mencari state terdekat jika state yang tepat tidak ada di tabel
def get_nearest_state(q_table, tds_air, tds_nutrisi_virtual):
    """Mencari state terdekat di Q-table menggunakan Manhattan distance."""
    all_states = list(q_table.keys())
    closest_state = min(
        all_states,
        key=lambda s: abs(s[0] - tds_air) + abs(s[1] - tds_nutrisi_virtual)
    )
    return closest_state

# Fungsi untuk menghitung TDS virtual dari beberapa nutrisi dengan rasio
def calculate_virtual_tds_from_ratios(tds_values, ratio_percent):
    """
    tds_values: list of tds values, e.g. [tds_a, tds_b]
    ratio_percent: list of percents for each (summing to 100), e.g. [60, 40]
    """
    if len(tds_values) != len(ratio_percent):
        raise ValueError("Panjang tds_values dan ratio_percent harus sama.")
    ratios = [rp / 100.0 for rp in ratio_percent]
    return sum([tds_values[i] * ratios[i] for i in range(len(tds_values))])

# Memuat data sekali di awal
Q_TABLES = load_q_tables()

# === UI TABS ===
if Q_TABLES:
    tabs = st.tabs(["**▶️ Simulasi 45 Hari**", "**▶️ Input Manual**"])

    # --- TAB 1: SIMULASI 45 HARI ---
    with tabs[0]:
        st.header("Simulasi Pertumbuhan Tanaman Selama 45 Hari")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            tds_air_init = st.number_input("Inisiasi TDS Air (ppm)", min_value=1, value=350, key="sim_air")
            air_toleransi_min = 1
            air_toleransi_max = tds_air_init
            st.info(f"Rentang TDS Air: {air_toleransi_min} - {air_toleransi_max} ppm")

        with col2:
            tds_nutrisi_a_init = st.number_input("Inisiasi TDS Nutrisi A (ppm)", min_value=1, value=2000, key="sim_nut_a")
            nutrisi_a_min = int(tds_nutrisi_a_init * 0.8)
            nutrisi_a_max = int(tds_nutrisi_a_init * 1.2)
            st.info(f"Rentang TDS Nutrisi A: {nutrisi_a_min} - {nutrisi_a_max} ppm")

        with col3:
            tds_nutrisi_b_init = st.number_input("Inisiasi TDS Nutrisi B (ppm)", min_value=1, value=2000, key="sim_nut_b")
            nutrisi_b_min = int(tds_nutrisi_b_init * 0.8)
            nutrisi_b_max = int(tds_nutrisi_b_init * 1.2)
            st.info(f"Rentang TDS Nutrisi B: {nutrisi_b_min} - {nutrisi_b_max} ppm")

        col1, col2= st.columns(2)
        with col1:
            flow_rate = st.number_input("Flowrate Pompa (ml/s)", min_value=1.0, value=25.0, step=1.0, key="sim_flow")
        with col2:
            ratio_ab = st.slider("Rasio Nutrisi A : B (%)", min_value=0, max_value=100, value=50, step=5, key="ratio_sim")
            # ratio list for two nutrients
            ratio_a_sim = ratio_ab
            ratio_b_sim = 100 - ratio_ab

        if st.button("Jalankan Simulasi 45 Hari", type="primary"):
            results = []
            for day in range(1, 46):
                # Tentukan TDS goal berdasarkan fase pertumbuhan
                if day <= 15:
                    tds_goal = 600
                elif day <= 30:
                    tds_goal = 900
                else:
                    tds_goal = 1200
                
                q_table_current = Q_TABLES[tds_goal]

                # 1. BACA STATE ASLI (Kondisi dinamis harian)
                tds_air = random.randint(air_toleransi_min, air_toleransi_max)
                tds_nutrisi_a = random.randint(nutrisi_a_min, nutrisi_a_max)
                tds_nutrisi_b = random.randint(nutrisi_b_min, nutrisi_b_max)

                # 2. TERJEMAHKAN KE STATE VIRTUAL (untuk model) menggunakan rasio
                tds_nutrisi_virtual = calculate_virtual_tds_from_ratios(
                    [tds_nutrisi_a, tds_nutrisi_b],
                    [ratio_a_sim, ratio_b_sim]
                )

                # 3. CARI AKSI OPTIMAL (menggunakan "Otak")
                state = get_nearest_state(q_table_current, tds_air, tds_nutrisi_virtual)
                raw_action = q_table_current[state]["Action"]
                best_action = eval(raw_action) if isinstance(raw_action, str) else tuple(raw_action)
                volume_air, volume_nutrisi_total = best_action

                # 4. TERJEMAHKAN AKSI KE AKSI FISIK (untuk "Tangan"/Pompa) - pecah berdasarkan rasio
                volume_nutrisi_a = volume_nutrisi_total * (ratio_a_sim / 100.0)
                volume_nutrisi_b = volume_nutrisi_total * (ratio_b_sim / 100.0)
                
                # Hitung waktu pompa dan hasil
                waktu_pompa_air = round(volume_air / flow_rate, 2)
                waktu_pompa_a = round(volume_nutrisi_a / flow_rate, 2)
                waktu_pompa_b = round(volume_nutrisi_b / flow_rate, 2)
                total_volume = volume_air + volume_nutrisi_total
                tds_hasil = calculate_tds_ab(volume_air, volume_nutrisi_a, volume_nutrisi_b, tds_air, tds_nutrisi_a, tds_nutrisi_b)

                results.append({
                    "Hari": day,
                    "TDS Air": tds_air,
                    "TDS Nutrisi A": tds_nutrisi_a,
                    "TDS Nutrisi B": tds_nutrisi_b,
                    "TDS Nutrisi Virtual (dipakai lookup)": round(tds_nutrisi_virtual, 2),
                    "Volume Air (ml)": volume_air,
                    "Volume Nutrisi A (ml)": round(volume_nutrisi_a, 2),
                    "Volume Nutrisi B (ml)": round(volume_nutrisi_b, 2),
                    "Waktu Pompa Air (s)": waktu_pompa_air,
                    "Waktu Pompa A (s)": waktu_pompa_a,
                    "Waktu Pompa B (s)": waktu_pompa_b,
                    "TDS Goal": tds_goal,
                    "TDS Hasil": round(tds_hasil, 2),
                })

            df = pd.DataFrame(results)
            st.success("Simulasi selesai. Berikut hasilnya:")
            st.dataframe(df)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Hasil Simulasi (CSV)", data=csv, file_name="simulasi_hidroponik_45_hari.csv", mime='text/csv')

            # Grafik TDS Hasil vs TDS Goal
            st.subheader("Grafik Performa TDS Hasil vs. TDS Goal Harian")
            chart_df = df[["TDS Hasil", "TDS Goal"]].set_index(pd.Index(range(1, 46), name="Hari"))
            st.line_chart(chart_df)

    # --- TAB 2: INPUT MANUAL ---
    with tabs[1]:
        st.header("Rekomendasi Aksi Berdasarkan Input Manual")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            manual_day = st.number_input("Hari ke-", min_value=1, max_value=45, value=1, key="man_day")
            if manual_day <= 15:
                tds_goal_manual = 600
            elif manual_day <= 30:
                tds_goal_manual = 900
            else:
                tds_goal_manual = 1200
            st.success(f"**TDS Goal** untuk hari ke-{manual_day} adalah **{tds_goal_manual} ppm**")
        
        with col_m2:
            manual_tds_air = st.number_input("TDS Air Aktual (ppm)", min_value=1, value=344, key="man_air")
            manual_tds_a = st.number_input("TDS Nutrisi A Aktual (ppm)", min_value=1, value=1430, key="man_nut_a")
        
        with col_m3:
            manual_tds_b = st.number_input("TDS Nutrisi B Aktual (ppm)", min_value=1, value=1590, key="man_nut_b")
            manual_flow_rate = st.number_input("Flowrate Pompa (ml/s)", min_value=1.0, value=25.0, step=1.0, key="man_flow")

        ratio_ab_manual = st.slider("Rasio Nutrisi A : B (%)", 0, 100, 50, 5, key="ratio_manual")
        ratio_a_manual = ratio_ab_manual
        ratio_b_manual = 100 - ratio_ab_manual

        if st.button("Dapatkan Rekomendasi Aksi", type="primary"):
            q_table_manual = Q_TABLES[tds_goal_manual]
            
            # 1. Terjemahkan input asli ke state virtual menggunakan rasio
            tds_nutrisi_virtual_manual = calculate_virtual_tds_from_ratios(
                [manual_tds_a, manual_tds_b],
                [ratio_a_manual, ratio_b_manual]
            )
            
            # 2. Cari aksi optimal (lookup di CSV)
            state_manual = get_nearest_state(q_table_manual, manual_tds_air, tds_nutrisi_virtual_manual)
            action_manual_raw = q_table_manual[state_manual]["Action"]
            action_manual = eval(action_manual_raw) if isinstance(action_manual_raw, str) else tuple(action_manual_raw)
            vol_air_manual, vol_nutrisi_total_manual = action_manual
            
            # 3. Terjemahkan aksi ke aksi fisik (pecah nutrisi sesuai rasio)
            vol_nutrisi_a_manual = vol_nutrisi_total_manual * (ratio_a_manual / 100.0)
            vol_nutrisi_b_manual = vol_nutrisi_total_manual * (ratio_b_manual / 100.0)

            # Hitung waktu dan hasil
            waktu_air = round(vol_air_manual / manual_flow_rate, 2)
            waktu_a = round(vol_nutrisi_a_manual / manual_flow_rate, 2)
            waktu_b = round(vol_nutrisi_b_manual / manual_flow_rate, 2)
            tds_hasil_manual = calculate_tds_ab(vol_air_manual, vol_nutrisi_a_manual, vol_nutrisi_b_manual, manual_tds_air, manual_tds_a, manual_tds_b)

            
            st.subheader("Didapati Hasil Terjemahan Input State:")
            st.metric(label="State (air, nutrisi)", value=f"({manual_tds_air}, {tds_nutrisi_virtual_manual}) ppm")
            
            st.subheader("Rekomendasi Aksi yang Harus Dilakukan Berdasarkan File Kebijakan Optimal (csv):")
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label="💧 Volume Air", value=f"{vol_air_manual} ml")
                st.metric(label="🅰️ Volume Nutrisi A", value=f"{round(vol_nutrisi_a_manual, 2)} ml")
                st.metric(label="🅱️ Volume Nutrisi B", value=f"{round(vol_nutrisi_b_manual, 2)} ml")

            with res_col2:
                st.metric(label="⏱️ Waktu Pompa Air", value=f"{waktu_air} detik")
                st.metric(label="⏱️ Waktu Pompa A", value=f"{waktu_a} detik")
                st.metric(label="⏱️ Waktu Pompa B", value=f"{waktu_b} detik")
            
            st.metric(label="🎯 TDS Hasil Prediksi", value=f"{round(tds_hasil_manual, 2)} ppm", delta=f"{round(tds_hasil_manual - tds_goal_manual, 2)} ppm dari Goal")
else:
    st.header("Gagal Memuat Data Model")
    st.warning("Aplikasi tidak dapat berjalan karena gagal memuat file kebijakan optimal (CSV). Mohon periksa pesan eror di atas dan pastikan file-file berikut ada di direktori yang sama dan formatnya benar:")
    st.code("- Output_iterasi_terbaik_600.csv\n- Output_iterasi_terbaik_900.csv\n- Output_iterasi_terbaik_1200.csv")

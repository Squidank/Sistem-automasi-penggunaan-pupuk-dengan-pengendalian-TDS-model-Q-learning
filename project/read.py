# test_read.py
import os

def read_file_content(filename):
    print(f"\n--- MENCoba MEMBACA FILE: {filename} ---")
    try:
        with open(filename, 'r') as f:
            print(f"Berhasil membuka {filename}.")
            
            # Baca dan cetak 5 baris pertama
            for i in range(5):
                line = f.readline()
                if not line:
                    print(f"--- AKHIR FILE DI BARIS {i+1} ---")
                    break
                # repr() akan menunjukkan karakter tersembunyi seperti \n atau \r
                print(f"Baris {i+1}: {repr(line)}")
            
    except OSError:
        print(f"GAGAL membuka file {filename}. Periksa nama dan lokasi.")
    print("-" * 20)

# Cek file apa saja yang ada di root direktori
print("File yang terdeteksi di memori:")
print(os.listdir('/'))
print("-" * 20)

# Baca konten dari setiap file q-table
read_file_content('q_table_600.csv')
read_file_content('q_table_900.csv')
read_file_content('q_table_1200.csv')
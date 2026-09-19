from machine import Pin, ADC
import time

# ====== KONFIGURASI ======
TOTAL_HARI = 45
SIMULASI_HARI_DETIK = 5
FLOW_RATE = 50   # ml/s
ADC_RES = 4095

# ====== PIN DEFINISI ======
pot_air = ADC(Pin(1))
pot_a = ADC(Pin(2))
pot_b = ADC(Pin(3))
for pot in [pot_air, pot_a, pot_b]:
    pot.atten(ADC.ATTN_11DB)

relay_air = Pin(10, Pin.OUT)
relay_a = Pin(11, Pin.OUT)
relay_b = Pin(12, Pin.OUT)

# ====== PEMBACAAN POTENSIOMETER ======
def read_adc_avg(pot, samples=5):
    total = 0
    for _ in range(samples):
        total += pot.read()
        time.sleep_ms(10)
    return total / samples

def baca_tds_air(pot):
    val = read_adc_avg(pot)
    return 1 + (val / ADC_RES) * (400 - 1)

def baca_tds_nutrisi(pot):
    val = read_adc_avg(pot)
    return 1400 + (val / ADC_RES) * (2600 - 1400)

# ====== PEMBULATAN STATE ======
def round_tds_air(value):
    """Membulatkan TDS air ke kelipatan 3 terdekat (1,4,7,10,...)"""
    nearest = round((value - 1) / 3) * 3 + 1
    return max(1, min(400, nearest))

def round_tds_nutrisi(value):
    """Membulatkan TDS nutrisi ke kelipatan 10 terdekat (1995→2000, 1994→1990)"""
    sisa = value % 10
    if sisa <= 5:
        return int(value - sisa)
    else:
        return int(value + (10 - sisa))

# ====== PERHITUNGAN ======
def calculate_tds_ab(vol_air, vol_a, vol_b, tds_air, tds_a, tds_b):
    total_mass = vol_air * tds_air + vol_a * tds_a + vol_b * tds_b
    total_vol = vol_air + vol_a + vol_b
    return total_mass / total_vol if total_vol > 0 else 0

def parse_tuple_string(s):
    """Ubah string '(630, 90)' menjadi tuple (630, 90)"""
    try:
        return tuple(map(float, s.strip("() ").split(",")))
    except:
        return None

# ====== BACA Q-TABLE ======
def find_action_for_state(goal, target_state):
    """
    Membuka file CSV dan mencari baris yang cocok dengan target_state.
    Format:
    "(400, 2000)",400,2000,599.53,-1.47,"(630, 90)",720,-0.147297297
    """
    filename = f"/Output_iterasi_terbaik_{goal}.csv"
    search_string = f"\"{target_state}\""  # Contoh: "(400, 2000)"

    try:
        with open(filename, 'r') as f:
            header = f.readline()  # skip header
            for line in f:
                if line.startswith(search_string):
                    # --- parsing yang kuat ---
                    action_start = line.find(',"(')
                    action_end = line.find(')"', action_start)
                    q_start = line.rfind(',')  # nilai terakhir di baris = Q_Value

                    if action_start == -1 or action_end == -1:
                        print("⚠️ Kolom Action tidak dikenali pada baris ini.")
                        return None

                    action_str = line[action_start + 2: action_end + 1]  # contoh: (630, 90)
                    q_value_str = line[q_start + 1:].strip()

                    action = parse_tuple_string(action_str)
                    q_value = float(q_value_str)

                    if action:
                        return {"Action": action, "Q_Value": q_value}
                    else:
                        print("⚠️ Action gagal di-parse.")
                        return None
            print(f"⚠️ State {target_state} tidak ditemukan di file {filename}.")
            return None

    except OSError:
        print(f"⚠️ File tidak ditemukan: {filename}")
        return None

# ====== AKSI RELAY ======
def aksi_pompa(vol_air, vol_a, vol_b):
    waktu_air = vol_air / FLOW_RATE
    waktu_a = vol_a / FLOW_RATE
    waktu_b = vol_b / FLOW_RATE
    print(f"Pompa Air {waktu_air:.2f}s | Pompa A {waktu_a:.2f}s | Pompa B {waktu_b:.2f}s")

    # Nyalakan semua relay
    relay_air.on()
    relay_a.on()
    relay_b.on()

    start = time.ticks_ms()
    while True:
        elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000  # detik

        if elapsed >= waktu_air:
            relay_air.off()
        if elapsed >= waktu_a:
            relay_a.off()
        if elapsed >= waktu_b:
            relay_b.off()

        if elapsed >= max(waktu_air, waktu_a, waktu_b):
            break

        time.sleep(0.05)  # update setiap 50 ms

    print("Semua pompa selesai bekerja.")


# ====== SIMULASI ======
print("=== SIMULASI HIDROPONIK Q-LEARNING (ESP32-S3) ===")

for hari in range(1, TOTAL_HARI + 1):
    print(f"\n=== Hari ke-{hari} ===")

    # Tentukan target TDS berdasarkan fase pertumbuhan
    if hari <= 15:
        goal = 600
    elif hari <= 30:
        goal = 900
    else:
        goal = 1200

    # Baca input dari potensiometer
    tds_air_raw = baca_tds_air(pot_air)
    tds_a_raw = baca_tds_nutrisi(pot_a)
    tds_b_raw = baca_tds_nutrisi(pot_b)
    tds_virtual_raw = (tds_a_raw + tds_b_raw) / 2

    # Bulatkan ke nilai diskrit model
    tds_air = round_tds_air(tds_air_raw)
    tds_virtual = round_tds_nutrisi(tds_virtual_raw)
    state = (tds_air, tds_virtual)
    print(f"TDS Air: {tds_air:.2f} ppm | A: {tds_a_raw:.2f} ppm | B: {tds_b_raw:.2f} ppm | TDS Nutrisi: {tds_virtual_raw:.2f}→{tds_virtual}")

    hasil = find_action_for_state(goal, state)
    if hasil:
        vol_air, vol_total_nutrisi = hasil["Action"]
        vol_a = vol_total_nutrisi / 2
        vol_b = vol_total_nutrisi / 2

        tds_hasil = calculate_tds_ab(vol_air, vol_a, vol_b,
                                     tds_air_raw, tds_a_raw, tds_b_raw)
        print(f"TDS Target: {goal} ppm | Hasil Prediksi: {tds_hasil:.2f} ppm")
        print(f"Aksi: (Air={vol_air}ml, A={vol_a}ml, B={vol_b}ml) | Q={hasil['Q_Value']:.3f}")

        aksi_pompa(vol_air, vol_a, vol_b)
    else:
        print("⚠️ Tidak ada aksi ditemukan untuk state ini.")

    print(f"Tunggu {SIMULASI_HARI_DETIK}s sebelum hari berikutnya...\n")
    time.sleep(SIMULASI_HARI_DETIK)

print("\n=== SIMULASI SELESAI ===")

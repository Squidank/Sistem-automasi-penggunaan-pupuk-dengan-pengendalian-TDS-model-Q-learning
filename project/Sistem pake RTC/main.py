from machine import Pin, ADC, I2C
import time
import ssd1306
from ds1307 import DS1307  # Pastikan file ds1307.py ada

# ====== CONFIG ======
TOTAL_HARI = 45
FLOW_RATE = 20   # ml/s
ADC_RES = 4095

# WAKTU PENYIRAMAN (Format 24 Jam)
TARGET_JAM = 21   # Jam 7 Pagi
TARGET_MENIT = 33  # Lewat 0 menit

# ====== PIN DEFINISI ======
pot_air = ADC(Pin(1))
pot_a = ADC(Pin(2))
pot_b = ADC(Pin(3))
pot_ratio = ADC(Pin(4))

for pot in [pot_air, pot_a, pot_b, pot_ratio]:
    pot.atten(ADC.ATTN_11DB)

# Setup I2C (OLED + RTC DS1307)
# Note: Pastikan DS1307 dan OLED terhubung ke jalur SDA/SCL yang sama
i2c = I2C(0, scl=Pin(41), sda=Pin(42))

# Inisialisasi Perangkat
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
rtc = DS1307(i2c)

relay_air = Pin(10, Pin.OUT)
relay_a = Pin(11, Pin.OUT)
relay_b = Pin(12, Pin.OUT)

# ====== FUNCTION ======
def read_adc_avg(pot, samples=5):
    total = 0
    for _ in range(samples):
        total += pot.read()
        time.sleep_ms(5)
    return total / samples

def baca_tds_air(pot):
    val = read_adc_avg(pot)
    return 1 + (val / ADC_RES) * (400 - 1)

def baca_tds_nutrisi(pot):
    val = read_adc_avg(pot)
    return 1400 + (val / ADC_RES) * (2600 - 1400)

def get_ratio():
    val = read_adc_avg(pot_ratio)
    percent = (val / ADC_RES) * 100
    percent_rounded = round(percent / 5) * 5
    percent_rounded = max(0, min(100, percent_rounded))
    return percent_rounded / 100

def round_tds_air(value):
    nearest = round((value - 1) / 3) * 3 + 1
    return max(1, min(400, nearest))

def round_tds_nutrisi(value):
    sisa = value % 10
    return int(value - sisa) if sisa <= 5 else int(value + (10 - sisa))

def calculate_tds_ab(vol_air, vol_a, vol_b, tds_air, tds_a, tds_b):
    total_mass = vol_air * tds_air + vol_a * tds_a + vol_b * tds_b
    total_vol = vol_air + vol_a + vol_b
    return total_mass / total_vol if total_vol > 0 else 0

def parse_tuple_string(s):
    try:
        return tuple(map(float, s.strip("() ").split(",")))
    except:
        return None

def find_action_for_state(goal, target_state):
    filename = f"/Output_iterasi_terbaik_{goal}.csv"
    search_string = f"\"{target_state}\""

    try:
        with open(filename, 'r') as f:
            f.readline()
            for line in f:
                if line.startswith(search_string):
                    action_start = line.find(',"(')
                    action_end = line.find(')"', action_start)
                    action_str = line[action_start + 2: action_end + 1]
                    action = parse_tuple_string(action_str)
                    if action:
                        return {"Action": action}
            return None
    except OSError:
        # Jangan print error terus menerus agar tidak spam serial
        return None

def aksi_pompa(vol_air, vol_a, vol_b):
    waktu_air = vol_air / FLOW_RATE
    waktu_a = vol_a / FLOW_RATE
    waktu_b = vol_b / FLOW_RATE

    oled.fill(0)
    oled.text("MENYIRAM...", 20, 30)
    oled.show()
    print(f"Vol Air : {vol_air}, Vol Ntrisi A : {vol_a}, Vol Ntrisi B : {vol_b}")
    print(f">> POMPA ON: Air {waktu_air:.1f}s | A {waktu_a:.1f}s | B {waktu_b:.1f}s")

    relay_air.on(); relay_a.on(); relay_b.on()
    start = time.ticks_ms()

    while True:
        elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000
        if elapsed >= waktu_air: relay_air.off()
        if elapsed >= waktu_a: relay_a.off()
        if elapsed >= waktu_b: relay_b.off()
        if elapsed >= max(waktu_air, waktu_a, waktu_b): break
        time.sleep(0.05)

# ===========================
# ======== MAIN LOOP ========
# ===========================

print("=== HIDROPONIK Q-LEARNING REAL-TIME (RTC) ===")

# --- SETUP WAKTU (PENTING!) ---
# Di Wokwi, waktu akan reset setiap restart.
# Di ESP32 Real, uncomment baris di bawah INI HANYA SEKALI untuk set jam, 
# lalu comment lagi dan upload ulang agar jam tidak reset terus saat restart.
# rtc.datetime((2024, 5, 20, 1, 6, 59, 50, 0)) # Format: (Y, M, D, W, H, M, S, SS)

hari_sekarang = 1
flag_sudah_siram = False # Penanda agar tidak menyiram berkali-kali di menit yang sama

while True:
    # 1. Baca Waktu dari RTC
    try:
        dt = rtc.datetime()
        # dt format: (year, month, day, weekday, hour, minute, second, subseconds)
        current_hour = dt[4]
        current_min = dt[5]
        current_sec = dt[6]
    except:
        print("Error membaca RTC")
        time.sleep(1)
        continue

    # 2. Input Sensor (Real-time monitoring)
    tds_air_raw = baca_tds_air(pot_air)
    tds_a_raw = baca_tds_nutrisi(pot_a)
    tds_b_raw = baca_tds_nutrisi(pot_b)
    ratio = get_ratio()
    tds_virtual_raw = (ratio * tds_a_raw) + ((1 - ratio) * tds_b_raw)
    
    # Diskrit data untuk Display & Logic
    tds_air = round_tds_air(tds_air_raw)
    tds_virtual = round_tds_nutrisi(tds_virtual_raw)

    # 3. Tampilkan Status di OLED (Update setiap detik)
    oled.fill(0)
    oled.text(f"Hari: {hari_sekarang}/{TOTAL_HARI}", 0, 0)
    oled.text(f"Jam : {current_hour:02d}:{current_min:02d}:{current_sec:02d}", 0, 10)
    oled.text(f"TDS Air: {int(tds_air)}", 0, 20)
    oled.text(f"Nutrisi A : {int(tds_a_raw)}", 0, 30)
    oled.text(f"Nutrisi B : {int(tds_b_raw)}", 0, 40)
    oled.text(f"A:B = {int(ratio*100)}%:{int((1-ratio)*100)}%", 0, 50)
    if flag_sudah_siram:
        oled.text("STATUS: SUDAH", 0, 60)
    else:
        oled.text("STATUS: MENUNGGU", 0, 60)
    oled.show()

    # 4. LOGIKA PENJADWALAN (CHECKER)
    # Cek apakah jam dan menit sekarang SAMA dengan target
    if current_hour == TARGET_JAM and current_min == TARGET_MENIT:
        
        if not flag_sudah_siram:
            print(f"\nWaktunya Menyiram! Hari ke-{hari_sekarang}")
            
            # Tentukan Goal berdasarkan hari
            if hari_sekarang <= 15: goal = 600
            elif hari_sekarang <= 30: goal = 900
            else: goal = 1200
            
            state = (tds_air, tds_virtual)
            hasil = find_action_for_state(goal, state)

            if hasil:
                vol_air, total_nutrisi = hasil["Action"]
                vol_a = total_nutrisi * ratio
                vol_b = total_nutrisi * (1 - ratio)
                
                print(f"Goal: {goal} | State: {state}")
                aksi_pompa(vol_air, vol_a, vol_b)
                
                tds_mix = calculate_tds_ab(vol_air, vol_a, vol_b, tds_air, tds_a_raw, tds_b_raw)
                print(f"Selesai. TDS Output: {tds_mix:.2f} ppm")
            else:
                print("Tidak ada aksi ditemukan di CSV.")
            
            # Update counter hari & set flag
            if hari_sekarang < TOTAL_HARI:
                hari_sekarang += 1
            else:
                print("Masa Tanam Selesai!")
            
            flag_sudah_siram = True
            
    else:
        # Jika waktu sudah berlalu (misal jam 7:01), reset flag agar besok bisa nyiram lagi
        if flag_sudah_siram:
            flag_sudah_siram = False

    time.sleep(0.5) # Delay agar loop tidak terlalu cepat
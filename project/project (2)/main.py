from machine import Pin, ADC, I2C
import time
import ssd1306

# ====== CONFIG ======
TOTAL_HARI = 45
SIMULASI_HARI_DETIK = 5
FLOW_RATE = 50   # ml/s
ADC_RES = 4095

# ====== PIN DEFINISI ======
pot_air = ADC(Pin(1))
pot_a = ADC(Pin(2))
pot_b = ADC(Pin(3))
pot_ratio = ADC(Pin(4))  # POT BARU UNTUK RASIO

for pot in [pot_air, pot_a, pot_b, pot_ratio]:
    pot.atten(ADC.ATTN_11DB)

i2c = I2C(0, scl=Pin(41), sda=Pin(42))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

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
    """Membaca pot sebagai rasio diskrit kelipatan 5%"""
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
        print(f"⚠️ File {filename} tidak ditemukan.")
        return None

def aksi_pompa(vol_air, vol_a, vol_b):
    waktu_air = vol_air / FLOW_RATE
    waktu_a = vol_a / FLOW_RATE
    waktu_b = vol_b / FLOW_RATE

    print(f"Pompa Air {waktu_air:.2f}s | A {waktu_a:.2f}s | B {waktu_b:.2f}s")

    relay_air.on(); relay_a.on(); relay_b.on()
    start = time.ticks_ms()

    while True:
        elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000

        if elapsed >= waktu_air: relay_air.off()
        if elapsed >= waktu_a: relay_a.off()
        if elapsed >= waktu_b: relay_b.off()

        if elapsed >= max(waktu_air, waktu_a, waktu_b):
            break

        time.sleep(0.05)

# ====== MAIN LOOP ======
print("=== HIDROPONIK Q-LEARNING ESP32 + OLED ===")

for hari in range(1, TOTAL_HARI + 1):
    print(f"\n=== Hari ke-{hari} ===")

    if hari <= 15: goal = 600
    elif hari <= 30: goal = 900
    else: goal = 1200

    # Baca nilai sensor
    tds_air_raw = baca_tds_air(pot_air)
    tds_a_raw = baca_tds_nutrisi(pot_a)
    tds_b_raw = baca_tds_nutrisi(pot_b)
    ratio = get_ratio()

    # Hitung TDS virtual
    tds_virtual_raw = (ratio * tds_a_raw) + ((1 - ratio) * tds_b_raw)

    # Diskrit untuk RL
    tds_air = round_tds_air(tds_air_raw)
    tds_virtual = round_tds_nutrisi(tds_virtual_raw)
    state = (tds_air, tds_virtual)

    # Tampilkan di OLED
    oled.fill(0)
    oled.text(f"A:B = {int(ratio*100)}%:{int((1-ratio)*100)}%", 10, 10)
    oled.text()
    oled.show()

    print(f"TDS Air:{tds_air} | A:{tds_a_raw:.1f} | B:{tds_b_raw:.1f} | Rasio={ratio*100:.0f}%")

    hasil = find_action_for_state(goal, state)

    if hasil:
        vol_air, total_nutrisi = hasil["Action"]
        vol_a = total_nutrisi * ratio
        vol_b = total_nutrisi * (1 - ratio)

        print(f"Action → Air={vol_air}ml, A={vol_a:.1f}ml, B={vol_b:.1f}ml")

        aksi_pompa(vol_air, vol_a, vol_b)

    time.sleep(SIMULASI_HARI_DETIK)

print("\n=== SELESAI ===")

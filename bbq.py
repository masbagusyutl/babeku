import requests
import time
import re
import base64
import hashlib
import random

# Fungsi untuk membaca data dari file data.txt
def read_data(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Fungsi untuk menampilkan hitung mundur waktu 1 jam
def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Countdown: {timeformat}", end='\r')
        time.sleep(1)
        seconds -= 1
    print()

# Fungsi untuk mengekstrak id_user dari parameter user di dalam Use-Agen
def extract_id_user(use_agen):
    match = re.search(r'%22id%22%3A(\d+)', use_agen)
    if match:
        return match.group(1)
    return None

# Fungsi untuk menghasilkan nilai game yang unik setiap kali dipanggil
def generate_game_value(id_user):
    random_value = random.randint(1, 1000000)
    base_string = f"{id_user}-{random_value}-{time.time()}"
    hash_object = hashlib.sha256(base_string.encode())
    hash_digest = hash_object.digest()
    game_value = base64.urlsafe_b64encode(hash_digest).decode('utf-8')
    return game_value

# Fungsi untuk melakukan tugas tap tap
def tap_tap_task(headers, payload, url, max_taps=10):
    for i in range(max_taps):
        # Mengupdate nilai game untuk setiap tap
        payload["game"] = generate_game_value(payload["id_user"])
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            print(f"Tap {i+1} berhasil untuk akun {payload['id_user']} dengan game {payload['game']}")
        else:
            print(f"Tap {i+1} gagal untuk akun {payload['id_user']} dengan game {payload['game']}")
        time.sleep(5)

# Fungsi utama untuk memproses semua akun
def process_accounts(file_path, url, max_taps=10):
    data = read_data(file_path)
    total_accounts = len(data)
    print(f"Jumlah akun: {total_accounts}")

    for index, use_agen in enumerate(data, start=1):
        id_user = extract_id_user(use_agen.strip())
        if id_user:
            headers = {
                "Use-Agen": use_agen.strip(),
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
            }
            payload = {
                "id_user": id_user,
                "mm": 100,
                "game": generate_game_value(id_user)  # Nilai game awal
            }
            print(f"Memproses akun {index} dari {total_accounts}: {payload['id_user']}")
            tap_tap_task(headers, payload, url, max_taps)
        else:
            print(f"ID pengguna tidak ditemukan di Use-Agen untuk akun {index}")

# Main loop
while True:
    process_accounts('data.txt', 'https://bbqbackcs.bbqcoin.ai/api/coin/earnmoney')
    print("Semua akun telah diproses. Memulai hitung mundur 1 jam.")
    countdown_timer(3600)  # Hitung mundur 1 jam (3600 detik)
    print("Memulai ulang proses.")

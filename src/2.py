import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Konstanta simulasi
jumlah_mahasiswa = 100
kapasitas_lift = 10
jumlah_lift = 10
waktu_per_lantai = 5  # detik
waktu_buka_tutup_pintu = 10  # detik
persentase_numpang = 0.3  # 30% mahasiswa numpang
max_lantai = 19  # Lantai tertinggi

# Buat data mahasiswa
np.random.seed(42)  # biar randomnya konsisten
lantai_tujuan = np.random.randint(2, max_lantai + 1, jumlah_mahasiswa)
mahasiswa = [{'id': i, 'lantai_tujuan': lantai_tujuan[i], 'waktu_masuk_lift': None, 'numpang': i < jumlah_mahasiswa * persentase_numpang} for i in range(jumlah_mahasiswa)]

# Antrian mahasiswa di lantai 1
antrian_normal = deque([m for m in mahasiswa if not m['numpang']])
antrian_numpang = deque([m for m in mahasiswa if m['numpang']])

# State lift
lifts = [{'posisi': 1, 'arah': 'turun', 'penumpang': []} for _ in range(jumlah_lift)]

# Waktu berjalan (dalam detik)
waktu = 0
waktu_max = 3600  # maksimal simulasi 1 jam

# Statistik
waktu_tunggu_normal = []
waktu_tunggu_numpang = []
log_antrian_normal = []
log_antrian_numpang = []

# Fungsi bantuan
def waktu_pindah_lantai(lantai_asal, lantai_tujuan):
    return abs(lantai_asal - lantai_tujuan) * waktu_per_lantai

def update_lift(lift, queue_normal, queue_numpang):
    global waktu
    # Jika lift kosong, cari penumpang
    if not lift['penumpang']:
        if lift['arah'] == 'turun' and queue_numpang:
            # Ambil penumpang numpang (mau ikut ke basement)
            for _ in range(min(len(queue_numpang), kapasitas_lift)):
                mahasiswa = queue_numpang.popleft()
                mahasiswa['waktu_masuk_lift'] = waktu
                lift['penumpang'].append(mahasiswa)
            # Bergerak ke basement (lantai 0)
            waktu += waktu_pindah_lantai(lift['posisi'], 0) + waktu_buka_tutup_pintu
            lift['posisi'] = 0
            lift['arah'] = 'naik'
        elif lift['arah'] == 'naik' and queue_normal:
            # Ambil penumpang normal
            for _ in range(min(len(queue_normal), kapasitas_lift)):
                mahasiswa = queue_normal.popleft()
                mahasiswa['waktu_masuk_lift'] = waktu
                lift['penumpang'].append(mahasiswa)
            # Bergerak ke tujuan pertama
            if lift['penumpang']:
                tujuan = min([m['lantai_tujuan'] for m in lift['penumpang']])
                waktu += waktu_pindah_lantai(lift['posisi'], 1) + waktu_buka_tutup_pintu
                lift['posisi'] = 1
                waktu += waktu_pindah_lantai(1, tujuan) + waktu_buka_tutup_pintu
                lift['posisi'] = tujuan
        else:
            # Tidak ada antrian, tetap di posisi
            waktu += 5

    else:
        # Turunkan penumpang sesuai tujuan
        tujuan = min([m['lantai_tujuan'] for m in lift['penumpang']])
        waktu += waktu_pindah_lantai(lift['posisi'], tujuan) + waktu_buka_tutup_pintu
        lift['posisi'] = tujuan
        lift['penumpang'] = [m for m in lift['penumpang'] if m['lantai_tujuan'] != tujuan]

# Simulasi utama
while waktu < waktu_max and (antrian_normal or antrian_numpang):
    for lift in lifts:
        update_lift(lift, antrian_normal, antrian_numpang)
    log_antrian_normal.append(len(antrian_normal))
    log_antrian_numpang.append(len(antrian_numpang))
    waktu += 10  # maju waktu 10 detik

# Rekap hasil
for m in mahasiswa:
    if m['waktu_masuk_lift'] is not None:
        tunggu = m['waktu_masuk_lift']
        if m['numpang']:
            waktu_tunggu_numpang.append(tunggu)
        else:
            waktu_tunggu_normal.append(tunggu)

# Grafik hasil
plt.figure(figsize=(10,5))
plt.plot(np.arange(len(log_antrian_normal))*10, log_antrian_normal, label='Antrian Normal')
plt.plot(np.arange(len(log_antrian_numpang))*10, log_antrian_numpang, label='Antrian Numpang')
plt.xlabel('Waktu (detik)')
plt.ylabel('Jumlah Mahasiswa')
plt.title('Antrian Mahasiswa Seiring Waktu')
plt.legend()
plt.grid()
plt.show()

# Grafik perbandingan rata-rata waktu tunggu
labels = ['Numpang', 'Menunggu']
waktu_rata_rata = [np.mean(waktu_tunggu_numpang), np.mean(waktu_tunggu_normal)]

plt.bar(labels, waktu_rata_rata, color=['blue', 'green'])
plt.ylabel('Waktu Tunggu Rata-rata (detik)')
plt.title('Perbandingan Waktu Tunggu Mahasiswa')
plt.show()

# Print hasil rekap
print(f"Rata-rata waktu tunggu mahasiswa numpang: {np.mean(waktu_tunggu_numpang):.2f} detik")
print(f"Rata-rata waktu tunggu mahasiswa menunggu: {np.mean(waktu_tunggu_normal):.2f} detik")

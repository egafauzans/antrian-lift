import matplotlib.pyplot as plt
import numpy as np

# Asumsi dasar
jumlah_mahasiswa = 100
kapasitas_lift = 10
jumlah_lift = 10
waktu_per_lantai = 5  # detik untuk naik/turun 1 lantai
waktu_buka_tutup_pintu = 10  # detik waktu buka-tutup lift
persentase_numpang = 0.3  # 30% mahasiswa ikut numpang

# Set tujuan mahasiswa
np.random.seed(42)
lantai_tujuan = np.random.randint(2, 20, jumlah_mahasiswa)  # random lantai 2-19

# Fungsi hitung waktu perjalanan
def hitung_waktu_naik(lantai_tujuan):
    # Waktu dari lantai 1 langsung ke tujuan
    return (lantai_tujuan - 1) * waktu_per_lantai + waktu_buka_tutup_pintu

def hitung_waktu_numpang(lantai_tujuan):
    # Waktu: turun ke basement -> naik ke lantai 1 -> naik ke lantai tujuan
    waktu_ke_basement = waktu_per_lantai + waktu_buka_tutup_pintu
    waktu_naik_ke_1 = waktu_per_lantai + waktu_buka_tutup_pintu
    waktu_naik_ke_tujuan = (lantai_tujuan - 1) * waktu_per_lantai + waktu_buka_tutup_pintu
    return waktu_ke_basement + waktu_naik_ke_1 + waktu_naik_ke_tujuan

# Bagi mahasiswa menjadi 2 kelompok
jumlah_numpang = int(jumlah_mahasiswa * persentase_numpang)
jumlah_menunggu = jumlah_mahasiswa - jumlah_numpang

# Hitung waktu perjalanan
waktu_numpang = [hitung_waktu_numpang(x) for x in lantai_tujuan[:jumlah_numpang]]
waktu_menunggu = [hitung_waktu_naik(x) for x in lantai_tujuan[jumlah_numpang:]]

# Statistik hasil
rata_rata_waktu_numpang = np.mean(waktu_numpang)
rata_rata_waktu_menunggu = np.mean(waktu_menunggu)

print(f"Rata-rata waktu tempuh mahasiswa numpang: {rata_rata_waktu_numpang:.2f} detik")
print(f"Rata-rata waktu tempuh mahasiswa menunggu: {rata_rata_waktu_menunggu:.2f} detik")

# Plot grafik
labels = ['Numpang', 'Menunggu']
waktu = [rata_rata_waktu_numpang, rata_rata_waktu_menunggu]

plt.bar(labels, waktu, color=['blue', 'green'])
plt.ylabel('Waktu Tempuh Rata-rata (detik)')
plt.title('Perbandingan Waktu Tempuh Mahasiswa')
plt.grid(axis='y')
plt.show()

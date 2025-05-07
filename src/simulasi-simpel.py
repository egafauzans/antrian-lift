import matplotlib.pyplot as plt
import numpy as np

# Asumsi dasar
jumlah_mahasiswa = 100
kapasitas_lift = 10
jumlah_lift = 10
waktu_per_lantai = 5  # detik
waktu_buka_tutup_pintu = 10  # detik
persentase_numpang = 0.3  # 30% numpang
lantai_tujuan = np.random.randint(2, 20, jumlah_mahasiswa)  # lantai tujuan acak

# Simulasi waktu tempuh
def hitung_waktu_naik(lantai_tujuan):
    return (lantai_tujuan - 1) * waktu_per_lantai + waktu_buka_tutup_pintu

def hitung_waktu_numpang(lantai_tujuan):
    waktu_ke_basement = 1 * waktu_per_lantai + waktu_buka_tutup_pintu  # turun 1 lantai ke basement
    waktu_naik_ke_1 = 1 * waktu_per_lantai + waktu_buka_tutup_pintu
    waktu_ke_tujuan = (lantai_tujuan - 1) * waktu_per_lantai + waktu_buka_tutup_pintu
    return waktu_ke_basement + waktu_naik_ke_1 + waktu_ke_tujuan

# Bagi mahasiswa
jumlah_numpang = int(jumlah_mahasiswa * persentase_numpang)
jumlah_menunggu = jumlah_mahasiswa - jumlah_numpang

# Waktu rata-rata
waktu_numpang = [hitung_waktu_numpang(x) for x in lantai_tujuan[:jumlah_numpang]]
waktu_menunggu = [hitung_waktu_naik(x) for x in lantai_tujuan[jumlah_numpang:]]

# Statistik
rata_rata_waktu_numpang = np.mean(waktu_numpang)
rata_rata_waktu_menunggu = np.mean(waktu_menunggu)

print(f"Rata-rata waktu tempuh mahasiswa numpang: {rata_rata_waktu_numpang:.2f} detik")
print(f"Rata-rata waktu tempuh mahasiswa menunggu: {rata_rata_waktu_menunggu:.2f} detik")

# Plot
labels = ['Numpang', 'Menunggu']
waktu = [rata_rata_waktu_numpang, rata_rata_waktu_menunggu]

plt.bar(labels, waktu, color=['blue', 'green'])
plt.ylabel('Waktu Tempuh Rata-rata (detik)')
plt.title('Perbandingan Waktu Tempuh Mahasiswa')
plt.show()

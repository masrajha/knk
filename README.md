# **LAPORAN HASIL EKSPERIMEN KOMPLEKSITAS ALGORITMA**

## **SOAL 1: EKSPERIMEN KOMPLEKSITAS ALGORITMA O(log n), O(n), DAN O(n log n)**

### **Eksperimen 1: Fungsi Rekursif O(log n)**

#### **1. Pendahuluan**
Eksperimen ini bertujuan untuk menganalisis perilaku waktu eksekusi fungsi rekursif dengan kompleksitas O(log n). Fungsi `func1(n)` yang digunakan merupakan implementasi rekursif yang membagi masalah menjadi dua bagian setiap iterasi, menghasilkan kompleksitas logaritmik. Eksperimen ini penting untuk memahami bagaimana algoritma dengan kompleksitas logaritmik merespons peningkatan ukuran input.

#### **2. Skenario Eksperimen**
- **Kode Program**: [Tugas_1.ipynb](Tugas_1.ipynb)
- **Fungsi yang diuji**: `func1(n)` - fungsi rekursif yang membagi n menjadi setengah setiap panggilan
- **Rentang nilai n**: n = 2^k untuk k = 1 sampai 10 (n = 2 sampai 1024)
- **Jumlah pengulangan**: 5 kali untuk setiap nilai n
- **Metode pengukuran**: Waktu eksekusi diukur dalam mikrodetik (µs)
- **Parameter analisis**:
  - Rata-rata waktu eksekusi
  - Standar deviasi
  - Analisis regresi linear
  - Perbandingan dengan model teoritis

#### **3. Hasil**
**Tabel Hasil Pengukuran:**

| k | n = 2^k | Waktu Rata-rata (µs) | Std Dev |
|---|---------|---------------------|---------|
| 1 | 2       | 0.62                | 0.60    |
| 2 | 4       | 0.46                | 0.17    |
| 3 | 8       | 0.60                | 0.15    |
| 4 | 16      | 0.66                | 0.08    |
| 5 | 32      | 0.78                | 0.04    |
| 6 | 64      | 0.92                | 0.04    |
| 7 | 128     | 1.00                | 0.06    |
| 8 | 256     | 1.20                | 0.06    |
| 9 | 512     | 1.32                | 0.04    |
| 10| 1024    | 1.70                | 0.60    |

**Analisis Statistik:**
- Persamaan regresi linear: **waktu = 0.1206 × k + 0.2627**
- Koefisien determinasi (R²): **0.892849**
- P-value: **0.000038** (signifikan secara statistik)

**Visualisasi:**
![Grafik Eksperimen 1](eksperimen1_hasil.png)

*Gambar 1: Grafik hasil Eksperimen 1 menunjukkan hubungan antara ukuran input (n) dengan waktu eksekusi*

#### **4. Kesimpulan**
1. Fungsi rekursif dengan kompleksitas O(log n) menunjukkan pertumbuhan waktu yang sangat lambat terhadap peningkatan ukuran input.
2. Hasil eksperimen **SESUAI** dengan teori O(log n), dengan koefisien determinasi R² = 0.8928 yang menunjukkan kesesuaian yang baik.
3. Waktu eksekusi meningkat dari 0.62 µs untuk n=2 menjadi hanya 1.70 µs untuk n=1024, menunjukkan efisiensi algoritma logaritmik.
4. Error relatif antara hasil eksperimen dan prediksi teori bervariasi antara 2.09% hingga 61.77%, dengan rata-rata sekitar 13.2%.

---

### **Eksperimen 2: Perbandingan O(n) vs O(n log n)**

#### **1. Pendahuluan**
Eksperimen ini bertujuan untuk membandingkan performa algoritma dengan kompleksitas O(n) dan O(n log n). Fungsi `func2(n)` mewakili algoritma linear sederhana, sedangkan `func3(n)` mewakili algoritma dengan nested loop yang menghasilkan kompleksitas n log n. Eksperimen ini penting untuk memahami dampak faktor logaritmik tambahan pada waktu eksekusi.

#### **2. Skenario Eksperimen**
- **Fungsi yang diuji**:
  - `func2(n)`: Kompleksitas O(n) - loop tunggal
  - `func3(n)`: Kompleksitas O(n log n) - nested loop dengan pembagian berulang
- **Rentang nilai n**: n = 10^k untuk k = 1 sampai 5 (n = 10 sampai 100,000)
- **Jumlah pengulangan**: 5 kali untuk setiap nilai n
- **Analisis perbandingan**:
  - Waktu eksekusi absolut
  - Rasio waktu O(n log n) / O(n)
  - Perbandingan dengan teori rasio log n

#### **3. Hasil**
**Tabel Hasil Pengukuran:**

| k | n       | O(n) (µs) | Std Dev | O(n log n) (µs) | Std Dev | Rasio | Teori Rasio |
|---|---------|-----------|---------|-----------------|---------|-------|-------------|
| 1 | 10      | 1.50      | 0.66    | 3.86            | 0.58    | 2.57  | 1.00        |
| 2 | 100     | 3.68      | 1.15    | 48.44           | 19.85   | 13.16 | 2.00        |
| 3 | 1,000   | 30.78     | 0.82    | 587.58          | 132.18  | 19.09 | 3.00        |
| 4 | 10,000  | 378.48    | 73.13   | 8,531.64        | 755.56  | 22.54 | 4.00        |
| 5 | 100,000 | 3,717.62  | 474.45  | 103,641.02      | 4,097.13| 27.88 | 5.00        |

**Analisis Statistik:**
- **O(n)**: Regresi: waktu = 0.037180 × n + 0.20, R² = 0.999992
- **O(n log n)**: Regresi: waktu = 0.207210 × (n log n) + 50.77, R² = 0.999994
- **Korelasi rasio**: Pearson = 0.9780, P-value = 0.003910

**Observasi Penting:**
1. Waktu O(n) tumbuh linear: dari 1.50 µs (n=10) ke 3,717.62 µs (n=100,000)
2. Waktu O(n log n) tumbuh lebih cepat: dari 3.86 µs ke 103,641.02 µs
3. Rasio eksperimen jauh lebih tinggi dari teori karena faktor konstanta yang berbeda

**Visualisasi:**
![Grafik Eksperimen 2](eksperimen2_hasil.png)

*Gambar 2: Grafik hasil Eksperimen 2 menunjukkan perbandingan waktu eksekusi antara O(n) dan O(n log n)*

#### **4. Kesimpulan**
1. Hasil eksperimen **SANGAT SESUAI** dengan teori untuk kedua kompleksitas (R² > 0.9999).
2. Algoritma O(n) lebih efisien untuk semua ukuran n yang diuji.
3. Rasio O(n log n)/O(n) dalam eksperimen jauh lebih tinggi dari prediksi teoritis log n, menunjukkan bahwa faktor konstanta memiliki pengaruh signifikan.
4. Untuk n=100,000, algoritma O(n log n) membutuhkan waktu 27.88 kali lebih lama daripada O(n), padahal teori memprediksi hanya 5 kali.

---

## **SOAL 2: EKSPERIMEN KODE PROGRAM REKURSIF DENGAN KOMPLEKSITAS O(n), O(n log n), DAN O(n²)**

### **Eksperimen 3: Algoritma Maximum Subarray Sum**

#### **1. Pendahuluan**
Eksperimen ini menganalisis tiga algoritma rekursif untuk menyelesaikan masalah Maximum Subarray Sum dengan kompleksitas berbeda: O(n) (Kadane rekursif), O(n log n) (Divide and Conquer), dan O(n²) (Brute Force rekursif). Tujuan eksperimen adalah memahami bagaimana perbedaan kompleksitas algoritma mempengaruhi waktu eksekusi untuk masalah yang sama. Eksperimen dilakukan dengan berbagai ukuran array dari n=10 hingga n=1000 untuk melihat pola pertumbuhan waktu eksekusi.

#### **2. Skenario Eksperimen**
- **Algoritma yang diuji**:
  1. `maxSubSum1`: Kadane rekursif - O(n)
  2. `maxSubSum2`: Divide and Conquer - O(n log n)
  3. `maxSubSum3`: Brute Force rekursif - O(n²)
- **Rentang ukuran array**: n = 10^k untuk k = 1.0 sampai 3.0 (n = 10 sampai 1000)
- **Jumlah pengulangan**: 7 kali dengan penghapusan outlier menggunakan metode IQR
- **Karakteristik data**: Array integer acak dengan nilai -20 sampai 20, seed tetap (42) untuk konsistensi
- **Metode analisis**:
  - Regresi linear untuk setiap kompleksitas terhadap bentuk teoritisnya
  - Analisis Mean Absolute Error (MAE) dan Mean Absolute Percentage Error (MAPE)
  - Analisis pertumbuhan rasio antar algoritma
  - Uji hipotesis pertumbuhan antara nilai aktual dan teoritis

#### **3. Hasil**
**Tabel Hasil Pengukuran (Ringkasan):**

| k   | n    | O(n) (µs) | Std Dev | O(n log n) (µs) | Std Dev | O(n²) (µs) | Std Dev | Rasio n²/n |
|-----|------|-----------|---------|-----------------|---------|------------|---------|------------|
| 1.0 | 10   | 4.85      | 0.58    | 11.04           | 0.93    | 15.09      | 0.82    | 3.11       |
| 1.2 | 16   | 6.39      | 0.18    | 16.01           | 0.72    | 23.17      | 1.55    | 3.62       |
| 1.4 | 25   | 9.54      | 0.12    | 26.16           | 0.89    | 52.30      | 9.34    | 5.48       |
| 1.6 | 40   | 14.91     | 0.11    | 44.73           | 1.46    | 112.19     | 2.87    | 7.53       |
| 1.8 | 63   | 23.55     | 0.07    | 72.79           | 1.88    | 313.83     | 36.21   | 13.33      |
| 2.0 | 100  | 45.76     | 0.25    | 122.55          | 4.06    | 1423.30    | 47.65   | 31.11      |
| 2.2 | 158  | 72.83     | 2.58    | 199.33          | 7.18    | 2572.95    | 42.19   | 35.33      |
| 2.4 | 251  | 118.81    | 1.93    | 331.99          | 20.09   | 7251.07    | 149.88  | 61.03      |
| 2.6 | 398  | 207.18    | 6.25    | 611.46          | 59.24   | 21269.74   | 578.90  | 102.67     |
| 2.8 | 631  | 453.28    | 104.33  | 1020.00         | 48.75   | 53301.68   | 1603.28 | 117.59     |
| 3.0 | 1000 | 595.89    | 20.38   | 1652.01         | 64.79   | 130034.38  | 5599.55 | 218.22     |

**Analisis Statistik:**
- **O(n)**: waktu = 0.6312 × n - 13.30, R² = 0.9821, MAE = 18.13 µs, MAPE = 53.08%
- **O(n log n)**: waktu = 0.1670 × (n log n) + 10.65, R² = 0.9992, MAE = 10.30 µs, MAPE = 10.40%
- **O(n²)**: waktu = 0.130656 × n² - 59.97, R² = 0.9998, MAE = 416.74 µs, MAPE = 74.39%

**Analisis Pertumbuhan Rasio:**
- **Rasio O(n log n)/O(n)**: Relatif stabil antara 2.25-3.09, menunjukkan bahwa O(n log n) sekitar 2-3 kali lebih lambat dari O(n) untuk rentang n yang diuji
- **Rasio O(n²)/O(n)**: Meningkat drastis dari 3.11 (n=10) menjadi 218.22 (n=1000), mengkonfirmasi pertumbuhan kuadratik
- **Error Pertumbuhan Rata-rata**: O(n)=11.56%, O(n log n)=7.84%, O(n²)=21.56%

**Visualisasi:**
![Grafik Eksperimen 3](eksperimen3_analisis_teori.png)

*Gambar 3: Grafik hasil Eksperimen 3 menunjukkan perbandingan tiga algoritma dengan kompleksitas berbeda*

#### **4. Kesimpulan**

**Kesesuaian dengan Teori:**
1. **O(n) - Kadane rekursif**: **CUKUP SESUAI** dengan teori (R²=0.982, MAPE=53.1%, Growth Error=11.6%)
   - Waktu eksekusi menunjukkan tren linear yang jelas
   - MAPE yang tinggi (53.1%) disebabkan oleh variabilitas pengukuran untuk n kecil
   - Error pertumbuhan hanya 11.6%, menunjukkan kesesuaian pola pertumbuhan

2. **O(n log n) - Divide and Conquer**: **SANGAT SESUAI** dengan teori (R²=0.999, MAPE=10.4%, Growth Error=7.8%)
   - Kesesuaian sangat baik dengan model teoritis
   - MAPE rendah (10.4%) menunjukkan prediksi yang akurat
   - Error pertumbuhan hanya 7.8%, mengkonfirmasi pola n log n

3. **O(n²) - Brute Force rekursif**: **CUKUP SESUAI** dengan teori (R²=1.000, MAPE=74.4%, Growth Error=21.6%)
   - R² sangat tinggi menunjukkan pola kuadratik yang jelas
   - MAPE tinggi (74.4%) disebabkan oleh variabilitas besar untuk n besar
   - Error pertumbuhan 21.6% masih dalam batas wajar untuk algoritma dengan kompleksitas tinggi

**Analisis Performa Komparatif:**
1. **Skalabilitas**: Algoritma O(n) menunjukkan skalabilitas terbaik, diikuti O(n log n), sedangkan O(n²) menjadi tidak praktis untuk n > 100
2. **Rasio Waktu**: Untuk n=1000, O(n²) 218× lebih lambat dari O(n) dan 79× lebih lambat dari O(n log n)
3. **Stabilitas**: Algoritma O(n) dan O(n log n) menunjukkan stabilitas pengukuran yang baik (std dev relatif kecil), sedangkan O(n²) memiliki variabilitas tinggi
4. **Break Point**: Perbedaan waktu menjadi signifikan pada n ≈ 100, di mana O(n²) mulai tidak praktis

**Rekomendasi Praktis:**
1. **Untuk n kecil (≤100)**: Ketiga algoritma dapat digunakan, tetapi O(n) tetap paling efisien
2. **Untuk n menengah (100-1000)**: Prioritaskan O(n) atau O(n log n), hindari O(n²)
3. **Untuk n besar (>1000)**: Hanya O(n) yang praktis, O(n log n) masih dapat dipertimbangkan dengan hardware memadai
4. **Trade-off**: Divide and Conquer (O(n log n)) menawarkan kompromi antara kompleksitas implementasi dan performa untuk masalah yang cocok dengan paradigma divide-and-conquer

**Implikasi Teoritis:**
1. **Validasi Model**: Hasil eksperimen memvalidasi model kompleksitas Big-O dalam memprediksi pertumbuhan waktu eksekusi
2. **Pentingnya Faktor Konstanta**: Perbedaan faktor konstanta menyebabkan rasio aktual berbeda dari prediksi teoritis murni
3. **Limitasi Pengukuran**: Untuk algoritma sangat cepat (O(n) untuk n kecil), noise pengukuran dapat signifikan

**Kesimpulan Akhir:**
Eksperimen berhasil mendemonstrasikan perbedaan dramatis dalam waktu eksekusi antara tiga kelas kompleksitas algoritma. Hasil menunjukkan bahwa pemilihan algoritma yang tepat berdasarkan kompleksitas waktu memiliki dampak kritis pada performa aplikasi, terutama untuk dataset besar. Algoritma O(n) (Kadane rekursif) terbukti sebagai pilihan optimal untuk masalah Maximum Subarray Sum dalam semua skenario yang diuji.

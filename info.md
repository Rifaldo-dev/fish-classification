# Info Proyek — FishID: Sistem Klasifikasi Ikan

---

## Tentang Proyek

FishID adalah sistem identifikasi ikan berbasis kecerdasan buatan yang mampu mengenali jenis ikan dari foto secara otomatis. Sistem ini dibangun menggunakan model YOLOv8 untuk klasifikasi gambar, dilengkapi dengan dashboard web berbasis Flask untuk memudahkan penggunaan.

---

## Tujuan

- Membangun model machine learning yang dapat mengklasifikasikan jenis ikan dari gambar
- Menyediakan antarmuka web yang mudah digunakan untuk melakukan identifikasi ikan
- Menyimpan riwayat identifikasi dan informasi harga ikan ke dalam database
- Sebagai referensi implementasi YOLOv8 untuk klasifikasi gambar dengan dataset kecil

---

## Manfaat

- **Nelayan & pedagang ikan** - membantu identifikasi jenis ikan dengan cepat tanpa harus ahli
- **Edukasi** - media pembelajaran mengenal jenis-jenis ikan air laut dan air tawar
- **Referensi harga** - sistem menyimpan harga pasar per kg untuk setiap jenis ikan
- **Dokumentasi** - riwayat identifikasi tersimpan di database untuk keperluan pencatatan

---

## Dataset

Dataset terdiri dari **7 kelas ikan** yang dibagi dalam 2 kategori:

| Kategori | Nama Ikan | Jumlah Gambar |
|----------|-----------|---------------|
| Laut | Kakap | 22 |
| Laut | Kuwe | 17 |
| Laut | Lema | 20 |
| Air Tawar | Arwana | 100 |
| Air Tawar | Cupang | 100 |
| Air Tawar | Koi | 100 |
| Air Tawar | Maskoki | 100 |
| **Total** | | **459 gambar** |

Gambar dikompres dan di-resize ke ukuran **224x224 px** untuk efisiensi training.

Split dataset: **70% train / 20% validasi / 10% test**

---

## Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Model AI | YOLOv8n-cls (Ultralytics 8.4.12) |
| Backend | Python 3.x, Flask 3.0 |
| Database | MySQL (via PyMySQL) |
| Frontend | Bootstrap 5, Font Awesome 6 |
| Image Processing | Pillow |
| Autentikasi | Flask Session |

---

## Hasil Training

| Metrik | Nilai |
|--------|-------|
| Arsitektur | YOLOv8n-cls |
| Epochs | 50 |
| Image Size | 224 x 224 px |
| Batch Size | 16 |
| Top-1 Accuracy (val) | 93.4% |
| Top-1 Accuracy (test) | 100% |
| Total Parameter | 1.447.255 |

---

## Cara Kerja

### 1. Preprocessing
Gambar dari folder `dataset/` displit secara acak ke dalam 3 folder:
- `data/train/` — untuk melatih model
- `data/val/` — untuk validasi saat training
- `data/test/` — untuk evaluasi akhir

### 2. Training
Model YOLOv8n-cls (pretrained) di-fine-tune menggunakan dataset ikan. YOLOv8 menggunakan arsitektur CNN dengan transfer learning — bobot dari ImageNet digunakan sebagai titik awal, lalu disesuaikan dengan data ikan.

```
Input Gambar (224x224)
       ↓
  YOLOv8n-cls
  (CNN Backbone + Classify Head)
       ↓
  Probabilitas per kelas
       ↓
  Kelas dengan prob tertinggi = Hasil
```

### 3. Inferensi (Prediksi)
Saat pengguna upload gambar di dashboard:

```
User upload gambar
       ↓
Flask menyimpan gambar ke folder uploads/
       ↓
Model YOLO memproses gambar
       ↓
Menghasilkan Top-3 prediksi + confidence
       ↓
Flask query harga ke MySQL
       ↓
Hasil ditampilkan di dashboard
       ↓
Riwayat disimpan ke tabel riwayat_identifikasi
```

### 4. Dashboard
Dashboard terdiri dari 4 halaman:

- **Dashboard** — statistik dataset, daftar kelas, dan info model
- **Identifikasi** — upload gambar dan lihat hasil prediksi beserta harga ikan
- **Riwayat** — histori semua identifikasi yang pernah dilakukan
- **Harga Ikan** — daftar harga per kg, dapat diedit langsung

---

## Struktur Database

### Tabel `harga_ikan`
Menyimpan harga pasaran ikan per kg.

| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INT | Primary key |
| nama_ikan | VARCHAR(50) | Nama ikan |
| jenis | ENUM | laut / tawar |
| harga_per_kg | DECIMAL | Harga dalam rupiah |
| updated_at | TIMESTAMP | Waktu update terakhir |

### Tabel `riwayat_identifikasi`
Menyimpan log setiap kali identifikasi dilakukan.

| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INT | Primary key |
| nama_ikan | VARCHAR(50) | Hasil prediksi |
| jenis_ikan | VARCHAR(30) | Laut / Air Tawar |
| confidence | DECIMAL | Tingkat keyakinan (%) |
| image_path | VARCHAR(255) | Nama file gambar |
| created_at | TIMESTAMP | Waktu identifikasi |

### Tabel `users`
Menyimpan data pengguna untuk autentikasi login.

| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INT | Primary key |
| username | VARCHAR(50) | Username unik |
| password | VARCHAR(255) | Password (SHA-256) |

---

## Keterbatasan

- Dataset masih kecil (459 gambar, 7 kelas) — akurasi bisa meningkat dengan lebih banyak data
- Model belum dioptimasi untuk inferensi real-time di perangkat mobile
- Belum mendukung deteksi multi-ikan dalam satu gambar (klasifikasi, bukan deteksi objek)
- Harga ikan diinput manual, belum terintegrasi dengan sumber data harga real-time

---

## Pengembangan Selanjutnya

- [ ] Tambah lebih banyak kelas ikan
- [ ] Export model ke TFLite / ONNX untuk deployment mobile
- [ ] Integrasi kamera langsung (real-time detection)
- [ ] API endpoint untuk integrasi aplikasi lain
- [ ] Grafik statistik riwayat identifikasi di dashboard

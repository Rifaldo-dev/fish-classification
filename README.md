# Klasifikasi Ikan

Sistem klasifikasi ikan berbasis YOLOv8 dengan dashboard Flask.

## Progress

- [x] Pengumpulan dataset - kumpul gambar, rename, kompres 224x224
- [x] Pengelompokan dataset - klasifikasi laut & tawar, struktur folder
- [x] Preprocessing - split train/val/test (70/20/10), augmentasi, normalisasi
- [x] Training YOLOv8 - train model klasifikasi, monitoring, simpan model (top1_acc: 93.4%, 50 epochs)
- [x] Evaluasi - confusion matrix, classification report (test accuracy: 100%, 48 gambar)
- [x] Dashboard - Flask, upload gambar, tampilkan hasil klasifikasi & top 3 prediksi

---

## Struktur Proyek

```
mlIkan/
├── dataset/
│   ├── laut/
│   │   ├── kakap/
│   │   ├── kuwe/
│   │   └── lema/
│   └── tawar/
│       ├── arwana/
│       ├── cupang/
│       ├── koi/
│       └── maskoki/
│
├── data/                     # hasil split (train/val/test) - di-generate otomatis
│
├── model/
│   ├── preprocess.py         # split dataset
│   ├── train.py              # training YOLOv8
│   ├── evaluate.py           # evaluasi model
│   └── runs/                 # hasil training (weights, metrics) - tidak di-commit
│
├── dashboard/
│   ├── app.py                # Flask app
│   ├── .env                  # konfigurasi database (tidak di-commit)
│   ├── .env.example          # template konfigurasi
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── identifikasi.html
│   │   ├── riwayat.html
│   │   └── harga.html
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/icon.png
│   └── uploads/              # gambar upload user - tidak di-commit
│
├── compress.py               # script kompresi gambar
├── requirements.txt
└── README.md
```

---

## Setup & Instalasi

### 1. Clone repo

```bash
git clone https://github.com/Rifaldo-dev/fish-classification.git
cd fish-classification
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Konfigurasi database

```bash
cp dashboard/.env.example dashboard/.env
```

Edit `dashboard/.env` sesuai konfigurasi MySQL lokal:

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=fishid_db
```

### 4. Setup database MySQL

Jalankan query berikut di MySQL:

```sql
CREATE DATABASE IF NOT EXISTS fishid_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fishid_db;

CREATE TABLE harga_ikan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama_ikan VARCHAR(50) NOT NULL,
  jenis ENUM('laut','tawar') NOT NULL,
  harga_per_kg DECIMAL(12,2) NOT NULL,
  satuan VARCHAR(20) DEFAULT 'kg',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE riwayat_identifikasi (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama_ikan VARCHAR(50) NOT NULL,
  jenis_ikan VARCHAR(30) NOT NULL,
  confidence DECIMAL(5,2) NOT NULL,
  image_path VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password) VALUES ('admin', SHA2('admin123', 256));

INSERT INTO harga_ikan (nama_ikan, jenis, harga_per_kg) VALUES
  ('kakap', 'laut', 85000), ('kuwe', 'laut', 75000), ('lema', 'laut', 45000),
  ('arwana', 'tawar', 500000), ('cupang', 'tawar', 25000),
  ('koi', 'tawar', 150000), ('maskoki', 'tawar', 35000);
```

### 5. Training model (opsional, skip jika sudah punya weights)

```bash
python model/preprocess.py   # split dataset
python model/train.py        # training YOLOv8
```

Update path model di `dashboard/app.py`:

```python
MODEL_PATH = "path/to/your/best.pt"
```

### 6. Jalankan dashboard

```bash
python dashboard/app.py
```

Buka `http://127.0.0.1:5000` — login dengan `admin` / `admin123`.

---

## Tech Stack

- Python 3.x
- YOLOv8 (Ultralytics)
- Flask
- MySQL + PyMySQL
- Bootstrap 5
- Font Awesome 6

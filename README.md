# Klasifikasi Ikan

## Progress

- [x] Pengumpulan dataset - kumpul gambar, rename, kompres 224x224
- [x] Pengelompokan dataset - klasifikasi laut & tawar, struktur folder
- [x] Preprocessing - split train/val/test (70/20/10), augmentasi, normalisasi
- [ ] Training YOLOv8 - train model klasifikasi, monitoring, simpan model
- [ ] Evaluasi - confusion matrix, classification report
- [ ] Dashboard - Flask, upload gambar, tampilkan hasil klasifikasi

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
├── model/
│   ├── train.py          # script training YOLOv8
│   ├── evaluate.py       # script evaluasi
│   └── runs/             # hasil training (weights, metrics)
│
├── dashboard/
│   ├── app.py            # Flask app
│   ├── templates/
│   │   └── index.html    # halaman upload & hasil
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── uploads/          # gambar yang diupload user
│
├── compress.py
├── requirements.txt
└── README.md
```

## Tech Stack

- Python 3.x
- YOLOv8 (Ultralytics)
- Flask
- Pillow

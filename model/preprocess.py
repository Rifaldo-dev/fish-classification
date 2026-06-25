import os
import shutil
import random

# Konfigurasi
DATASET_DIR = "dataset"
OUTPUT_DIR  = "data"
SPLIT       = (0.7, 0.2, 0.1)  # train, val, test
SEED        = 42

random.seed(SEED)

splits = ["train", "val", "test"]

# Kumpulkan semua kelas dari subfolder laut & tawar
classes = []
for jenis in ["laut", "tawar"]:
    jenis_path = os.path.join(DATASET_DIR, jenis)
    if not os.path.exists(jenis_path):
        continue
    for nama_ikan in os.listdir(jenis_path):
        full_path = os.path.join(jenis_path, nama_ikan)
        if os.path.isdir(full_path):
            classes.append((nama_ikan, full_path))

print(f"Kelas ditemukan: {[c[0] for c in classes]}\n")

for split in splits:
    for cls_name, _ in classes:
        os.makedirs(os.path.join(OUTPUT_DIR, split, cls_name), exist_ok=True)

for cls_name, cls_path in classes:
    images = [f for f in os.listdir(cls_path)
              if f.lower().endswith((".jpg", ".jpeg", ".png")) and f != ".gitkeep"]
    random.shuffle(images)

    n = len(images)
    n_train = int(n * SPLIT[0])
    n_val   = int(n * SPLIT[1])

    split_data = {
        "train": images[:n_train],
        "val":   images[n_train:n_train + n_val],
        "test":  images[n_train + n_val:]
    }

    for split, files in split_data.items():
        for fname in files:
            src = os.path.join(cls_path, fname)
            dst = os.path.join(OUTPUT_DIR, split, cls_name, fname)
            shutil.copy2(src, dst)
        print(f"  {cls_name:10s} | {split:5s} : {len(files)} gambar")

print(f"\nSelesai! Dataset tersimpan di '{OUTPUT_DIR}'")
print(f"Struktur siap untuk YOLOv8 classify training.")

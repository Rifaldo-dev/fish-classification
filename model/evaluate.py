from ultralytics import YOLO
from sklearn.metrics import classification_report, confusion_matrix
import os
import numpy as np

# Konfigurasi
MODEL_PATH = "C:/Users/ACER/runs/classify/model/runs/fish-classify/weights/best.pt"
TEST_DIR   = "data/test"

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Model tidak ditemukan: {MODEL_PATH}")
        return

    if not os.path.exists(TEST_DIR):
        print(f"[ERROR] Folder test tidak ditemukan: {TEST_DIR}")
        return

    model = YOLO(MODEL_PATH)

    # Kumpulkan semua gambar test beserta label aslinya
    classes = sorted(os.listdir(TEST_DIR))
    print(f"Kelas: {classes}\n")

    y_true = []
    y_pred = []

    for cls_name in classes:
        cls_path = os.path.join(TEST_DIR, cls_name)
        images = [f for f in os.listdir(cls_path)
                  if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        for img_file in images:
            img_path = os.path.join(cls_path, img_file)
            results = model.predict(img_path, verbose=False)
            pred_class = results[0].names[results[0].probs.top1]

            y_true.append(cls_name)
            y_pred.append(pred_class)

    # Classification Report
    print("=" * 50)
    print("CLASSIFICATION REPORT")
    print("=" * 50)
    print(classification_report(y_true, y_pred, target_names=classes))

    # Confusion Matrix
    print("=" * 50)
    print("CONFUSION MATRIX")
    print("=" * 50)
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    # Header
    header = f"{'':10s}" + "".join(f"{c:10s}" for c in classes)
    print(header)
    for i, row in enumerate(cm):
        print(f"{classes[i]:10s}" + "".join(f"{v:10d}" for v in row))

    # Akurasi keseluruhan
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    total = len(y_true)
    print(f"\nAkurasi Test : {correct}/{total} = {correct/total*100:.2f}%")

if __name__ == "__main__":
    main()

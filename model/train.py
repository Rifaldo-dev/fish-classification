from ultralytics import YOLO
import os

# Konfigurasi
DATA_DIR   = "data"
MODEL      = "yolov8n-cls.pt"   # nano - ringan & cepat
EPOCHS     = 30
IMG_SIZE   = 224
BATCH      = 16
PROJECT    = "model/runs"
NAME       = "fish-classify"

def main():
    # Cek data tersedia
    for split in ["train", "val", "test"]:
        path = os.path.join(DATA_DIR, split)
        if not os.path.exists(path):
            print(f"[ERROR] Folder '{path}' tidak ditemukan.")
            print("Jalankan dulu: python model/preprocess.py")
            return

    classes = os.listdir(os.path.join(DATA_DIR, "train"))
    print(f"Kelas       : {classes}")
    print(f"Jumlah kelas: {len(classes)}")
    print(f"Model       : {MODEL}")
    print(f"Epochs      : {EPOCHS}")
    print(f"Image size  : {IMG_SIZE}x{IMG_SIZE}")
    print(f"Batch size  : {BATCH}")
    print("-" * 40)

    # Load model
    model = YOLO(MODEL)

    # Training
    results = model.train(
        data=DATA_DIR,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        project=PROJECT,
        name=NAME,
        save=True,
        plots=True,
        verbose=True,
    )

    print("\nTraining selesai!")
    print(f"Model tersimpan di: {PROJECT}/{NAME}/weights/best.pt")

if __name__ == "__main__":
    main()

from PIL import Image
import os

dataset_dir = "dataset"
target_size = (224, 224)
quality = 85

total_before = 0
total_after = 0
count = 0

for root, dirs, files in os.walk(dataset_dir):
    for fname in files:
        if fname == ".gitkeep":
            continue
        ext = fname.lower().split(".")[-1]
        if ext not in ("jpg", "jpeg", "png", "webp", "bmp"):
            continue

        fpath = os.path.join(root, fname)
        size_before = os.path.getsize(fpath)
        total_before += size_before

        try:
            img = Image.open(fpath).convert("RGB")
            img = img.resize(target_size, Image.LANCZOS)

            # Simpan sebagai jpg
            new_path = os.path.splitext(fpath)[0] + ".jpg"
            img.save(new_path, "JPEG", quality=quality, optimize=True)

            # Hapus file asli kalau extensi berbeda
            if fpath != new_path:
                os.remove(fpath)

            size_after = os.path.getsize(new_path)
            total_after += size_after
            count += 1

            print(f"[{count}] {fname} : {size_before//1024}KB -> {size_after//1024}KB")

        except Exception as e:
            print(f"SKIP {fname}: {e}")

print(f"\n{'='*40}")
print(f"Total file    : {count}")
print(f"Sebelum       : {total_before/1024/1024:.2f} MB")
print(f"Sesudah       : {total_after/1024/1024:.2f} MB")
print(f"Hemat         : {(total_before-total_after)/1024/1024:.2f} MB ({100*(1-total_after/total_before):.1f}%)")

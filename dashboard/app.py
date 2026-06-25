from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
from PIL import Image
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MODEL_PATH = "C:/Users/ACER/runs/classify/model/runs/fish-classify/weights/best.pt"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

model = YOLO(MODEL_PATH)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang dikirim"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Format file tidak valid. Gunakan JPG atau PNG"}), 400

    # Simpan file
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Prediksi
    results = model.predict(filepath, verbose=False)
    probs = results[0].probs
    names = results[0].names

    # Top 3 prediksi
    top3_idx = probs.top5[:3]
    top3 = [
        {"label": names[i], "confidence": round(float(probs.data[i]) * 100, 2)}
        for i in top3_idx
    ]

    return jsonify({
        "prediction": top3[0]["label"],
        "confidence": top3[0]["confidence"],
        "top3": top3,
        "image_url": f"/uploads/{filename}"
    })

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)

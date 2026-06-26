from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from ultralytics import YOLO
from dotenv import load_dotenv
from functools import wraps
import pymysql
import os
import uuid
import hashlib

load_dotenv()

app = Flask(__name__)
app.secret_key = "fishid-secret-2025"

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER  = os.path.join(BASE_DIR, "uploads")
MODEL_PATH     = "C:/Users/ACER/runs/classify/model/runs/fish-classify/weights/best.pt"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO(MODEL_PATH)

FISH_TYPE = {
    "kakap":   "Ikan Laut",
    "kuwe":    "Ikan Laut",
    "lema":    "Ikan Laut",
    "arwana":  "Ikan Air Tawar",
    "cupang":  "Ikan Air Tawar",
    "koi":     "Ikan Air Tawar",
    "maskoki": "Ikan Air Tawar",
}

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "fishid_db"),
        cursorclass=pymysql.cursors.DictCursor
    )

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ── Routes ──────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        hashed   = hashlib.sha256(password.encode()).hexdigest()
        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed))
            user = cur.fetchone()
        db.close()
        if user:
            session["user"] = user["username"]
            return redirect(url_for("dashboard"))
        error = "Username atau password salah"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM riwayat_identifikasi")
        total_identifikasi = cur.fetchone()["total"]
    db.close()
    return render_template("dashboard.html", active="dashboard", total_identifikasi=total_identifikasi)

@app.route("/identifikasi")
@login_required
def identifikasi():
    return render_template("identifikasi.html", active="identifikasi")

@app.route("/riwayat")
@login_required
def riwayat():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM riwayat_identifikasi ORDER BY created_at DESC LIMIT 50")
        rows = cur.fetchall()
    db.close()
    return render_template("riwayat.html", active="riwayat", rows=rows)

@app.route("/harga")
@login_required
def harga():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM harga_ikan ORDER BY jenis, nama_ikan")
        rows = cur.fetchall()
    db.close()
    return render_template("harga.html", active="harga", rows=rows)

@app.route("/harga/update", methods=["POST"])
@login_required
def harga_update():
    data = request.get_json()
    db = get_db()
    with db.cursor() as cur:
        cur.execute("UPDATE harga_ikan SET harga_per_kg=%s WHERE id=%s", (data["harga"], data["id"]))
    db.commit()
    db.close()
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Format tidak valid. Gunakan JPG atau PNG"}), 400

    ext      = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    results  = model.predict(filepath, verbose=False)
    probs    = results[0].probs
    names    = results[0].names
    top3_idx = probs.top5[:3]
    top3 = [
        {"label": names[i], "confidence": round(float(probs.data[i]) * 100, 2)}
        for i in top3_idx
    ]

    prediction = top3[0]["label"]
    confidence = top3[0]["confidence"]
    fish_type  = FISH_TYPE.get(prediction, "Tidak diketahui")

    # Ambil harga dari DB
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT harga_per_kg FROM harga_ikan WHERE nama_ikan=%s", (prediction,))
        row = cur.fetchone()
        harga = int(row["harga_per_kg"]) if row else None

        # Simpan riwayat
        cur.execute(
            "INSERT INTO riwayat_identifikasi (nama_ikan, jenis_ikan, confidence, image_path) VALUES (%s,%s,%s,%s)",
            (prediction, fish_type, confidence, filename)
        )
    db.commit()
    db.close()

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "fish_type":  fish_type,
        "harga":      harga,
        "top3":       top3,
        "image_url":  f"/uploads/{filename}"
    })

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, reloader_type="stat")

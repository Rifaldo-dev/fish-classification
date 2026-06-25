const uploadBox    = document.getElementById("uploadBox");
const fileInput    = document.getElementById("fileInput");
const uploadContent = document.getElementById("uploadContent");
const previewImg   = document.getElementById("previewImg");
const btnPredict   = document.getElementById("btnPredict");
const resultBox    = document.getElementById("resultBox");
const resultLabel  = document.getElementById("resultLabel");
const resultConf   = document.getElementById("resultConfidence");
const top3List     = document.getElementById("top3List");
const loading      = document.getElementById("loading");
const btnReset     = document.getElementById("btnReset");

let selectedFile = null;

// Klik upload box
uploadBox.addEventListener("click", () => fileInput.click());

// Drag & drop
uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.classList.add("drag-over");
});
uploadBox.addEventListener("dragleave", () => uploadBox.classList.remove("drag-over"));
uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadBox.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

// Pilih file
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

function handleFile(file) {
  if (!["image/jpeg", "image/png"].includes(file.type)) {
    alert("Format file harus JPG atau PNG");
    return;
  }
  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewImg.hidden = false;
    uploadContent.hidden = true;
    btnPredict.disabled = false;
  };
  reader.readAsDataURL(file);

  // Sembunyikan hasil lama
  resultBox.hidden = true;
}

// Tombol prediksi
btnPredict.addEventListener("click", async () => {
  if (!selectedFile) return;

  btnPredict.disabled = true;
  loading.hidden = false;
  resultBox.hidden = true;

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const res = await fetch("/predict", { method: "POST", body: formData });
    const data = await res.json();

    if (data.error) {
      alert(data.error);
      return;
    }

    // Tampilkan hasil
    resultLabel.textContent = data.prediction;
    resultConf.textContent = `${data.confidence}%`;

    // Top 3 bar
    top3List.innerHTML = "";
    data.top3.forEach(item => {
      const div = document.createElement("div");
      div.className = "top3-item";
      div.innerHTML = `
        <span>${item.label}</span>
        <div class="bar-bg">
          <div class="bar-fill" style="width: ${item.confidence}%"></div>
        </div>
        <span class="pct">${item.confidence}%</span>
      `;
      top3List.appendChild(div);
    });

    resultBox.hidden = false;
  } catch (err) {
    alert("Gagal menghubungi server. Pastikan Flask berjalan.");
  } finally {
    loading.hidden = true;
    btnPredict.disabled = false;
  }
});

// Reset
btnReset.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  previewImg.src = "";
  previewImg.hidden = true;
  uploadContent.hidden = false;
  btnPredict.disabled = true;
  resultBox.hidden = true;
});

const uploadBox     = document.getElementById("uploadBox");
const fileInput     = document.getElementById("fileInput");
const uploadContent = document.getElementById("uploadContent");
const previewImg    = document.getElementById("previewImg");
const btnPredict    = document.getElementById("btnPredict");
const btnReset      = document.getElementById("btnReset");
const resultBox     = document.getElementById("resultBox");
const emptyBox      = document.getElementById("emptyBox");
const resultLabel   = document.getElementById("resultLabel");
const resultConf    = document.getElementById("resultConfidence");
const top3List      = document.getElementById("top3List");

let selectedFile = null;

uploadBox.addEventListener("click", () => fileInput.click());

uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.classList.add("drag-over");
});
uploadBox.addEventListener("dragleave", () => uploadBox.classList.remove("drag-over"));
uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadBox.classList.remove("drag-over");
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});

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
    btnReset.hidden = false;
  };
  reader.readAsDataURL(file);
  resultBox.hidden = true;
  emptyBox.hidden = false;
}

btnPredict.addEventListener("click", () => {
  if (!selectedFile) return;

  btnPredict.disabled = true;
  btnPredict.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Memproses...';
  resultBox.hidden = true;
  emptyBox.hidden = true;

  const formData = new FormData();
  formData.append("file", selectedFile);

  fetch("/predict", { method: "POST", body: formData })
    .then(res => {
      if (!res.ok) throw new Error("Server error " + res.status);
      return res.json();
    })
    .then(data => {
      if (data.error) { alert(data.error); emptyBox.hidden = false; return; }

      resultLabel.textContent = data.prediction;
      resultConf.textContent  = "Confidence: " + data.confidence + "%";

      const hargaEl = document.getElementById("resultHarga");
      if (data.harga) {
        hargaEl.innerHTML = '<i class="fa-solid fa-tag me-1"></i>Rp ' + data.harga.toLocaleString("id-ID") + " / kg";
      } else {
        hargaEl.textContent = "";
      }

      const typeEl = document.getElementById("resultType");
      typeEl.textContent = data.fish_type;
      typeEl.className = "result-type badge " + (data.fish_type === "Ikan Laut" ? "type-laut" : "type-tawar");

      top3List.innerHTML = "";
      data.top3.forEach(item => {
        const d = document.createElement("div");
        d.className = "top3-item";
        d.innerHTML =
          '<span class="item-label">' + item.label + '</span>' +
          '<div class="bar-bg"><div class="bar-fill" style="width:' + item.confidence + '%"></div></div>' +
          '<span class="pct">' + item.confidence + '%</span>';
        top3List.appendChild(d);
      });

      resultBox.hidden = false;
    })
    .catch(err => {
      alert("Error: " + err.message);
      emptyBox.hidden = false;
    })
    .finally(() => {
      btnPredict.disabled = false;
      btnPredict.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles me-1"></i> Identifikasi';
    });
});

btnReset.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  previewImg.src = "";
  previewImg.hidden = true;
  uploadContent.hidden = false;
  btnPredict.disabled = true;
  btnReset.hidden = true;
  resultBox.hidden = true;
  emptyBox.hidden = false;
});

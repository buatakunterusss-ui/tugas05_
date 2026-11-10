import os
import warnings
import joblib
import numpy as np
from flask import Flask, render_template, request

warnings.filterwarnings("ignore", message="X does not have valid feature names")

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "..", "model", "model_decision_tree.pkl")
FEATURES_PATH = os.path.join(BASE, "..", "model", "features.pkl")

app = Flask(__name__, template_folder=os.path.join(BASE, "templates"))
model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

LABELS = {
    "radius_mean": "Radius rata-rata",
    "texture_mean": "Tekstur rata-rata",
    "perimeter_mean": "Perimeter rata-rata",
    "area_mean": "Luas area rata-rata",
    "smoothness_mean": "Kehalusan rata-rata",
    "compactness_mean": "Kekompakan rata-rata",
    "concavity_mean": "Konkavitas rata-rata",
    "concave points_mean": "Titik konkaf rata-rata",
    "symmetry_mean": "Simetri rata-rata",
    "fractal dimension_mean": "Dimensi fraktal rata-rata",
}
# Contoh nilai (median tiap kelas pada dataset) agar mudah dicoba
EXAMPLES = {
    "jinak": {"radius_mean": 12.2, "texture_mean": 17.39, "perimeter_mean": 78.18, "area_mean": 458.4,
              "smoothness_mean": 0.0908, "compactness_mean": 0.0752, "concavity_mean": 0.0371,
              "concave points_mean": 0.0235, "symmetry_mean": 0.1714, "fractal dimension_mean": 0.0633},
    "ganas": {"radius_mean": 17.325, "texture_mean": 21.46, "perimeter_mean": 114.2, "area_mean": 932.0,
              "smoothness_mean": 0.1022, "compactness_mean": 0.1323, "concavity_mean": 0.1514,
              "concave points_mean": 0.0861, "symmetry_mean": 0.1899, "fractal dimension_mean": 0.0615},
}
FIELDS = [{"key": f, "id": f.replace(" ", "_"), "label": LABELS.get(f, f)} for f in features]


@app.route("/", methods=["GET", "POST"])
def index():
    values = {f["id"]: "" for f in FIELDS}
    result = None
    error = None
    if request.method == "POST":
        try:
            row = {}
            for f in FIELDS:
                raw = request.form.get(f["id"], "").strip().replace(",", ".")
                values[f["id"]] = raw
                row[f["key"]] = float(raw)
            X = np.array([[row[k] for k in features]])
            pred = int(model.predict(X)[0])
            proba = model.predict_proba(X)[0]
            result = {
                "label": "Ganas (Malignant)" if pred == 1 else "Jinak (Benign)",
                "kelas": "ganas" if pred == 1 else "jinak",
                "prob_ganas": round(float(proba[1]) * 100, 1),
                "prob_jinak": round(float(proba[0]) * 100, 1),
            }
        except ValueError:
            error = "Semua kolom harus diisi dengan angka yang valid."
    return render_template("index.html", fields=FIELDS, values=values,
                           result=result, error=error, examples=EXAMPLES)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

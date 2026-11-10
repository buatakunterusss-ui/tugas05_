# TA-05 Decision Tree: Klasifikasi Tumor Payudara

Pembelajaran Mesin, Modul 05. Model Decision Tree (max_depth=3) untuk memprediksi tumor ganas atau jinak
dari dataset Breast Cancer Wisconsin (Diagnostic), disajikan sebagai aplikasi web Flask.

## Struktur
- `notebook/analisis_decision_tree.ipynb` : EDA, preprocessing, Model A vs Model B, evaluasi, visualisasi
- `app/` : aplikasi Flask (`app.py`, `templates/index.html`)
- `model/` : model dan daftar fitur (Joblib)
- `data/breast_cancer.csv`, `figures/`

## Menjalankan lokal
```
pip install -r requirements.txt
python app/app.py
```
Buka http://localhost:5000

## Deploy (Render)
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --chdir app app:app`

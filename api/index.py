# Titik masuk untuk Vercel: memuat aplikasi Flask dari app/app.py
import os
import importlib.util

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "app.py")
_spec = importlib.util.spec_from_file_location("flask_app", _path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

app = _mod.app

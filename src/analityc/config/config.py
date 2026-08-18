import os

# Configuración centralizada
MODEL_PATH = os.getenv("MODEL_PATH", "models/base/yolo11m.pt")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "9000"))

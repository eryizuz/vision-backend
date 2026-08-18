from ultralytics import YOLO
import os

# Asegurar que los modelos se descarguen en la carpeta models
os.makedirs('/home/gsu/repos/python/SERVER-IA/models', exist_ok=True)
model = YOLO("yolo11m.pt")
print("YOLO11m listo.")

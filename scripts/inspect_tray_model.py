from ultralytics import YOLO

model = YOLO("/home/gsu/repos/python/SERVER-IA/models/cosmeticos/weights/best.pt")
print("Clases del modelo:", model.names)

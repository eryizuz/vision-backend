import cv2
import json
import os
from src.analityc.core.person_amazona_inference import PersonAmazonasInference

def test_tray_integration():
    print("--- Probando integración YOLO11 + Tray Detection ---")
    video_path = "/home/gsu/repos/python/SERVER-IA/output/test_video.mp4"
    cap = cv2.VideoCapture(video_path)
    
    # Asegurar que las variables de entorno estén configuradas para el test
    os.environ["MODEL_PATH_AMAZONAS"] = "/home/gsu/repos/python/SERVER-IA/models/cosmeticos/weights/best.pt"
    
    inference = PersonAmazonasInference()
    
    # Procesar primer frame
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el video")
        return

    detections = inference.process_frame(frame)
    
    print(f"Detecciones procesadas: {len(detections)}")
    for det in detections:
        print(f"ID: {det['track_id']}, Tray detected: {det['holding_tray']}")
    
    cap.release()

if __name__ == "__main__":
    test_tray_integration()

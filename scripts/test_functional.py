import cv2
import json
from src.analityc.core.person_amazona_inference import PersonAmazonasInference
from src.analityc.core.analytics.demographics import DemographicsModule

def test_video(video_path):
    print(f"--- Procesando: {video_path} ---")
    cap = cv2.VideoCapture(video_path)
    inference = PersonAmazonasInference(model_path="/home/gsu/repos/python/SERVER-IA/models/base/yolo11m.pt")
    demographics = DemographicsModule()
    
    # Procesar solo un frame para prueba rápida
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el video")
        return

    detections = inference.process_frame(frame)
    demo_results = demographics.analyze(frame)
    
    print(json.dumps({
        "persons_detected": len(detections),
        "demographics": demo_results
    }, indent=2))
    cap.release()

if __name__ == "__main__":
    test_video("/home/gsu/repos/python/SERVER-IA/output/test_video.mp4")
    test_video("/home/gsu/repos/python/SERVER-IA/output/asdasd.mp4")

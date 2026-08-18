from ultralytics import YOLO
import cv2

class PersonAmazonasInference:
    def __init__(self, model_path="yolo11m.pt"):
        # Carga del modelo YOLO11
        self.model = YOLO(model_path)

    def process_frame(self, frame):
        # Inferencia con seguimiento (BoTSORT integrado por defecto en predict)
        # tracker='botsort.yaml' activa el rastreador
        results = self.model.track(
            frame, 
            persist=True, 
            tracker="botsort.yaml", 
            classes=[0] # Clase 0 para personas en COCO
        )
        
        detections = []
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            
            for box, track_id in zip(boxes, track_ids):
                detections.append({
                    "box": box.tolist(),
                    "track_id": int(track_id)
                })
        
        return detections

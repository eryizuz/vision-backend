from ultralytics import YOLO
import cv2
import os
import numpy as np
from src.analityc.config.config import MODEL_PATH

class PersonAmazonasInference:
    def __init__(self):
        # Carga del modelo base (personas)
        self.model = YOLO(MODEL_PATH)
        # Carga del modelo de cosméticos (bandejas/objetos) si existe
        cosmetics_path = os.getenv("MODEL_PATH_AMAZONAS", "models/cosmeticos/weights/best.pt")
        self.cosmetics_model = None
        if os.path.exists(cosmetics_path):
            self.cosmetics_model = YOLO(cosmetics_path)

    def process_frame(self, frame):
        # Detección y tracking de personas
        results = self.model.track(frame, persist=True, tracker="botsort.yaml", classes=[0])
        
        detections = []
        tray_boxes = [] # Initialize tray boxes
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            
            # Detección de bandejas
            if self.cosmetics_model:
                tray_res = self.cosmetics_model(frame, classes=[0])
                for box in tray_res[0].boxes.xyxy.cpu().numpy():
                    tray_boxes.append(box.tolist())

            # Data for people
            people_data = []
            for box, track_id in zip(boxes, track_ids):
                # Expand box upwards
                height = box[3] - box[1]
                # Expand more to ensure hands/chest coverage
                expanded_box = [box[0], box[1] - height * 1.2, box[2], box[3]]
                people_data.append({
                    "box": box.tolist(),
                    "expanded_box": expanded_box,
                    "track_id": int(track_id),
                    "center": ((box[0] + box[2])/2, (box[1] + box[3])/2),
                    "holding_tray": False
                })

            # Assign trays
            for t_box in tray_boxes:
                t_center_x = (t_box[0] + t_box[2]) / 2
                t_center_y = (t_box[1] + t_box[3]) / 2
                
                min_dist = float('inf')
                closest_person_idx = -1
                
                for i, person in enumerate(people_data):
                    # Check if in expanded box
                    e_box = person["expanded_box"]
                    if e_box[0] <= t_center_x <= e_box[2] and \
                       e_box[1] <= t_center_y <= e_box[3]:
                        # Distance to center of person box
                        dist = np.sqrt((t_center_x - person["center"][0])**2 + \
                                       (t_center_y - person["center"][1])**2)
                        if dist < min_dist:
                            min_dist = dist
                            closest_person_idx = i
                
                if closest_person_idx != -1:
                    people_data[closest_person_idx]["holding_tray"] = True
            
            # Construct detections list
            for person in people_data:
                detections.append({
                    "box": person["box"],
                    "track_id": person["track_id"],
                    "holding_tray": person["holding_tray"]
                })
        
        return detections, tray_boxes

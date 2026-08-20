import cv2

class Overlay:
    def draw(self, frame, detections, tray_boxes):
        # Draw people
        for det in detections:
            box = det['box']
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {det['track_id']}", (int(box[0]), int(box[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw trays
        for t_box in tray_boxes:
            cv2.rectangle(frame, (int(t_box[0]), int(t_box[1])), (int(t_box[2]), int(t_box[3])), (0, 0, 255), 2)
            cv2.putText(frame, "Tray", (int(t_box[0]), int(t_box[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
        return frame

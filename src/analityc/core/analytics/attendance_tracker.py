import math

class AttendanceTracker:
    def __init__(self, proximity_threshold=100):
        self.threshold = proximity_threshold

    def check_interaction(self, detections):
        interactions = []
        # Suposición: ID 0 es vendedor, otros son clientes
        for i, d1 in enumerate(detections):
            for d2 in detections[i+1:]:
                dist = self._calculate_dist(d1['box'], d2['box'])
                if dist < self.threshold:
                    interactions.append((d1['track_id'], d2['track_id']))
        return interactions

    def _calculate_dist(self, b1, b2):
        # Distancia entre centros
        c1 = ((b1[0]+b1[2])/2, (b1[1]+b1[3])/2)
        c2 = ((b2[0]+b2[2])/2, (b2[1]+b2[3])/2)
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

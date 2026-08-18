class PeopleCounter:
    def __init__(self):
        self.unique_ids = set()

    def update(self, detections):
        for det in detections:
            self.unique_ids.add(det['track_id'])
        return len(self.unique_ids)

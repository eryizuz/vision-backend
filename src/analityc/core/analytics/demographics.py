from insightface.app import FaceAnalysis

class DemographicsModule:
    def __init__(self):
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def _get_age_range(self, age):
        if age < 18: return "0-17"
        if age < 35: return "18-34"
        if age < 50: return "35-49"
        return "50+"

    def analyze(self, frame):
        faces = self.app.get(frame)
        demographics = []
        for face in faces:
            demographics.append({
                "age": int(face.age),
                "age_range": self._get_age_range(int(face.age)),
                "gender": "male" if face.gender == 1 else "female",
                "bbox": face.bbox.tolist()
            })
        return demographics

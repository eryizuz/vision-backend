import onnxruntime as ort
import numpy as np
import os
from src.analityc.config.config import MODEL_PATH

class FaceReidentifier:
    def __init__(self):
        # Ajustar ruta al modelo ArcFace
        model_path = os.path.join(os.path.dirname(MODEL_PATH), "../classifiers/w600k_r50.onnx")
        self.session = ort.InferenceSession(model_path)

    def get_embedding(self, face_img):
        # Preprocesamiento básico: redimensionar a 112x112 y normalizar
        img = cv2.resize(face_img, (112, 112))
        img = img.transpose(2, 0, 1).astype(np.float32)
        img = (img - 127.5) / 128.0
        img = np.expand_dims(img, axis=0)
        
        # Inferencia
        input_name = self.session.get_inputs()[0].name
        embedding = self.session.run(None, {input_name: img})[0]
        return embedding.flatten()

from insightface.app import FaceAnalysis
import os

# Asegurar carpeta de modelos
os.makedirs('/home/gsu/repos/python/SERVER-IA/models', exist_ok=True)
app = FaceAnalysis(name='buffalo_l', root='/home/gsu/repos/python/SERVER-IA/models')
app.prepare(ctx_id=0, det_size=(640, 640))
print("Face embeddings listo.")

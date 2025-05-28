import numpy as np
from insightface.app import FaceAnalysis
import cv2

embeddings = np.load('cyclist_embeddings.npy', allow_pickle=True).item()

faceapp = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
faceapp.prepare(ctx_id=0)

img = cv2.imread("test_images/lotte_test.jpeg")
faces = faceapp.get(img)

if faces:
    emb_test = faces[0].embedding

    # Calculer la distance à tous les cyclistes connus
    best_name = None
    best_score = -1

    for name, emb_ref in embeddings.items():
        # Cosine similarity
        score = np.dot(emb_ref, emb_test) / (np.linalg.norm(emb_ref) * np.linalg.norm(emb_test))

        if score > best_score:
            best_score = score
            best_name = name

    print(f"Prediction: {best_name} (score: {best_score:.4f})")

else:
    print("No face detected in the image")


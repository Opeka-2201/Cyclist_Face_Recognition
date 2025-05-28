import os
import numpy as np
import cv2
from tqdm import tqdm
from insightface.app import FaceAnalysis

# Init face detector + embedding model
faceapp = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
faceapp.prepare(ctx_id=0)

image_folder = 'mugshots'
embeddings = {}
failed = []

for filename in tqdm(os.listdir(image_folder)):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    name = os.path.splitext(filename)[0].replace("-", " ")
    path = os.path.join(image_folder, filename)

    img = cv2.imread(path)
    if img is None:
        print(f"Error loading {filename}")
        continue

    faces = faceapp.get(img)
    if len(faces) == 0:
        failed.append(name)
        continue

    # Use first detected face (should be only one)
    emb = faces[0].embedding
    embeddings[name] = emb

# Save embeddings to disk
np.save("cyclist_embeddings.npy", embeddings)

print(f"Saved {len(embeddings)} embeddings.")
if failed:
    print("Failed to detect face for:", failed)

import cv2  # type: ignore
import numpy as np  # type: ignore
from insightface.app import FaceAnalysis  # type: ignore
import mss  # type: ignore
import time
import pyautogui  # type: ignore

time.sleep(0.01)
start = True
translation = None

""" needed for MacOS
translation = {
    'q': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'i': 'i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    ',': 'm',
    'n': 'n',
    'o': 'o',
    'p': 'p',
    'a': 'q',
    'r': 'r',
    's': 's',
    't': 't',
    'u': 'u',
    'v': 'v',
    'z': 'w',
    'x': 'x',
    'y': 'y',
    'w': 'z',
    'm': ';',
    ' ': ' '
}
"""


def translate(text):
    if translation is None:
        return text

    translated = ""
    for c in text:
        if c in translation:
            translated += translation[c]
        else:
            translated += c

    return translated


# Prediction function
def predict_identity(face_embedding):
    best_name = None
    best_score = -1
    for name, emb_ref in embeddings.items():
        score = np.dot(emb_ref, face_embedding) / (
            np.linalg.norm(emb_ref) * np.linalg.norm(face_embedding)
        )
        if score > best_score:
            best_score = score
            best_name = name
    return best_name, best_score


# Load embeddings
embeddings = np.load("data/cyclist_embeddings.npy", allow_pickle=True).item()

# Init InsightFace face detector and embedding model
faceapp = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
faceapp.prepare(ctx_id=0)

# Screen capture using mss (may need to allow access in macOS)
sct = mss.mss()
monitor = {"top": 0, "left": 0, "width": 720, "height": 900}  # Adjust

while True:
    while start:
        input(
            "Press Enter to continue (you have 2 seconds to put your "
            "cursor on the quiz box)..."
        )
        start = False
        # time.sleep(2)

    # Screen capture
    sct_img = sct.grab(monitor)
    img = np.array(sct_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    faces = faceapp.get(img)

    for face in faces:
        box = face.bbox.astype(int)
        name, score = predict_identity(face.embedding)

        if score > 0.4:  # Threshold to tune
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]),
                          (0, 0, 255), 2)
            cv2.putText(
                img,
                f"{name}",
                (box[0] - 30, box[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                img,
                f"Score: {score:.2f}",
                (box[0] - 30, box[3] + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

            pyautogui.press("command")
            # Uncomment below to type the name in the quiz box
            # pyautogui.typewrite(translate(name), interval=0.05)
            # pyautogui.press("enter")

    # Show the image with detected faces
    cv2.imshow("Cyclist Recognition", img)
    if cv2.waitKey(1) == ord("q"):
        break

    # Load limiter
    # time.sleep(0.1)

cv2.destroyAllWindows()

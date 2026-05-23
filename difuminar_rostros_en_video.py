import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

cap = cv2.VideoCapture("video.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rostros_detectados = app.get(frame)

    for rostro in rostros_detectados:
        bbox = rostro.bbox.astype(int)
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]

        h, w, _ = frame.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        rostro_roi = frame[y1:y2, x1:x2]
        
        if rostro_roi.size > 0:
            difuminado = cv2.GaussianBlur(rostro_roi, (99, 99), 0)
            frame[y1:y2, x1:x2] = difuminado

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

    cv2.imshow("Video", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
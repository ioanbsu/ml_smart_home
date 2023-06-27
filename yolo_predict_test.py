# Use this file to test accuracy of your model.
import math

import cv2
import cvzone
from ultralytics import YOLO

# configure camera capture.
cap = cv2.VideoCapture(0)  # for the laptop's webcam
width = 1280
height = 720
cap.set(3, width)
cap.set(4, height)

# You'd need to train your model first, see train/train.ipynb notebook for details.
# Load a model. Look fo the weights (best.pt) in train/runs/detect/trainX/weights/* folders
model = YOLO('/INSERT_HERE_PATH_TO_YOLO_TRAIN_FOLDER/best.pt')  # load a custom model

# Predict with the model
while True:
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (width, height))
        # device = "mps" optimized for M1/M2 macs, for other hardware, you can remove device="mps"
        results = model(img, stream=True, device="mps")
        for result in results:
            bboxes = result.boxes.data
            for bbox in bboxes:
                x1, y1, x2, y2 = bbox[:4]
                w, h = x2 - x1, y2 - y1
                className = result.names[int(bbox[5].item())]
                confidence = math.ceil(bbox[4] * 100) / 100

                x1, y1, x2, y2, w, h = int(x1), int(y1), int(x2), int(y2), int(w), int(h)
                color = (255, 255, 255)
                if className == 'SwitchOn' or className == 'DyiSwitchOn':
                    color = (0, 255, 0)
                elif className == 'SwitchOff' or className == 'DyiSwitchOff':
                    color = (0, 0, 255)
                cvzone.cornerRect(img, (x1, y1, w, h), t=2, l=5, colorR=color, colorC=color, rt=5)
                cvzone.putTextRect(img, f'{className} - {confidence}', (max(0, x1), max(35, y1)), scale=1.0,
                                   thickness=1,
                                   colorB=color,
                                   offset=5)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

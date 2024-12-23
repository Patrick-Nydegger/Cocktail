"""
Here, the main menu and application control will be programmed. The current file was not completed.
"""


"""

import cv2
import numpy as np
from ultralytics import YOLO

# Load model
model = YOLO('best.pt')

# open camera
cap = cv2.VideoCapture(0)

while True:
    # Lies ein Frame
    ret, frame = cap.read()
    if not ret:
        print("Frame could not be read")
        break

    results = model(frame)

    # Process the results, if any
    if results and len(results) > 0:
        for detection in results[0].boxes:  # Zugriff auf das erste Bild und seine Detections
            # Extrahiere die Bounding-Box-Koordinaten und Klasse
            x_min, y_min, x_max, y_max = map(int, detection.xyxy[0])  # Bounding-Box-Koordinaten
            confidence = detection.conf[0]  # Vertrauen
            class_id = int(detection.cls[0])  # Klassen-ID

            # Draw the rectangle around the detected object
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            # Add the class name and confidence
            label = f"{results[0].names[class_id]}: {confidence:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Show results
    cv2.imshow('YOLOv8 Detection', frame)

    # quit with 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# release camera
cap.release()
cv2.destroyAllWindows()

"""

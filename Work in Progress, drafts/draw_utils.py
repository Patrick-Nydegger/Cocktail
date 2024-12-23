"""
Draw the given detections on the frame.
"""

import cv2
from ultralytics import YOLO


def draw_object(frame, detections, color=(255, 255, 255), label_prefix="Object"):
    for detection in detections:
        # Check if the detection has at least 5 values
        if len(detection) < 5:
            continue

        # Extract the first 5 values
        x_min, y_min, x_max, y_max, confidence = detection[:5]
        class_name = detection[5] if len(detection) > 5 else "Unknown"

        # Create the label with the class name and confidence
        label = f"{label_prefix} {class_name}: {confidence:.2f}"

        # Draw the rectangle and the label
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
        cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame


class BottleClassifier:
    def __init__(self, model_path='best.pt'):
        self.model = YOLO(model_path)

    def classify_bottles(self, frame):
        results = self.model(frame)
        names = self.model.names

        detections = []
        if results and len(results) > 0:
            for detection in results[0].boxes:
                x_min, y_min, x_max, y_max = map(int, detection.xyxy[0])
                confidence = detection.conf[0]
                class_id = int(detection.cls[0])
                class_name = names[class_id]

                detections.append((x_min, y_min, x_max, y_max, confidence, class_name))
        return detections

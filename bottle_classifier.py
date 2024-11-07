from ultralytics import YOLO


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
                class_name = names[class_id]  # Erhalte den Klassennamen

                detections.append((x_min, y_min, x_max, y_max, confidence, class_id, class_name))
        return detections

from ultralytics import YOLO


class BottleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # YOLOv8-Modell laden
        self.model = YOLO(model_path)

    def detect_bottles(self, frame):
        # Modell auf den Frame anwenden
        results = self.model(frame)
        detections = []

        # Überprüfe, ob Ergebnisse vorhanden sind und durchlaufe die Erkennungsergebnisse
        if results and len(results) > 0:
            for result in results[0].boxes:
                class_id = int(result.cls.cpu().numpy())
                confidence = float(result.conf.cpu().numpy())

                # Nur Flaschen erkennen (class_id 39)
                if class_id == 39 and confidence > 0.7:
                    x_min, y_min, x_max, y_max = result.xyxy[0].cpu().numpy().astype(int)
                    detections.append((x_min, y_min, x_max, y_max, confidence, class_id))

        return detections

"""
The following file generally recognizes bottles using the pre-trained YOLOv8n model. This was adopted from the first
approach but was not conclusively completed due to lack of time.
"""

from ultralytics import YOLO


class BottleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # Load YOLOv8-Model
        self.model = YOLO(model_path)

    def detect_bottles(self, frame):
        results = self.model(frame)
        detections = []

        # Check if results are available and iterate through the detection results
        if results and len(results) > 0:
            for result in results[0].boxes:
                class_id = int(result.cls.cpu().numpy())
                confidence = float(result.conf.cpu().numpy())

                # Only recognize bottles (class_id 39)
                if class_id == 39 and confidence > 0.7:
                    x_min, y_min, x_max, y_max = result.xyxy[0].cpu().numpy().astype(int)
                    detections.append((x_min, y_min, x_max, y_max, confidence, class_id))

        return detections

import cv2
from ultralytics import YOLO

def draw_object(frame, detections, color=(255, 0, 0), label_prefix="Object"):
    """
    Zeichnet die gegebenen Detektionen auf dem Frame.

    Args:
        frame: Das Bild, auf das gezeichnet wird.
        detections: Liste von Detektionen, jede als Tuple (x_min, y_min, x_max, y_max, confidence, class_name).
        color: Farbe der Box (B, G, R).
        label_prefix: Text-Label für die Detektionen.
    """
    for detection in detections:
        # Überprüfe, ob die Detektion mindestens 5 Werte hat
        if len(detection) < 5:
            continue  # Überspringe diese Detektion, wenn sie nicht genug Werte hat

        # Extrahiere die ersten 5 Werte
        x_min, y_min, x_max, y_max, confidence = detection[:5]
        class_name = detection[5] if len(detection) > 5 else "Unknown"  # Verwende den Klassennamen, falls vorhanden

        # Erstelle das Label mit dem Klassennamen und der Konfidenz
        label = f"{label_prefix} {class_name}: {confidence:.2f}"

        # Zeichne das Rechteck und das Label
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
                class_name = names[class_id]  # Erhalte den Klassennamen

                detections.append((x_min, y_min, x_max, y_max, confidence, class_name))  # Füge den Klassennamen hinzu
        return detections

import cv2
from ultralytics import YOLO
import numpy as np

# YOLOv8-Modell laden
yolo = YOLO("yolov8n.pt")  # Verwende das YOLOv8 Nano-Modell

# Liste von Trackern und zugehörigen Bounding Boxes
trackers = []
tracker_labels = []

# Schwellwert für die minimale Distanz zwischen Trackern
MIN_DISTANCE = 50  # Pixel
CONFIDENCE_THRESHOLD = 0.3  # Mindestvertrauensschwelle

# Funktion, um den Mittelpunkt einer Bounding Box zu berechnen
def get_center(bbox):
    x_min, y_min, w, h = bbox
    center_x = x_min + w / 2
    center_y = y_min + h / 2
    return np.array([center_x, center_y])

# Funktion, um den Überlappungsbereich von zwei Bounding Boxes zu berechnen
def bbox_overlap(box1, box2):
    x1_min, y1_min, w1, h1 = box1
    x2_min, y2_min, w2, h2 = box2

    # Die maximalen und minimalen Ecken bestimmen
    x1_max, y1_max = x1_min + w1, y1_min + h1
    x2_max, y2_max = x2_min + w2, y2_min + h2

    # Berechne die Koordinaten der überlappenden Box
    overlap_x_min = max(x1_min, x2_min)
    overlap_y_min = max(y1_min, y2_min)
    overlap_x_max = min(x1_max, x2_max)
    overlap_y_max = min(y1_max, y2_max)

    # Berechne die Fläche der überlappenden Box
    overlap_w = max(0, overlap_x_max - overlap_x_min)
    overlap_h = max(0, overlap_y_max - overlap_y_min)

    overlap_area = overlap_w * overlap_h
    area_box1 = w1 * h1
    area_box2 = w2 * h2

    # Rückgabe des Überlappungsprozentsatzes relativ zur Fläche der größeren Box
    return overlap_area / min(area_box1, area_box2)

# Kamera öffnen
cap = cv2.VideoCapture(0)  # Öffne die Standard-Webcam

if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden!")
    exit()

while True:
    ret, frame = cap.read()  # Frame von der Kamera lesen
    if not ret:
        print("Konnte das Kamerabild nicht lesen!")
        break

    # YOLO Objekterkennung
    results = yolo(frame)

    # YOLO-Ergebnisse verarbeiten und neue Tracker hinzufügen
    for result in results[0].boxes:
        class_id = int(result.cls.cpu().numpy())  # Klassen-ID (von Tensor in NumPy konvertieren)
        confidence = float(result.conf.cpu().numpy())  # Zuverlässigkeit (von Tensor in NumPy konvertieren)

        if class_id == 39 and confidence > 0.5:  # Nur Flaschen erkennen
            # Koordinaten der Bounding Box (von Tensor in NumPy konvertieren)
            x_min, y_min, x_max, y_max = result.xyxy[0].cpu().numpy().astype(int)
            bbox = (x_min, y_min, x_max - x_min, y_max - y_min)

            # Berechne den Mittelpunkt der aktuellen Bounding Box
            new_center = get_center(bbox)

            # Überprüfe, ob ein Tracker in der Nähe ist
            found_existing_tracker = False
            for tracker in trackers:
                success, tracked_bbox = tracker.update(frame)
                if success:
                    tracked_center = get_center(tracked_bbox)
                    distance = np.linalg.norm(new_center - tracked_center)

                    if distance < MIN_DISTANCE:  # Wenn die Objekte nah genug beieinander sind
                        found_existing_tracker = True
                        break

            if not found_existing_tracker:  # Nur wenn kein passender Tracker existiert, erstelle einen neuen
                tracker = cv2.TrackerCSRT_create()  # Oder ein anderer OpenCV-Tracker
                trackers.append(tracker)
                tracker.init(frame, bbox)
                tracker_labels.append(f"Flasche {len(trackers)}")

    # Tracke alle Objekte und überprüfe auf Erfolgsrückgabe
    new_trackers = []
    new_labels = []
    bboxes = []

    for i, tracker in enumerate(trackers):
        success, box = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            bboxes.append((x, y, w, h))  # Speichere die Bounding Boxes

            # Überprüfen Sie den Inhalt im Rahmen mit YOLO
            tracked_frame = frame[y:y + h, x:x + w]
            tracked_results = yolo(tracked_frame)

            # Bestimmen Sie die beste Zuverlässigkeit
            max_confidence = 0.0
            for result in tracked_results[0].boxes:
                confidence = float(result.conf.cpu().numpy())
                if confidence > max_confidence:
                    max_confidence = confidence

            # Überprüfen Sie die Zuverlässigkeit
            if max_confidence < CONFIDENCE_THRESHOLD:
                continue  # Dieser Tracker wird nicht beibehalten

            # Text einfügen
            label = tracker_labels[i]
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Behalte den Tracker nur bei, wenn das Tracking erfolgreich ist
            new_trackers.append(tracker)
            new_labels.append(tracker_labels[i])

    # Vergleiche Bounding Boxes, um den größeren zu löschen, wenn er im kleineren liegt
    to_remove = set()
    for i in range(len(bboxes)):
        for j in range(i + 1, len(bboxes)):
            overlap = bbox_overlap(bboxes[i], bboxes[j])

            # Wenn die Überschneidung hoch ist, lösche die größere Bounding Box
            if overlap > 0.6:  # Überschneidungsschwellwert
                area_i = bboxes[i][2] * bboxes[i][3]  # Fläche der Box i
                area_j = bboxes[j][2] * bboxes[j][3]  # Fläche der Box j
                if area_i > area_j:
                    to_remove.add(i)
                else:
                    to_remove.add(j)

    # Entferne die Tracker, die in einem größeren Bereich liegen
    final_trackers = []
    final_labels = []
    for idx, (tracker, label) in enumerate(zip(new_trackers, new_labels)):
        if idx not in to_remove:
            final_trackers.append(tracker)
            final_labels.append(label)
            # Zeichne den gültigen Rahmen
            (x, y, w, h) = [int(v) for v in bboxes[idx]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 4)

    # Aktualisiere die Listen der Tracker und Labels
    trackers = final_trackers
    tracker_labels = final_labels

    # Frame mit gezeichneten Elementen im Fenster anzeigen
    cv2.imshow('Kamera Feed - Flaschen Tracking', frame)

    # Beenden, wenn "q" gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera freigeben und Fenster schließen
cap.release()
cv2.destroyAllWindows()

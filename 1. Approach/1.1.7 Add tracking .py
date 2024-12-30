import cv2
from ultralytics import YOLO
import pytesseract
from PIL import Image
import numpy as np

# Pfad zur Tesseract-OCR-Installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# YOLOv8-Modell laden
yolo = YOLO("yolov8n.pt")

# Initialisiere eine Liste von Trackern und IDs
trackers = []
track_ids = []
next_track_id = 1

# Funktion zur Texterkennung mit OCR
def ocr_recognition(crop_img):
    pil_img = Image.fromarray(crop_img)
    text = pytesseract.image_to_string(pil_img)
    return text

# Funktion zur Erstellung eines neuen Trackers für jedes Objekt
def create_tracker(frame, box):
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, tuple(box))
    return tracker

# Funktion zur Verarbeitung des Kamerastreams
def process_frame(frame):
    global next_track_id

    # YOLO Objekterkennung durchführen
    results = yolo(frame)

    detections = []
    recognized_texts = []

    # YOLO-Ergebnisse durchgehen und nur Flaschen verarbeiten (Klassen-ID 44)
    for result in results[0].boxes:
        class_id = int(result.cls.numpy())
        confidence = float(result.conf.numpy())

        if class_id == 39 and confidence > 0.3:
            x_min, y_min, x_max, y_max = result.xyxy[0].astype(int)

            # Texterkennung auf dem Bildausschnitt
            crop_img = frame[y_min:y_max, x_min:x_max]
            text = ocr_recognition(crop_img)
            recognized_texts.append(text)

            # Füge die erkannte Box in das Format [x_min, y_min, Breite, Höhe]
            box = [x_min, y_min, x_max - x_min, y_max - y_min]
            detections.append(box)

    # Verfolgt bestehende Objekte weiter, falls sie sichtbar sind
    new_trackers = []
    new_track_ids = []
    for tracker, track_id in zip(trackers, track_ids):
        success, box = tracker.update(frame)
        if success:
            new_trackers.append(tracker)
            new_track_ids.append(track_id)

    # Neue Tracker erstellen für neue Erkennungen
    for detection in detections:
        new_tracker = create_tracker(frame, detection)
        new_trackers.append(new_tracker)
        new_track_ids.append(next_track_id)
        next_track_id += 1

    # Aktualisiere die Tracker und IDs
    return new_trackers, new_track_ids, recognized_texts

# Hauptfunktion zur Kamerasteuerung
def camera_stream():
    cap = cv2.VideoCapture(0)  # Öffne die Webcam

    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Konnte das Kamerabild nicht lesen!")
            break

        global trackers, track_ids
        trackers, track_ids, recognized_texts = process_frame(frame)

        # Zeichne Rahmen und Tracking-IDs um die getrackten Flaschen
        for i, (tracker, track_id) in enumerate(zip(trackers, track_ids)):
            success, box = tracker.update(frame)
            if success:
                x_min, y_min, width, height = [int(v) for v in box]
                x_max = x_min + width
                y_max = y_min + height

                # Zeichne den Rahmen um die Flasche
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # Füge die Trackingnummer und den erkannten Text oberhalb des Rahmens hinzu
                text = recognized_texts[i] if i < len(recognized_texts) else "No Text"
                text_position = (x_min, y_min - 10 if y_min - 10 > 10 else y_min + 20)
                cv2.putText(frame, f"ID: {track_id} - {text.strip()}", text_position,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Frame im Fenster anzeigen
        cv2.imshow('Live Kamera Feed - Flaschen mit Tracking', frame)

        # Mit "q" die Kamera beenden
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kamera freigeben und Fenster schließen
    cap.release()
    cv2.destroyAllWindows()

# Starte die Kamera
if __name__ == "__main__":
    camera_stream()

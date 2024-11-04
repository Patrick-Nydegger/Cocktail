import cv2
from ultralytics import YOLO
import numpy as np
import pytesseract
from PIL import Image

# YOLOv8-Modell laden
yolo = YOLO("yolov8n.pt")  # Verwende das YOLOv8 Nano-Modell

# Pfad zur Tesseract-OCR-Installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Funktion zur Bildvorverarbeitung (Schärfen, Kontrast, Binarisierung)
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(gray, -1, sharpen_kernel)
    contrast = cv2.equalizeHist(sharpened)
    _, binary = cv2.threshold(contrast, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary

# Funktion zur Texterkennung mit OCR
def ocr_recognition(crop_img, lang='eng'):
    try:
        preprocessed_img = preprocess_image(crop_img)
        pil_img = Image.fromarray(preprocessed_img)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(pil_img, config=custom_config, lang=lang)
        return text
    except Exception as e:
        print(f"Fehler bei der Texterkennung: {e}")
        return None

# Schwellwert für die minimale Distanz zwischen Trackern
MIN_DISTANCE = 50  # Pixel
CONFIDENCE_THRESHOLD = 0.3  # Mindestvertrauensschwelle

# Funktion, um den Mittelpunkt einer Bounding Box zu berechnen
def get_center(bbox):
    x_min, y_min, w, h = bbox
    center_x = x_min + w / 2
    center_y = y_min + h / 2
    return np.array([center_x, center_y])

# Kamera öffnen
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden!")
    exit()

# Variablen für Tracker und Archivierung
trackers = []  # Aktuelle Tracker
tracker_labels = []  # Labels für aktive Tracker
tracker_ocr_lists = []  # Erkannte OCR-Texte für aktive Tracker

bottle_instances = {}  # Archiv für alle erkannten Flaschen
next_label_id = 1  # Fortlaufender Zähler für eindeutige Labels

while True:
    ret, frame = cap.read()
    if not ret:
        print("Konnte das Kamerabild nicht lesen!")
        break

    # YOLO Objekterkennung
    results = yolo(frame)

    # YOLO-Ergebnisse verarbeiten und neue Tracker hinzufügen
    for result in results[0].boxes:
        class_id = int(result.cls.cpu().numpy())
        confidence = float(result.conf.cpu().numpy())

        if class_id == 39 and confidence > 0.7:  # Nur Flaschen erkennen
            x_min, y_min, x_max, y_max = result.xyxy[0].cpu().numpy().astype(int)
            bbox = (x_min, y_min, x_max - x_min, y_max - y_min)

            # Berechne den Mittelpunkt der aktuellen Bounding Box
            new_center = get_center(bbox)

            found_existing_tracker = False
            for tracker in trackers:
                success, tracked_bbox = tracker.update(frame)
                if success:
                    tracked_center = get_center(tracked_bbox)
                    distance = np.linalg.norm(new_center - tracked_center)

                    if distance < MIN_DISTANCE:
                        found_existing_tracker = True
                        break

            if not found_existing_tracker:
                tracker = cv2.TrackerCSRT_create()
                trackers.append(tracker)
                tracker.init(frame, bbox)
                new_label = f"bottle {next_label_id}"  # Eindeutiges Label
                next_label_id += 1
                tracker_labels.append(new_label)
                tracker_ocr_lists.append([])

    # Tracke alle Objekte und überprüfe auf Erfolgsrückgabe
    new_trackers = []
    new_labels = []
    new_ocr_lists = []
    bboxes = []

    for i, tracker in enumerate(trackers):
        success, box = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            bboxes.append((x, y, w, h))

            tracked_frame = frame[y:y + h, x:x + w]

            # OCR auf den aktuellen Bildausschnitt anwenden
            recognized_text = ocr_recognition(tracked_frame)
            if recognized_text:
                tracker_ocr_lists[i].append(recognized_text)

            # Zeichne den Rahmen um die Flasche
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 4)
            label = tracker_labels[i]
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            new_trackers.append(tracker)
            new_labels.append(tracker_labels[i])
            new_ocr_lists.append(tracker_ocr_lists[i])

        else:
            # Wenn der Tracker nicht mehr erfolgreich ist, in das Archiv verschieben
            if tracker_labels[i] not in bottle_instances:
                bottle_instances[tracker_labels[i]] = tracker_ocr_lists[i]
                print(f"Tracker {tracker_labels[i]} archiviert mit Texten: {tracker_ocr_lists[i]}")

    # Aktualisiere die Tracker-, Label- und OCR-Listen
    trackers = new_trackers
    tracker_labels = new_labels
    tracker_ocr_lists = new_ocr_lists

    # Frame mit gezeichneten Elementen im Fenster anzeigen
    cv2.imshow('Kamera Feed - Flaschen Tracking mit OCR', frame)

    # Beenden, wenn "q" gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Archiviere auch alle noch aktiven Tracker, die noch im Bild sind
        for i in range(len(trackers)):
            if tracker_labels[i] not in bottle_instances:
                bottle_instances[tracker_labels[i]] = tracker_ocr_lists[i]
                print(f"Aktiver Tracker {tracker_labels[i]} archiviert mit Texten: {tracker_ocr_lists[i]}")

        # Gebe alle archivierten Flaschen und ihre Texte aus
        print("Archivierte Flaschen und erkannte Texte:")
        for label, ocr_list in bottle_instances.items():
            print(f"Flasche: {label}")
            print("Erkannte Texte:")
            for text in ocr_list:
                print(text)
        break

# Kamera freigeben und Fenster schließen
cap.release()
cv2.destroyAllWindows()

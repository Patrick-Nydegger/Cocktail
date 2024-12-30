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
    # Graustufen
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Schärfen
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(gray, -1, sharpen_kernel)

    # Kontrastanpassung (Histogramm-Ausgleich)
    contrast = cv2.equalizeHist(sharpened)

    # Binarisierung (Schwellenwert)
    _, binary = cv2.threshold(contrast, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return binary


# Funktion zur Texterkennung mit OCR
def ocr_recognition(crop_img, lang='eng'):
    try:
        # Bild vorverarbeiten
        preprocessed_img = preprocess_image(crop_img)

        # In PIL-Format umwandeln
        pil_img = Image.fromarray(preprocessed_img)

        # OCR ausführen
        custom_config = r'--oem 3 --psm 6'  # OCR-Engine-Modus und Seitensegmentierung anpassen
        text = pytesseract.image_to_string(pil_img, config=custom_config, lang=lang)

        return text
    except Exception as e:
        print(f"Fehler bei der Texterkennung: {e}")
        return None


# Liste von Trackern, zugehörigen Bounding Boxes und erkannte OCR-Textlisten
trackers = []
tracker_labels = []
tracker_ocr_lists = []  # Neue Liste für die erkannten Texte pro Tracker

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
    overlap_y_max = max(x2_max, y2_max)
    overlap_x_max = min(x1_max, x2_max)

    # Berechne die Fläche der überlappenden Box
    overlap_w = max(0, overlap_x_max - overlap_x_min)
    overlap_h = max(0, overlap_y_max - overlap_y_min)

    overlap_area = overlap_w * overlap_h
    area_box1 = w1 * h1
    area_box2 = w2 * h2

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
                tracker = cv2.TrackerCSRT_create()  # Oder ein anderer OpenCV-Tracker
                trackers.append(tracker)
                tracker.init(frame, bbox)
                tracker_labels.append(f"Flasche {len(trackers)}")
                tracker_ocr_lists.append([])  # Neue leere Liste für diesen Tracker

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
                tracker_ocr_lists[i].append(recognized_text)  # Text zur Liste hinzufügen

            # Text einfügen
            label = tracker_labels[i]
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Behalte den Tracker nur bei, wenn das Tracking erfolgreich ist
            new_trackers.append(tracker)
            new_labels.append(tracker_labels[i])
            new_ocr_lists.append(tracker_ocr_lists[i])

    # Vergleiche Bounding Boxes, um den größeren zu löschen, wenn er im kleineren liegt
    to_remove = set()
    for i in range(len(bboxes)):
        for j in range(i + 1, len(bboxes)):
            overlap = bbox_overlap(bboxes[i], bboxes[j])
            if overlap > 0.6:
                area_i = bboxes[i][2] * bboxes[i][3]
                area_j = bboxes[j][2] * bboxes[j][3]
                if area_i > area_j:
                    to_remove.add(i)
                else:
                    to_remove.add(j)

    final_trackers = []
    final_labels = []
    final_ocr_lists = []
    for idx, (tracker, label, ocr_list) in enumerate(zip(new_trackers, new_labels, new_ocr_lists)):
        if idx not in to_remove:
            final_trackers.append(tracker)
            final_labels.append(label)
            final_ocr_lists.append(ocr_list)
            (x, y, w, h) = [int(v) for v in bboxes[idx]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 4)

    # Aktualisiere die Tracker-, Label- und OCR-Listen
    trackers = final_trackers
    tracker_labels = final_labels
    tracker_ocr_lists = final_ocr_lists

    # Frame mit gezeichneten Elementen im Fenster anzeigen
    cv2.imshow('Kamera Feed - Flaschen Tracking mit OCR', frame)

    # Beenden, wenn "q" gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        for i in final_labels:
            print(label)
            print(ocr_list)

        print(tracker_ocr_lists)

        for i in tracker_ocr_lists:
            print(ocr_list)
        break

# Kamera freigeben und Fenster schließen
cap.release()
cv2.destroyAllWindows()

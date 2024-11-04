import cv2
from ultralytics import YOLO
import pytesseract
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# YOLOv8-Modell laden
yolo = YOLO("yolov8n.pt")

# Funktion zur Texterkennung mit OCR
def ocr_recognition(crop_img):
    pil_img = Image.fromarray(crop_img)
    text = pytesseract.image_to_string(pil_img)
    return text

# Funktion zur Verarbeitung des Kamerastreams
def process_frame(frame):
    # YOLO Objekterkennung durchführen
    results = yolo(frame)

    object_boxes = []
    recognized_texts = []

    # Für jede erkannte Box ein Bildausschnitt und die Koordinaten speichern
    for result in results[0].boxes:
        x_min, y_min, x_max, y_max = result.xyxy[0].numpy()  # Extrahiere Koordinaten
        confidence = result.conf.numpy()  # Vertraulichkeit des Detektors
        class_id = result.cls.numpy()  # Klassen-ID des erkannten Objekts

        # Überprüfen, ob das erkannte Objekt eine Flasche ist (class_id = 39 für COCO-Dataset)
        if class_id == 39:  # 39 entspricht der Klasse "bottle" im COCO-Dataset
            # Bildausschnitt des erkannten Objekts
            crop_img = frame[int(y_min):int(y_max), int(x_min):int(x_max)]

            # Texterkennung auf dem Bildausschnitt
            text = ocr_recognition(crop_img)

            # Speichere die Box-Koordinaten und den erkannten Text
            object_boxes.append((int(x_min), int(y_min), int(x_max), int(y_max)))
            recognized_texts.append(text)

    return object_boxes, recognized_texts

# Hauptfunktion zur Kamerasteuerung
def camera_stream():
    cap = cv2.VideoCapture(0)  # Öffne die Webcam

    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden!")
        return

    while True:
        # Frame von der Kamera lesen
        ret, frame = cap.read()
        if not ret:
            print("Konnte das Kamerabild nicht lesen!")
            break

        # YOLO und OCR auf dem aktuellen Frame anwenden
        object_boxes, recognized_texts = process_frame(frame)

        # Zeichne Rahmen um die erkannten Flaschen und füge Texte hinzu
        for i, (box, text) in enumerate(zip(object_boxes, recognized_texts)):
            x_min, y_min, x_max, y_max = box

            # Zeichne den Rahmen um die Flasche
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Füge den erkannten Text oberhalb des Rahmens hinzu
            cv2.putText(frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Frame im Fenster anzeigen
        cv2.imshow('Live Kamera Feed', frame)

        # Mit "q" die Kamera beenden
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kamera freigeben und Fenster schließen
    cap.release()
    cv2.destroyAllWindows()

# Starte die Kamera
if __name__ == "__main__":
    camera_stream()

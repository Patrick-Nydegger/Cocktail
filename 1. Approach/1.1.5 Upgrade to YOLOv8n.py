import cv2
from ultralytics import YOLO
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import numpy as np

# YOLOv8-Modell laden
yolo = YOLO("yolov8n.pt")  # YOLOv8-Modell ('n' steht für nano, es gibt auch 's', 'm', 'l', 'x')

# Funktion zur Texterkennung mit OCR
def ocr_recognition(crop_img):
    pil_img = Image.fromarray(crop_img)
    text = pytesseract.image_to_string(pil_img)
    return text

# Funktion zur Verarbeitung des Kamerastreams
def process_frame(frame):
    # YOLO Objekterkennung durchführen
    results = yolo(frame)

    object_crops = []
    recognized_texts = []

    # Für jede erkannte Box ein Bildausschnitt erstellen
    for result in results[0].boxes:
        x_min, y_min, x_max, y_max = result.xyxy[0].numpy()  # Extrahiere Koordinaten
        confidence = result.conf.numpy()  # Vertraulichkeit des Detektors
        class_id = result.cls.numpy()  # Klassen-ID des erkannten Objekts

        # Bildausschnitt des erkannten Objekts
        crop_img = frame[int(y_min):int(y_max), int(x_min):int(x_max)]
        object_crops.append(crop_img)

        # Texterkennung auf dem Bildausschnitt
        text = ocr_recognition(crop_img)
        recognized_texts.append(text)

    return object_crops, recognized_texts

# Hauptfunktion zur Kamerasteuerung
def camera_stream():
    cap = cv2.VideoCapture(0)  # Öffne die Webcam (0 steht für die Standardkamera)

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
        object_crops, recognized_texts = process_frame(frame)

        # Ergebnisse anzeigen (die erkannten Objekte und deren Texte)
        for i, text in enumerate(recognized_texts):
            print(f"Objekt {i + 1}: {text}")

        # Frame im Fenster anzeigen (optional)
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

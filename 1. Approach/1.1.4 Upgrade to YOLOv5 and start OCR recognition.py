import cv2
from yolov5 import YOLOv5
import pytesseract
from PIL import Image
import numpy as np

# YOLO-Modell laden
yolo = YOLOv5("yolov5s.pt", device="cpu")  # YOLOv5-Modell (kann auch 'gpu' sein, falls GPU vorhanden)


# Funktion zur Texterkennung mit OCR
def ocr_recognition(crop_img):
    pil_img = Image.fromarray(crop_img)
    text = pytesseract.image_to_string(pil_img)
    return text


# Funktion zur Verarbeitung des Kamerastreams
def process_frame(frame):
    # YOLO Objekterkennung durchführen
    results = yolo.predict(frame)

    object_crops = []
    recognized_texts = []

    # Für jede erkannte Box ein Bildausschnitt erstellen
    for detection in results.xyxy[0]:
        x_min, y_min, x_max, y_max, confidence, class_id = detection
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

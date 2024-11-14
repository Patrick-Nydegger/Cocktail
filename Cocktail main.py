#Hier wird das Hauptmenu und die Applikationssteuerung Programmiert



"""

import cv2
import numpy as np
from ultralytics import YOLO

# Lade das Modell
model = YOLO('best.pt')

# Öffne die Kamera
cap = cv2.VideoCapture(0)

while True:
    # Lies ein Frame
    ret, frame = cap.read()
    if not ret:
        print("Frame konnte nicht gelesen werden")
        break

    # Nutze das Modell, um das Bild zu verarbeiten
    results = model(frame)

    # Verarbeite die Ergebnisse, falls vorhanden
    if results and len(results) > 0:
        for detection in results[0].boxes:  # Zugriff auf das erste Bild und seine Detections
            # Extrahiere die Bounding-Box-Koordinaten und Klasse
            x_min, y_min, x_max, y_max = map(int, detection.xyxy[0])  # Bounding-Box-Koordinaten
            confidence = detection.conf[0]  # Vertrauen
            class_id = int(detection.cls[0])  # Klassen-ID

            # Zeichne das Rechteck um das erkannte Objekt
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            # Füge den Klassennamen und die Konfidenz hinzu
            label = f"{results[0].names[class_id]}: {confidence:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Zeige die Ergebnisse
    cv2.imshow('YOLOv8 Detection', frame)

    # Beende mit 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Gib die Kamera frei
cap.release()
cv2.destroyAllWindows()

"""

import cv2
from ultralytics import YOLO

# YOLOv8-Modell laden
yolo = YOLO("yolov8n.pt")  # Verwende das YOLOv8 Nano-Modell

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

    # Gehe durch alle erkannten Objekte
    for result in results[0].boxes:
        class_id = int(result.cls.cpu().numpy())  # Klassen-ID (von Tensor in NumPy konvertieren)
        confidence = float(result.conf.cpu().numpy())  # Zuverlässigkeit (von Tensor in NumPy konvertieren)

        if class_id == 39 and confidence > 0.3:  # Nur Flaschen erkennen
            # Koordinaten der Bounding Box (von Tensor in NumPy konvertieren)
            x_min, y_min, x_max, y_max = result.xyxy[0].cpu().numpy().astype(int)

            # Zeichne den Rahmen um die Flasche
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 255, 255), 4)

            # ID und Text einfügen
            label = f"Flasche: {confidence:.2f}"  # Füge die Konfidenz als Text hinzu
            cv2.putText(frame, label, (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Frame mit gezeichneten Elementen im Fenster anzeigen
    cv2.imshow('Kamera Feed - Flaschen Tracking', frame)

    # Beenden, wenn "q" gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera freigeben und Fenster schließen
cap.release()
cv2.destroyAllWindows()

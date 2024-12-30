import cv2
import numpy as np

# Laden des vortrainierten YOLO-Modells (hier YOLOv3 als Beispiel)
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Objektklassen laden
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Kamera starten oder ein Bild laden
cap = cv2.VideoCapture(0)

while True:
    # Frame von der Kamera lesen
    ret, frame = cap.read()

    if not ret:
        break

    height, width, channels = frame.shape

    # YOLO Eingangsblob vorbereiten
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Objekterkennung mit YOLO
    outputs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Ergebnisse der Erkennung verarbeiten
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Nur wenn das Objekt vertrauenswürdig genug erkannt wurde
            if confidence > 0.5 and classes[class_id] == 'bottle':  # Hier wird nach Flaschen gesucht
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-Maximum Suppression anwenden, um überlappende Boxen zu entfernen
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            roi = frame[y:y + h, x:x + w]  # Region of Interest (Flaschenbereich)

            # GrabCut für präzise Segmentierung der Flasche
            mask = np.zeros(roi.shape[:2], np.uint8)
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            rect = (10, 10, w - 10, h - 10)  # Rechteck innerhalb der Bounding Box für GrabCut
            cv2.grabCut(roi, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

            # Maske verfeinern
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            roi = roi * mask2[:, :, np.newaxis]

            # Bild in Graustufen umwandeln
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

            # Setze das farbige Objekt in das Graustufenbild zurück
            gray_frame[y:y + h, x:x + w] = roi

            # Zeige das Ergebnis
            cv2.imshow('Farbiges Objekt mit grauem Hintergrund', gray_frame)

    # Beenden, wenn 'q' gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera freigeben und Fenster schließen
cap.release()
cv2.destroyAllWindows()

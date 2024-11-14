import cv2
import numpy as np

# Lade YOLO
net = cv2.dnn.readNet(r'C:\Users\padin\PycharmProjects\cocktAIl\.venv\yolov3.weights', r'C:\Users\padin\PycharmProjects\cocktAIl\.venv\yolov3.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Lade die Klassen
with open(r'C:\Users\padin\PycharmProjects\cocktAIl\.venv\coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Öffne die Kamera
cap = cv2.VideoCapture(0)

while True:
    # Lies ein Bild von der Kamera
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Bereite das Bild für YOLO vor
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Informationen über die erkannten Objekte sammeln
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]  # Scores ab Index 5 extrahieren
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.3 and classes[class_id] == 'bottle':
                # Objekt erkannt
                center_x = int(detection[0] * width)  # X-Koordinate
                center_y = int(detection[1] * height)  # Y-Koordinate
                w = int(detection[2] * width)  # Breite der Box
                h = int(detection[3] * height)  # Höhe der Box
                x = int(center_x - w / 2)  # Berechne linke obere Ecke der Box
                y = int(center_y - h / 2)  # Berechne obere Ecke der Box
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)


                # Non-max suppression anwenden
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Zeichne Rechtecke um die erkannten Flaschen
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = (255, 255, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 6)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Zeige das Bild mit den markierten Flaschen
    cv2.imshow('Flaschen erkannt', frame)

    # Beende die Schleife, wenn 'q' gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

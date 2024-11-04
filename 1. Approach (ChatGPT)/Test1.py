import cv2

# Lade das Bild
image = cv2.imread('C:\\Users\\padin\\Pictures\\Camera Roll\\WIN_20240925_16_07_44_Pro.jpg')

# Lade das vortrainierte Modell für die Gesichtserkennung
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Konvertiere das Bild in Graustufen
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Erkenne Gesichter im Bild
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Zeichne Rechtecke um die erkannten Gesichter
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Zeige das Bild mit den markierten Gesichtern
cv2.imshow('Gesichter erkannt', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

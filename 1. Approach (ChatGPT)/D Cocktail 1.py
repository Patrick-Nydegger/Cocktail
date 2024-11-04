import cv2
import os
from ultralytics import YOLO
import numpy as np
import pytesseract
from PIL import Image


class CVision():
    def __init__(self):
        pass

    def yolo(self):

        """YOLOv8n implementierung"""

        return bottle
        pass

    def tracking(self):
        return track_nr
        pass



class Ocr(bottle,track_nr):
    def __init__(self):
        self.bottel = CVision.yolo(bottle)
        pass

    def preprocess(self,bottle):
        pass

    def ocr(self,bottle):
        return text
        pass

class Collect(bottle,text):
    def __init__(self):
        self.bottel = CVision.yolo(bottle)
        self.text = Ocr.ocr(text)
        self.track_nr = CVision.tracking(track_nr)

    #Sammeln der einzelnen Texte zu der Liste der Bottles
    def collect(self):

        if self.text in track_nr:
            # Ergänzen der Liste mit dem neuen Eintrag
            bottles[track_nr].append(self.text)
        else:
            # Falls der Key nicht existiert, erstelle eine neue Liste mit dem neuen Eintrag
            bottles[track_nr] = [self.text]
        pass

class Categorize(bottles):
    def __init__(self):
        self.bottles = Collect.collect(bottles)

    def categorize(bottles):

        """vergleich von der liste mit texten der
        jeweiligen track_nr mit den verfügbaren klassen"""

        pass

class Export

if __name__ == "__main__":
    bottles = {} #Erstellung des Dictionarys von allen Bottles und den zugehörigen Listen mit Texten

    # Kamera öffnen
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden!")
        exit()

    while True:
        bottles = Collect().collect(bottles)


    """implementierung des loops"""

    # Beenden, wenn "q" gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Beende das Programm und gebe alle archivierten Flaschen und ihre Texte aus
        print("Archivierte Flaschen und erkannte Texte:")
        for i in bottles.values():
            print(i)


        for i in bottles.items():
            print(f"Flasche: {track_nr}")
            print("Erkannte Texte:")
            for text in track_nr:
                print(text)

            break

# Kamera freigeben und Fenster schließen
cap.release()
cv2.destroyAllWindows()

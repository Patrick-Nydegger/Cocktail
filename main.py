import cv2
from yolo_bottle_detector import BottleDetector
from bottle_classifier import BottleClassifier
from ocr_recognition import OCRRecognition
from draw_utils import draw_object


def main():
    bottle_detector = BottleDetector()
    bottle_classifier = BottleClassifier('best.pt')
    ocr_recognizer = OCRRecognition(language='eng')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame konnte nicht gelesen werden")
            break


        # Flaschen erkennen
        bottle_detections = bottle_detector.detect_bottles(frame)
        frame = draw_object(frame, bottle_detections, color=(0, 255, 0), label_prefix="Bottle")


        # Flaschenklassifizierung mit optimiertem YOLO-Modell
        bottle_classifications = bottle_classifier.classify_bottles(frame)
        frame = draw_object(frame, bottle_classifications, color=(255, 0, 0), label_prefix="Class")


        # Überprüfe, ob eine Klassifizierung ungenau ist
        unsatisfactory = any(confidence < 0.9 for _, _, _, _, confidence, _, _ in bottle_classifications)





        # Starte OCR, falls unzureichende Klassifizierung
        if unsatisfactory:

            text = ocr_recognizer.extract_text(frame)
            print("OCR-Erkannter Text:", text)



        # Zeige die Ergebnisse
        cv2.imshow('Bottle Detection and OCR', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

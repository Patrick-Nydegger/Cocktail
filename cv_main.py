import cv2
from yolo_bottle_detector import BottleDetector
from bottle_classifier import BottleClassifier
from ocr_recognition import OCRRecognition
from draw_utils import draw_object


# Erstellung der Liste für erkannte Flaschen
available_ingredients = []

# Funktion für management von CV-Modul
def cv_main():
    bottle_detector = BottleDetector()
    bottle_classifier = BottleClassifier('best.pt')
    ocr_recognizer = OCRRecognition(language='eng')

    cap = cv2.VideoCapture(0)

    #Einstellen der Confidence, die verlangt wird, falls ein lable durch bottle_classifications erkannt wird
    confidence_level =0.9
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame konnte nicht gelesen werden")
            break


        # Flaschen erkennen
        bottle_detections = bottle_detector.detect_bottles(frame)
        frame = draw_object(frame, bottle_detections, color=(0, 255, 0), label_prefix="Bottle")
        bottle_frame = frame

        # Flaschenklassifizierung mit optimiertem YOLO-Modell
        bottle_classification = bottle_classifier.classify_bottles(frame)
        frame = draw_object(frame, bottle_classification, color=(255, 0, 0), label_prefix="Class")


        # Überprüfe, ob eine Klassifizierung ungenau ist
        unsatisfactory = any(confidence < confidence_level  for _, _, _, _, confidence, _, _ in bottle_classification)

        # Fülle available_ingredients-Liste mit zufriedenstellenden Klassennamen
        for x_min, y_min, x_max, y_max, confidence, class_id, class_name in bottle_classification:
            if confidence >= confidence_level:
                available_ingredients.append(class_name)

        # Starte OCR, falls unzureichende Klassifizierung
        if unsatisfactory:

            text = ocr_recognizer.extract_text(bottle_frame)
            print("OCR-Erkannter Text:", text)




        # Zeige die Ergebnisse
        cv2.imshow('Bottle Detection and OCR', frame)

        if cv2.waitKey(1) == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
    print(available_ingredients)


if __name__ == "__main__":
    cv_main()

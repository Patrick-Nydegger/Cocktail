import textwrap

import cv2

from db_interaktion import find_recipes_with_ingredients
from normalize_classes import normalize_classes
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

    # Einstellen der Confidence, die verlangt wird, falls ein Label durch bottle_classifications erkannt wird
    confidence_level = 0.9

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame konnte nicht gelesen werden")
            break

        # Flaschenklassifizierung mit optimiertem YOLO-Modell
        bottle_classification = bottle_classifier.classify_bottles(frame)
        frame = draw_object(frame, bottle_classification, color=(255, 0, 0), label_prefix="Class")

        # Debugging der Klassifikationen
        if not bottle_classification:
            print("Keine Klassifikation erkannt!")
        else:
            print(f"Klassifikationen gefunden: {bottle_classification}")

        # Erkannt Klassen in der Konsole ausgeben
        recognized_classes = []
        for x_min, y_min, x_max, y_max, confidence, class_id, class_name in bottle_classification:
            print(f"Gefunden: {class_name} mit Confidence: {confidence:.2f}")  # Debugging der Confidence-Werte
            if confidence >= confidence_level:
                #available_ingredients.append(class_name)

                recognized_classes.append(class_name)

        # Zeige die erkannten Klassen nur einmal pro Frame
        if recognized_classes:
            print(f"Erkannte Klassen: {', '.join(set(recognized_classes))}")
        else:
            print("Keine Klassen erkannt")

        # Zeige die Ergebnisse
        cv2.imshow('Bottle Detection', frame)


        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    #print("Alle erkannte Klassen:", available_ingredients)

    recognized_classes = [] # "gin","cointrau","prosecco", "Orange Juice", "Lime"]
    available_essentials = input("Enter your available essentials (like: lemon juice, sugar,...) \n ")
    #recognized_classes.append(available_essentials)

    # Eingabe splitten und zur Liste hinzufügen
    recognized_classes.extend(available_essentials.split(","))  # Split basierend auf Kommas

    # Liste bereinigen: Whitespace entfernen und Normalisierung anwenden
    recognized_classes = [item.strip() for item in recognized_classes if
                          item.strip()]  # Entfernt Leerzeichen und leere Einträge

    # Normalisierte Klassen erzeugen
    normalized_classes = normalize_classes(recognized_classes)

    recipes = find_recipes_with_ingredients(normalized_classes)

    print("Gefundene Rezepte:")
    # for recipe in recipes:
    # print(f"{recipe['name']} \n - Zutaten: {', '.join(recipe['ingredients'])} \n - Methode: {recipe['method']} \n {150*'='}")

    for recipe in recipes:
        print(f"{recipe['name']}\nZutaten:")
        for ingredient in recipe['ingredients']:
            print(f"   {ingredient}")

        # Methode formatieren und umbrechen
        wrapped_method = textwrap.fill(recipe['method'], width=80)
        print(f"Methode:\n{wrapped_method}\n{'=' * 80}")




if __name__ == "__main__":
    cv_main()

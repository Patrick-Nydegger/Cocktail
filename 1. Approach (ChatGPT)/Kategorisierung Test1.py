import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Liste von Marken und Kategorien
drink_categories = {
    "jack daniels": "Whiskey",
    "jameson": "Whiskey",
    "absolut": "Vodka",
    "grey goose": "Vodka",
    "heineken": "Bier",
    "corona": "Bier",
    "red bull": "Energy Drink"
    # Weitere Marken und Kategorien hinzufügen...
}

# Schwellenwert für die Ähnlichkeit (0-100)
SIMILARITY_THRESHOLD = 80


# Funktion zur Kategorisierung mit Fuzzy-Suche
def categorize_drinks(text):
    nlp = spacy.load("en_core_web_sm")

    # Text durch das NLP-Modell verarbeiten
    doc = nlp(text)

    found_categories = []

    # Jede erkannte Entität mit drink_categories abgleichen
    for ent in doc.ents:
        entity_text = ent.text.lower()  # Kleinschreibung für Vergleich

        # Verwende fuzzywuzzy, um ähnliche Begriffe zu finden
        best_match, similarity = process.extractOne(entity_text, drink_categories.keys(), scorer=fuzz.token_sort_ratio)

        # Wenn die Ähnlichkeit über dem Schwellenwert liegt, die Kategorie speichern
        if similarity >= SIMILARITY_THRESHOLD:
            found_categories.append(drink_categories[best_match])
            print(f"'{entity_text}' wurde als '{best_match}' erkannt (Ähnlichkeit: {similarity}%)")

    # Ausgabe der gefundenen Kategorien
    if found_categories:
        print(f"Gefundene Kategorien: {', '.join(found_categories)}")
    else:
        print("Keine passenden Getränkekategorien gefunden.")


# Eingabeaufforderung für den Benutzer
text = input("Enter label or drink name: ")
categorize_drinks(text)

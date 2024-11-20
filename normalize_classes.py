def normalize_classes(recognized_classes):
    """
    Normalisiert erkannte Klassen durch Entfernen von Duplikaten, Zuordnung zu standardisierten Namen
    und Umwandlung aller Werte in Kleinbuchstaben.

    Args:
        recognized_classes (list): Liste erkannter Klassen oder Marken.

    Returns:
        set: Menge der normalisierten Klassen (in Kleinbuchstaben).
    """
    # Duplikate entfernen, indem die Eingabe in ein Set umgewandelt wird
    unique_classes = set(recognized_classes)

    # Mappings von standardisierten Namen zu möglichen Schreibweisen/Markennamen
    normalization_mapping = {
        "gin": ["gin", "giin", "ggin", "ggiinn", "giin", "giinn", "ginn", "tschinn", "tschin",
                "bombay sapphire", "tanqueray", "hendricks", "beefeater",
                "hendrick's", "gordon's", "plymouth", "brooklyn gin", "seagrams",
                "monkey 47", "aviation gin", "sipsmith", "the botanist",
                "roku gin", "whitley neill", "gin mare", "nolet's", "hayman's",
                "caorunn", "scapegrace", "tanqueray ten", "bobby's gin",
                "silent pool", "four pillars", "the london no. 1", "stray dog",
                "edinburgh gin", "oxley", "barr hill", "st. george", "warner's gin"],

        "whiskey": ["whiskey", "whiskee", "whiski", "wiskey", "wisky", "wiskee",
                    "wiskie", "wwhiskey", "wwhisky", "wisskey", "wiski", "whysky",
                    "wyskey", "viskey", "vwhisky", "whyski" "whiskey", "whisky",
                    "scotch", "bourbon", "rye whiskey", "single malt",
                    "blended whisky", "cask strength", "malt whisky", "blended scotch",
                    "jack daniels", "red label", "jameson", "chivas regal"]


    }

    # Liste zum Speichern der normalisierten Klassen
    normalized_classes = []

    # Jede Klasse prüfen und mit den Mappings abgleichen
    for item in unique_classes:
        matched = False
        for standard_name, aliases in normalization_mapping.items():
            if item.lower() in aliases or item.lower() == standard_name:
                normalized_classes.append(standard_name.lower())  # Standardnamen in Kleinbuchstaben hinzufügen
                matched = True
                break
        # Falls keine Übereinstimmung, das Original (klein geschrieben) hinzufügen
        if not matched:
            normalized_classes.append(item.lower())

    # Duplikate aus der normalisierten Liste entfernen und als Set zurückgeben
    return set(normalized_classes)

"""
# Beispielaufruf
recognized_classes = [
    "Bombay Sapphire",
    "Tanqueray",
    "Jack Daniels",
    "Unknown Brand",
    "Jameson",
    "Gin"
]

result = normalize_classes(recognized_classes)
print(result)
"""
"""
This file captures many user inputs, which results in more items being recognized in the database. The file will become
even more important when an OCR implementation is carried out. Normalized recognized classes by removing duplicates,
assigning standardized names, and converting all values to
lowercase.
"""


def normalize_classes(recognized_classes):
    # Remove duplicates by converting the input into a set.
    unique_classes = set(recognized_classes)

    # Mappings of standardized names to possible spellings/brand names.
    normalization_mapping = {
        "gin": ["gin", "giin", "ggin", "ggiinn", "giin", "giinn", "ginn", "tschinn", "tschin",
                "bombay sapphire", "tanqueray", "hendricks", "beefeater",
                "hendrick's", "gordon's", "gordon", "plymouth", "brooklyn gin", "seagrams",
                "monkey 47", "aviation gin", "sipsmith", "the botanist",
                "roku gin", "whitley neill", "gin mare", "nolet's", "hayman's",
                "caorunn", "scapegrace", "tanqueray ten", "bobby's gin",
                "silent pool", "four pillars", "the london no. 1", "stray dog",
                "edinburgh gin", "oxley", "barr hill", "st. george", "warner's gin"],

        "whiskey": ["jack daniels", "jack", "daniels", "whiskey", "whiskee", "whiski", "wiskey", "wisky", "wiskee",
                    "wiskie", "wwhiskey", "wwhisky", "wisskey", "wiski", "whysky",
                    "wyskey", "viskey", "vwhisky", "whyski" "whiskey", "whisky",
                    "scotch", "bourbon", "rye whiskey", "single malt",
                    "blended whisky", "cask strength", "malt whisky", "blended scotch",
                    "red label", "jameson", "chivas regal"],

        "vodka": ["vodka", "wodka", "voodka", "wwodka", "vodkaa", "vvodka", "vvodkaa", "vvodka",
                  "absolut", "smirnoff", "grey goose", "belvedere", "ciroc", "ketel one",
                  "tito's", "stolichnaya", "svedka", "skyy", "three olives", "chopin",
                  "zubrowka", "reyka", "luksusowa", "beluga", "crystal head", "finlandia",
                  "new amsterdam", "42 below", "frïs", "polar ice", "platinum 7x", "pravda",
                  "ivanabitch", "rain", "effen", "nemiroff", "moskovskaya", "karlsson's gold",
                  "soplica", "wyborowa", "parliament", "imperial collection", "wiborowa"],

        "campari": ["campari", "campairi", "camparee", "campare", "cammpari", "campari bitter",
                    "camparee bitter", "camparee aperitif", "campare"],

        "rum": ["rum", "rhum", "room", "ruhm", "rumm", "rohm", "rrum", "rrumm", "rohm",
                "bacardi", "captain morgan", "havana club", "myers's", "mount gay",
                "zaya", "ron zacapa", "el dorado", "appleton estate", "gosling's",
                "pyrat", "plantation", "don q", "kraken", "flor de caña", "barcelo",
                "dictador", "santa teresa", "sailor jerry", "blackwell", "bacardi carta blanca"],

        "martini": ["martini", "martine", "martinii", "martiny", "marrtini", "marrtinii",
                    "martini rosso", "martini bianco", "martini extra dry", "vermouth",
                    "noilly prat", "cinzano", "lillet blanc", "carpano", "dolin",
                    "martini gold", "martini royale", "martini fiero", "antica formula"]

    }

    # List to store the normalized classes.
    normalized_classes = []

    # Check each class and match it with the mappings.
    for item in unique_classes:
        matched = False
        for standard_name, aliases in normalization_mapping.items():
            if item.lower() in aliases or item.lower() == standard_name:
                normalized_classes.append(standard_name.lower())
                matched = True
                break
        # If no match, add the original (in lowercase)
        if not matched:
            normalized_classes.append(item.lower())

    # Remove duplicates from the normalized list and return it as a set.
    return set(normalized_classes)

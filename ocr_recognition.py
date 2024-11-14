import cv2
import pytesseract

class OCRRecognition:
    def __init__(self, language='eng'):
        self.language = language

    def extract_text(self, frame):
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #text = pytesseract.image_to_string(gray, lang=self.language)
        text= "Test hardcoded"
        return text #Ausgabe muss noch als liste erstellt werden

    #Diese funktion ist im moment noch auf tracking ausgelegt. sollte nur ein bild erkannnt werden, muss die lsitenfunktionen stakt vereinfacht werden.
    def compare_text(self, text):
        text = self.extract_text(self)

        from scipy.spatial.distance import cosine



        def OCR-classifier(target_list):
            whisky_keywords = [
                # Allgemeine Begriffe und Schreibweisen
                "whisky",
                "whiskey",
                "scotch",
                "bourbon",
                "rye whiskey",
                "single malt",
                "blended whisky",
                "cask strength",
                "malt whisky",
                "blended scotch",

                # Bekannte Marken und Varianten
                "johnnie walker",
                "jack daniel's",
                "jim beam",
                "glenfiddich",
                "macallan",
                "glenlivet",
                "ardbeg",
                "lagavulin",
                "laphroaig",
                "jameson",
                "bulleit",
                "wild turkey",
                "makers mark",
                "chivas regal",
                "talisker",
                "bushmills",
                "balvenie",
                "caol ila",
                "knob creek",
                "glenmorangie",
                "springbank",
                "redbreast",
                "yamazaki",
                "hakushu",
                "hibiki",
                "nikka",
                "tullamore dew",
                "canadian club",
                "crown royal",
                "paddy",

                # Herkunftsorte und andere Begriffe
                "scotland",
                "ireland",
                "tennessee",
                "kentucky",
                "islay",
                "speyside",
                "highlands",
                "lowlands",
                "campbeltown",
                "japan",
                "canada",
                "tennessee whiskey",
                "kentucky bourbon",
                "smoky",
                "peat",
                "oak cask"
            ]

            gin_keywords = [
                # Allgemeine Begriffe und Schreibweisen
                "gin",
                "dry gin",
                "london dry gin",
                "distilled gin",
                "old tom gin",
                "navy strength gin",
                "sloe gin",
                "botanical gin",
                "herbal gin",
                "pink gin",

                # Bekannte Marken und Varianten
                "tanqueray",
                "bombay sapphire",
                "beefeater",
                "hendrick's",
                "gordon's",
                "plymouth",
                "brooklyn gin",
                "seagrams",
                "monkey 47",
                "aviation gin",
                "sipsmith",
                "the botanist",
                "roku gin",
                "whitley neill",
                "gin mare",
                "nolet's",
                "hayman's",
                "caorunn",
                "scapegrace",
                "tanqueray ten",
                "bobby's gin",
                "silent pool",
                "four pillars",
                "the london no. 1",
                "stray dog",
                "edinburgh gin",
                "oxley",
                "barr hill",
                "st. george",
                "warner's gin",

                # Herkunftsorte und andere Begriffe
                "juniper",
                "botanicals",
                "england",
                "spain",
                "scotland",
                "genever",
                "netherlands",
                "citrus",
                "juniper berries",
                "herbal",
                "floral",
                "cucumber",
                "citrus peel",
                "london",
                "amsterdam",
                "small batch gin",
                "craft gin"
            ]

            rum_keywords = [
                # Allgemeine Begriffe und Schreibweisen
                "rum",
                "dark rum",
                "white rum",
                "aged rum",
                "spiced rum",
                "gold rum",
                "overproof rum",
                "light rum",
                "black rum",
                "cachaça",  # brasilianische Variante von Rum
                "ron",  # Spanische Bezeichnung

                # Bekannte Marken und Varianten (Bacardi im Fokus)
                "bacardi",
                "bacardi superior",
                "bacardi gold",
                "bacardi black",
                "bacardi carta blanca",
                "bacardi reserva",
                "bacardi 151",
                "bacardi spiced",
                "bacardi oakheart",
                "havana club",
                "captain morgan",
                "myers's rum",
                "appleton estate",
                "mount gay",
                "kraken",
                "don papa",
                "ron zacapa",
                "pyrat",
                "matusalem",
                "plantation",
                "el dorado",
                "gosling's",
                "flor de caña",
                "sailor jerry",
                "malibu",
                "bundaberg",
                "diplomatico",
                "angostura",
                "chairman's reserve",
                "bayou",
                "cockspur",

                # Herkunftsorte und weitere Begriffe
                "caribbean",
                "jamaica",
                "puerto rico",
                "cuba",
                "trinidad",
                "guyana",
                "barbados",
                "molasses",
                "sugarcane",
                "tropical",
                "demerara",
                "island rum",
                "rum punch",
                "aged in oak",
                "cuban rum"
            ]

            campari_keywords = [
                # Allgemeine Begriffe und Schreibweisen
                "campari",
                "bitter campari",
                "campari bitter",
                "campari liqueur",
                "aperitivo campari",
                "campari soda",
                "campari spritz",
                "campari negroni",
                "campari cocktail",
                "italian bitter",
                "campari red",

                # Varianten und Mischgetränke
                "campari orange",
                "campari tonic",
                "campari americano",
                "campari prosecco",
                "campari mojito",
                "campari mule",
                "campari martini",
                "campari with soda",
                "campari with orange",
                "campari mix",
                "campari rosso",
                "bitter rosso",

                # Cocktails und Drinks mit Campari
                "negroni",
                "americano",
                "spritz",
                "campari spritz",
                "garibaldi",
                "jungle bird",
                "bitter orange cocktail",
                "mi-to",
                "campari punch",
                "bittersweet cocktail",
                "old pal",
                "negroni sbagliato",
                "boulevardier",
                "campari sour",

                # Geschmacks- und Inhaltsbeschreibungen
                "herbal bitter",
                "citrus flavor",
                "aromatic bitters",
                "bitter orange",
                "herbal liqueur",
                "fruity bitter",
                "red liqueur",
                "aromatic herbs",
                "botanical flavor",

                # Marken und ähnliche Liköre
                "aperol",
                "cynar",
                "fernet",
                "luxardo bitter",
                "montenegro",
                "amaro",
                "italian aperitivo",
                "italian amaro",
                "aperitivo rosso",
                "italian vermouth"
            ]

            martini_keywords = [
                # Allgemeine Begriffe und Schreibweisen
                "martini",
                "martini rosso",
                "martini bianco",
                "martini extra dry",
                "martini rosato",
                "martini vermouth",
                "martini bitter",
                "martini d’oro",
                "martini & rossi",
                "martini prosecco",

                # Geschmacksrichtungen und Varianten
                "vermouth rosso",
                "vermouth bianco",
                "vermouth extra dry",
                "italian vermouth",
                "sweet vermouth",
                "dry vermouth",
                "aromatic vermouth",

                # Verwandte Begriffe und Geschmack
                "italian aperitif",
                "italian liqueur",
                "botanical blend",
                "herbal flavor",
                "spiced vermouth",
                "aromatic herbs",
                "bitter vermouth",
                "spiced aperitif",

                # Geografische und andere relevante Begriffe
                "piedmont vermouth",
                "italy",
                "torino",
                "turin vermouth",
            ]



        def find_most_similar_list(target_list, comparison_dict, similarity_threshold=0.9):
            """
            Vergleicht eine Ziel-Liste mit mehreren anderen Listen (als Dictionary) und findet die Liste mit der höchsten Ähnlichkeit.

            :param target_list: Die Liste, die verglichen werden soll.
            :param comparison_dict: Ein Dictionary, in dem der Key der Listenname und der Value die Liste selbst ist.
            :param similarity_threshold: Schwellenwert für den Kosinus-Similaritätswert, z. B. 0.9 für 90%.
            :return: Ein Tupel (Listenname, Ähnlichkeit) der Liste, die der Ziel-Liste am ähnlichsten ist,
                     oder (None, 0), falls keine Liste die Ähnlichkeitsschwelle erreicht.
            """
            highest_similarity = 0
            most_similar_name = None

            for name, comparison_list in comparison_dict.items():
                # Berechne den Kosinus-Abstand (1 - Kosinus-Ähnlichkeit)
                similarity = 1 - cosine(target_list, comparison_list)

                # Check if this similarity exceeds the current highest similarity and threshold
                if similarity > highest_similarity and similarity >= similarity_threshold:
                    highest_similarity = similarity
                    most_similar_name = name

            return most_similar_name, highest_similarity

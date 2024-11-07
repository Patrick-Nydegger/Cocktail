import cv2
import pytesseract

class OCRRecognition:
    def __init__(self, language='eng'):
        self.language = language

    def extract_text(self, frame):
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #text = pytesseract.image_to_string(gray, lang=self.language)
        text= "Test hardcoded"
        return text

"""
This file will contain the OCR implementation. The file was created using the first approach, but due to the
limited time, it was not used in the second approach. It is still under development.
"""


import cv2
import pytesseract

class OCRRecognition:
    def __init__(self, language='eng'):
        self.language = language

    def extract_text(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang=self.language)
        return text #The output still needs to be created as a list

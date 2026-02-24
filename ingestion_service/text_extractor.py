from PIL import Image
import pytesseract
# pip install pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class TextExtractor:
    def get_clean_text(self, image):
        raw_image = Image.open(image.path)

        # gray_image = raw_image.convert("L") # improving visibility for reading the text
        text = pytesseract.image_to_string(raw_image) # getting the text
        image.text = text
        return image

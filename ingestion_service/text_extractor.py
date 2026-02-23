from PIL import Image
import pytesseract
# pip install pytesseract


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def get_clean_text(images):
    for image in images:
        raw_image = Image.open(image["path"])
        gray_image = raw_image.convert("L") # improving visibility for reading the text

        text = pytesseract.image_to_string(gray_image) # getting the text

        clean_text = text.replace("\x0c", "").strip() # cleaning the text
        image["text"] = clean_text
        return image


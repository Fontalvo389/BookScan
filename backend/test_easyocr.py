import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Archivos de programa\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Archivos de programa\Tesseract-OCR"

img = Image.open("test.jpg")
texto = pytesseract.image_to_string(img, lang="spa")
print(texto)

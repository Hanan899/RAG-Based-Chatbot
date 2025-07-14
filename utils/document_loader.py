from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import numpy as np
import cv2
from utils.image_preprocess import preprocess_image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_pdf_bytes(pdf_bytes, filename):
    full_text = ""
    images = convert_from_bytes(pdf_bytes, poppler_path=r"C:\Users\hani3\Downloads\poppler-24.08.0\Library\bin")

    for i, image in enumerate(images):
        preprocessed = preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed, lang="eng+equ")
        full_text += f"\n\n=== Page {i+1} ===\n{text}"
    
    return {"text": full_text, "name": filename}

from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import numpy as np
import cv2
from utils.image_preprocess import preprocess_image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_pdf_bytes(pdf_bytes, filename):
    images = convert_from_bytes(pdf_bytes, poppler_path=r"C:\Users\hani3\Downloads\poppler-24.08.0\Library\bin")
    extracted = []

    for i, image in enumerate(images):
        preprocessed = preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed, lang="eng+equ")
        lines = text.splitlines()

        for line_number, line in enumerate(lines):
            line = line.strip()
            if line:
                extracted.append({
                    "text": line,
                    "metadata": {
                        "source": filename,
                        "page_number": i + 1,
                        "line_number": line_number + 1
                    }
                })

    return extracted

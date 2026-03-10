"""
Extract text from invoice documents using PDF parsing
and OCR for scanned images.
"""
import fitz
from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
import pytesseract
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_text_pdf(pdf_path):
    """Extract text from digital or scanned PDF files."""
    logging.info(f"Using PyMuPDF for {pdf_path}")
    text = ""
    full_text = ""
    doc = fitz.open(pdf_path)
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text().strip()
        if text:
            logging.info(f"Page {page_number+1} → digital text")
            full_text += page.get_text() + "\n"
        else:
            logging.info(f"Page {page_number+1} → OCR required")
            images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1)
            for img in images:
                ocr_text = ocr_image(img)
                full_text += ocr_text + "\n"
    doc.close()
    return full_text

def preprocess_image(image):
    """Preprocess image to improve OCR accuracy."""
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2.5, fy=2.5)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def ocr_image(image):
    """Perform OCR using Tesseract to extract text."""
    processed = preprocess_image(image)
    text = pytesseract.image_to_string(processed, lang="eng", config="--oem 3 --psm 6")
    return text

def extract_text_image(image_path):
    """Extract text from image invoices using OCR."""
    logging.info(f"Using OCR for image: {image_path}")
    image = Image.open(image_path)
    text = ocr_image(image)
    return text

def extract_text(file_path):
    """Detect file type and extract text accordingly."""
    ext = file_path.lower().split(".")[-1]

    if ext == "pdf":
        return extract_text_pdf(file_path)
    elif ext in ["png", "jpg", "jpeg"]:
        return extract_text_image(file_path)
    else:
        raise ValueError("Unsupported file type") 
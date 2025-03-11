from PIL import Image
import fitz
from pdf2image import convert_from_path
import os
from os import listdir
from os.path import isfile, join

PDF_PATH="input/mat11ats.pdf"
OUTPUT_DIR="temp"
DEFAULT_RESOLUTION=72 # DPI
SELECTED_RESOLUTION=300 # DPI, must be exatly this for the pixel inspection to work

def pdf_to_images(pdf_path, output_folder):
    dpi = SELECTED_RESOLUTION
    document = fitz.open(pdf_path)
    num_pages = document.page_count
    for page_number in range(num_pages):
        page = document.load_page(page_number)
        scale = dpi / DEFAULT_RESOLUTION
        zoom_matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=zoom_matrix)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = f"{output_folder}/page_{page_number + 1}.png"
        img.save(output_path)
        print(f"Saved page {page_number + 1} as {output_path}")
    return num_pages

pdf_to_images(PDF_PATH, OUTPUT_DIR)
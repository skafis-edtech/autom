from PIL import Image
import fitz
from pdf2image import convert_from_path
import os
from os import listdir
from os.path import isfile, join

def pdf_to_images(pdf_path, output_folder):
    dpi = 300  # must be exatly this for the pixel inspection to work
    document = fitz.open(pdf_path)
    num_pages = document.page_count
    for page_number in range(num_pages):
        page = document.load_page(page_number)
        scale = dpi / 72  # 72 DPI is the default resolution
        zoom_matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=zoom_matrix)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = f"{output_folder}/page_{page_number + 1}.png"
        img.save(output_path)
        print(f"Saved page {page_number + 1} as {output_path}")
    return num_pages

pdf_to_images("input/mat11ats.pdf", "temp")
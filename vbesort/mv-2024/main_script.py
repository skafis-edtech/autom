import fitz  # PyMuPDF
import os
import re

# Define input PDF file and output directory
pdf_path = "input/2024k.pdf"
output_dir = "output/"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Regular expression for detecting problem numbers (e.g., "B01.", "17.1.")
problem_pattern = re.compile(r"\b\d{2}\b")

# Function to find text with specific font
def extract_problem_text_in_font(page, font_name):
    text_instances = []
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if "lines" not in block:
            continue  # Skip if no text lines present
        
        for line in block["lines"]:
            for span in line["spans"]:
                if font_name in span["font"]:  # Check if the font matches Yantramanav
                    if re.match(problem_pattern, span["text"].strip()):
                        text_instances.append((span["text"].strip(), fitz.Rect(span["bbox"])))
    return text_instances

# Iterate over each page in the PDF, starting from the second page (index 1)
for page_num in range(1, len(pdf_document)):  # Start from page 1 (second page)
    page = pdf_document.load_page(page_num)  # Load the page
    
    # Extract problem numbers in the font "Yantramanav"
    problems = extract_problem_text_in_font(page, "Arial-BoldMT")
    
    # Now iterate over the detected problems to extract them as images
    for i, (problem_text, rect) in enumerate(problems):
        # Add some padding around the problem
        rect = rect + (-10, -10, 10, 10)  # Expand the rectangle for better visibility
        pix = page.get_pixmap(clip=rect)  # Extract the region as an image
        # Remove the last symbol if it's a period
        if problem_text.endswith('.'):
            problem_text = problem_text[:-1]

        output_image_path = os.path.join(output_dir, f"{problem_text}.png")
        pix.save(output_image_path)  # Save image to file

# Close the PDF after processing
pdf_document.close()

print(f"All problems in font 'Arial-BoldMT' have been extracted and saved as individual images in {output_dir}")

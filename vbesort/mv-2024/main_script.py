import fitz  # PyMuPDF
import os
import re

pdf_path = "input/2024k.pdf"
output_dir = "output/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

pdf_document = fitz.open(pdf_path)

problem_pattern = re.compile(r"\b\d{2}\b")

# Function to find text with specific font
def extract_problem_text_in_font(page, font_name):
    text_instances = []
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if "lines" not in block:
            continue
        
        for line in block["lines"]:
            for span in line["spans"]:
                if font_name in span["font"]: 
                    if re.match(problem_pattern, span["text"].strip()):
                        text_instances.append((span["text"].strip(), fitz.Rect(span["bbox"])))
    return text_instances

import re

def check_for_b_before_problem(problem_number, text_with_fonts_file="output/text_with_fonts.txt"):
    if not os.path.isfile(text_with_fonts_file):
        print(f"The file {text_with_fonts_file} does not exist. You need to first run text_content_analysis.py script to generate this file.")
        exit(1)

    with open(text_with_fonts_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    problem_pattern = re.compile(rf"^{re.escape(problem_number)}\.?$")  # Match problem_number exactly, with optional period

    for i, line in enumerate(lines):
        match = re.match(r"(.*) \((.*)\)", line.strip())
        if match:
            text = match.group(1).strip()
            font = match.group(2).strip()

            # Only consider problem numbers in "Arial-BoldMT" font
            if font != "Arial-BoldMT":
                continue  # Skip lines where the font is not Arial-BoldMT

            # Check if the current line contains the problem number exactly
            if re.match(problem_pattern, text):
                if i >= 2:
                    # Get the line two lines before
                    prev_line = lines[i-2].strip()
                    prev_line_match = re.match(r"(.*) \((.*)\)", prev_line)
                    if prev_line_match:
                        prev_text = prev_line_match.group(1).strip()
                        prev_font = prev_line_match.group(2).strip()

                        # Check if the previous text is exactly "B" and font is "Arial-BoldMT"
                        if prev_text == "B" and prev_font == "Arial-BoldMT":
                            return True  # Exact match found
                # Do not break; continue searching for other occurrences
    return False  # If no matching occurrence found


def has_subproblems(problem_number, text_with_fonts_file="output/text_with_fonts.txt"):
    if not os.path.isfile(text_with_fonts_file):
        print(f"The file {text_with_fonts_file} does not exist.")
        return False

    subproblem_pattern = re.compile(rf"\b{problem_number}\.\d+\b")
    with open(text_with_fonts_file, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"(.*) \((.*)\)", line.strip())
            if match:
                text = match.group(1).strip()
                if re.match(subproblem_pattern, text):
                    return True
    return False

# Iterate over each page in the PDF, starting from the second page (index 1)
for page_num in range(1, len(pdf_document)): 
    page = pdf_document.load_page(page_num) 
    
    problems = extract_problem_text_in_font(page, "Arial-BoldMT")
    
    b_is_on_root = None  # Track if the root problem is a "B" problem

    for i, (problem_text, rect) in enumerate(problems):
        rect = rect + (-10, -10, 10, 10)  # Slight adjustment for better screenshot area
        pix = page.get_pixmap(clip=rect)

        if problem_text.endswith('.'):
            problem_text = problem_text[:-1]  # Remove the trailing period

        # Check if the problem is a "B" problem
        if check_for_b_before_problem(problem_text):
            print(f"Found a 'B' problem: {problem_text}")
            if '.' in problem_text: 
                problem_text = f"{problem_text}B" 
            else: 
                if has_subproblems(problem_text):  
                    b_is_on_root = problem_text 
                else:
                    problem_text = f"{problem_text}B"
                    b_is_on_root = problem_text
        else: 
            if b_is_on_root and b_is_on_root == problem_text.split('.')[0]:
                problem_text = f"{problem_text}B"
            else:
                b_is_on_root = None

        # Save the image with the appropriate name
        output_image_path = os.path.join(output_dir, f"{problem_text}.png")
        pix.save(output_image_path)
# Close the PDF after processing
pdf_document.close()

print(f"All problems in font 'Arial-BoldMT' have been extracted and saved as individual images in {output_dir}")

import cv2
import numpy as np
import os
import re

# 665 out of 625 accuracy

# === CONFIGURATION ===
INPUT_DIR = "temp/"
OUTPUT_DIR = "output/"

# Defines the vertical strip where problem numbers are located
STRIP_X_START = 250   # Start of the vertical strip (left boundary)
STRIP_X_END = 285     # End of the vertical strip (right boundary)
RIGHT_MARGIN = 2350   # Where the problem text ends
Y_BOTTOM_MARGIN = 100

IMAGE_THRESHOLD = 200  # Threshold for detecting dark numbers in the strip
MIN_GAP_BETWEEN_PROBLEMS = 40  # Minimum vertical pixel distance between detected numbers

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# === GET ALL PAGE FILES IN ORDER ===
all_files = [f for f in os.listdir(INPUT_DIR) if re.match(r"page_\d+\.png", f)]
all_files.sort(key=lambda x: int(re.search(r"page_(\d+)\.png", x).group(1)))  # Sort numerically

problem_counter = 1  # Start numbering problems across all pages

# === PROCESS EACH PAGE FILE ===
for file in all_files:
    input_image_path = os.path.join(INPUT_DIR, file)

    # === STEP 1: Load and Preprocess Image ===
    image = cv2.imread(input_image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract only the strip where numbers are located
    strip = hsv[:hsv.shape[0] - Y_BOTTOM_MARGIN, STRIP_X_START:STRIP_X_END]

    # Apply threshold to detect problem numbers in the strip
    LOWER_BLACK = np.array([0, 0, 0])  # Lower bound for black in HSV
    UPPER_BLACK = np.array([180, 255, 50])  # Upper bound (ignores blue)

    mask_black = cv2.inRange(strip, LOWER_BLACK, UPPER_BLACK)  # Detects black numbers only
    strip_thresh = mask_black  # Use this for further processing

    # === STEP 2: Find Vertical Positions of Problem Numbers ===
    vertical_histogram = np.sum(strip_thresh, axis=1)  # Sum pixel intensity along columns

    # Detect peaks where numbers are present (darker spots in the strip)
    problem_y_coords = []
    for y in range(1, len(vertical_histogram) - 1):
        if vertical_histogram[y] > 0 and vertical_histogram[y - 1] == 0:
            problem_y_coords.append(y)

    # Filter out closely spaced values (to remove duplicate detections)
    filtered_y_coords = []
    prev_y = -MIN_GAP_BETWEEN_PROBLEMS
    for y in problem_y_coords:
        if y - prev_y > MIN_GAP_BETWEEN_PROBLEMS:
            filtered_y_coords.append(y)
            prev_y = y

    # === STEP 3: Extract & Save Individual Problems ===
    for i, y_start in enumerate(filtered_y_coords):
        y_end = filtered_y_coords[i + 1] if i + 1 < len(filtered_y_coords) else max(image.shape[0] - Y_BOTTOM_MARGIN, y_start + 10)

       # Crop the problem from STRIP_X_END to RIGHT_MARGIN
        problem_crop = image[y_start-50:y_end, STRIP_X_START-100:RIGHT_MARGIN]

        # Ensure the cropped image is not empty before saving
        if problem_crop.size > 0 and problem_crop.shape[0] > 0 and problem_crop.shape[1] > 0:
            problem_filename = f"mat11-{problem_counter:02d}.png"
            cv2.imwrite(os.path.join(OUTPUT_DIR, problem_filename), problem_crop)
            print(f"Saved {problem_filename}")
            problem_counter += 1  # Increment only if a valid image was saved
        else:
            print(f"Skipped empty problem at y={y_start}")

print("All pages processed successfully!")

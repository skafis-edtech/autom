import json
import re
import random
import string

# === CONFIGURATION ===
START_SKF = 1  # Starting SKF code number
SOURCE_ID = "q67knKaKvv21Es2kYZTp" 
UNSORTED_CAT_ID = "5PqEdNi0RBpAw33tIPQ8"  # Nepertvarkytos 99 kategorija
CAT_CODE_FOR_TEMP_IMAGES = "mat11"

# === STEP 1: Firebase-like ID Generator ===
def generate_firebase_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

# === STEP 2: Parse Markdown File for Problems/Answers ===
def parse_md(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    entries = {}
    sections = re.split(r"\n(\d+)\.", md_text)[1:]  # Capture problem numbers

    for i in range(0, len(sections), 2):
        problem_number = int(sections[i].strip())  # Extract problem number
        section_text = sections[i + 1].strip()

        # Replace single newlines with double newlines & fix Lithuanian chars
        formatted_text = section_text.replace("\n", "\n\n").strip()
        formatted_text = formatted_text.replace("é", "ė").replace("è", "ė").replace("ê", "ė").replace("ë", "ė").replace("ē", "ė").replace("ì", "į").replace("í", "į").replace("ị", "į").replace("ě", "ė").replace("İ", "Į").replace("ị", "į").replace("ị", "į").replace("ì", "į").replace("ě", "ė").replace("è", "ė").replace("é", "ė").replace("ụ", "ė")

        entries[problem_number] = formatted_text  # Store as dictionary {problem_number: text}

    return entries

# === STEP 3: Load Category Mapping from `cats.json` ===
def load_categories(cats_file):
    with open(cats_file, "r", encoding="utf-8") as f:
        cats_data = json.load(f)

    category_map = {}  # { "1.1.1.": "category_id", "1.2.3.": "category_id", ... }
    for cat in cats_data:
        code = cat["name"].split()[0]  # Extract category code (e.g., "1.1.1.")
        category_map[code] = cat["id"]

    return category_map

# === STEP 4: Load Class Mapping from `class.txt` ===
def load_class_mapping(class_file):
    class_map = {}  # { problem_number: [category_codes] }
    with open(class_file, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"(\d+)\s*→\s*([\d.;\s]+)", line.strip())
            if match:
                problem_number = int(match.group(1))  # Extract problem number
                categories = [c.strip() for c in match.group(2).split(";")]  # Extract categories
                class_map[problem_number] = categories

    return class_map

# === STEP 5: Merge Problems, Answers, and Categories ===
def merge_problems_answers(problem_file, answer_file, class_file, cats_file, output_json):
    problems_data = parse_md(problem_file)  # Extract problems
    answers_data = parse_md(answer_file)    # Extract answers
    class_map = load_class_mapping(class_file)  # Map problems to categories
    category_map = load_categories(cats_file)  # Get category IDs

    problems = []
    for number, problem_text in problems_data.items():
        # Get categories from class.txt, convert to category IDs, and add unsorted category
        category_codes = class_map.get(number, [])  # Get category codes from `class.txt`
        category_ids = [category_map[code] for code in category_codes if code in category_map]  # Convert to IDs
        category_ids.append(UNSORTED_CAT_ID)  # Always include "unsorted" category

        problems.append({
            "id": generate_firebase_id(),  # Generate Firebase-like ID
            "sourceId": SOURCE_ID,
            "problemImagePath": f"problems/{CAT_CODE_FOR_TEMP_IMAGES}-{number}.png",
            "answerText": answers_data.get(number, ""),  # Get answer if available
            "answerImagePath": f"answers/{CAT_CODE_FOR_TEMP_IMAGES}-{number}.png",
            "sourceListNr": number,  # Store problem number
            "problemText": problem_text,
            "categories": category_ids,  # Store category IDs
            "skfCode": f"SKF-{START_SKF + len(problems)}",  # Fixed SKF numbering
            "isApproved": False
        })

    # Write JSON output
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)

    print(f"JSON file '{output_json}' created successfully!")

# === USAGE ===
merge_problems_answers("input/mat11.md", "input/mat11ats.md", "input/class.txt", "output/cats.json", "output/problems.json")

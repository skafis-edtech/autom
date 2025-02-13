import json
import re
import random
import string

START_SKF = 1  # Starting SKF code number
SOURCE_ID = "q67knKaKvv21Es2kYZTp"  
UNSORTED_CAT_ID = "5PqEdNi0RBpAw33tIPQ8"  # Nepertvarkytos 99 kategorija
CAT_CODE_FOR_TEMP_IMAGES = "mat11"

def generate_firebase_id():
    """Generates a random Firebase-like document ID (20-character alphanumeric)."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

def parse_md(md_file):
    """Extracts problems/answers from a Markdown file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    entries = {}
    sections = re.split(r"\n(\d+)\.", md_text)[1:]  # Capture problem numbers

    for i in range(0, len(sections), 2):
        problem_number = int(sections[i].strip())  # Extract problem number
        section_text = sections[i + 1].strip()

        # Replace single newlines with double newlines
        formatted_text = section_text.replace("\n", "\n\n").strip()
        formatted_text = formatted_text.replace("é", "ė").replace("è", "ė").replace("ê", "ė").replace("ë", "ė").replace("ē", "ė")

        entries[problem_number] = formatted_text  # Store as dictionary {problem_number: text}

    return entries

def merge_problems_answers(problem_file, answer_file, output_json):
    """Merges problems with their corresponding answers and saves to JSON."""
    problems_data = parse_md(problem_file)  # Extract problems
    answers_data = parse_md(answer_file)    # Extract answers

    problems = []
    for number, problem_text in problems_data.items():
        problems.append({
            "id": generate_firebase_id(),  # Generate Firebase-like ID
            "sourceId": SOURCE_ID,
            "problemImagePath": f"problems/{CAT_CODE_FOR_TEMP_IMAGES}-{number}.png",
            "answerText": answers_data.get(number, ""),  # Get answer if available
            "answerImagePath": f"answers/{CAT_CODE_FOR_TEMP_IMAGES}-{number}.png",
            "sourceListNr": number,  # Store problem number
            "problemText": problem_text,
            "categories": [UNSORTED_CAT_ID],
            "skfCode": f"SKF-{START_SKF + len(problems)}",  # Fixed SKF numbering
            "isApproved": False
        })

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)

# Usage
merge_problems_answers("input/mat11.md", "input/mat11ats.md", "output/problems.json")

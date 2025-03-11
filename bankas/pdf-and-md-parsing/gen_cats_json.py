import json
import re
import random
import string

# Function to generate Firebase-like ID
def generate_firebase_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

# Read the input file
input_file = "input/cats.txt"  # Change this to your actual file path
output_file = "output/cats.json"

# Regular expression to match lines with three-number codes (e.g., 1.1.1, 1.2.3)
pattern = re.compile(r"^(\d+\.\d+\.\d+)\.\s+(.*)$")

categories = []

# Process the file
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        match = pattern.match(line.strip())
        if match:
            category_code = match.group(1).strip()  # Extracts "1.1.1"
            category_name = match.group(2).strip()  # Extracts "Skaičių aibės: Realiųjų skaičių aibės"
            categories.append({
                "id": generate_firebase_id(),
                "visibility": "PUBLIC",
                "name": f"{category_code}. {category_name}",
                "description": "",
                "ownerOfPrivateId": ""
            })

# Write to JSON file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(categories, file, indent=2, ensure_ascii=False)

print(f"JSON file '{output_file}' created successfully!")

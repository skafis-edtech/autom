import re

# === CONFIGURATION ===
INPUT_FILE = "input/mat11.md"
EXPECTED_RANGE = range(1, 626)  # Expect numbers from 1 to 625

# === STEP 1: Read the file ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# === STEP 2: Extract Numbers Using Regex ===
numbers = [int(match.group(1)) for match in re.finditer(r"\n(\d+)\.", content)]

# === STEP 3: Check Order & Missing Numbers ===
expected_numbers = list(EXPECTED_RANGE)

if numbers == expected_numbers:
    print("✅ All numbers from 1 to 625 are present and in order!")
else:
    missing = [num for num in expected_numbers if num not in numbers]
    extra = [num for num in numbers if num not in expected_numbers]

    print("❌ Issues found:")
    if missing:
        print(f"  Missing numbers: {missing}")
    if extra:
        print(f"  Extra numbers found: {extra}")

    # Check for incorrect order
    if numbers != sorted(numbers):
        print("  ❌ Numbers are not in correct order!")

    print("\n⚠️ Fix any missing/extra numbers in the file!")


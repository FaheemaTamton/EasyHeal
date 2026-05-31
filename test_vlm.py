import os
from backend.vlm.service import extract_medicine_details

# Always resolve path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "test_crop.jpg")

result = extract_medicine_details(image_path)

print("===== RAW MODEL OUTPUT =====")
print(result)


import cv2
from backend.vlm.preprocess import preprocess_prescription

processed = preprocess_prescription("test_crop.jpg")

cv2.imwrite("debug_processed.jpg", processed)
print("Saved debug_processed.jpg")

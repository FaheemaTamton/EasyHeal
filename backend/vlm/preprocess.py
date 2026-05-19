import cv2
import numpy as np


def preprocess_prescription(image_path):
    """
    Cleans and enhances a cropped prescription image
    for better VLM extraction.
    """

    # Read image from path
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image could not be loaded. Check the path.")

    # 1. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Increase contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)

    # 3. Reduce noise
    denoised = cv2.GaussianBlur(contrast, (5, 5), 0)

    # 4. Sharpen text
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    return sharpened

# utils/ocr.py

import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image: Image.Image) -> str:
    img_np = np.array(image)
    results = reader.readtext(img_np)
    extracted_text = " ".join([text for _, text, _ in results])
    return extracted_text

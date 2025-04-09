# utils/ocr.py

import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image: Image.Image) -> list[str]:
    img_np = np.array(image)
    results = reader.readtext(img_np, detail=1)

    # Group by Y position (row-like clustering)
    lines = []
    current_line = []
    previous_y = None
    threshold = 15  # pixel threshold to group words on the same line

    for (bbox, text, _) in results:
        y = bbox[0][1]  # top-left Y of the bounding box

        if previous_y is None or abs(y - previous_y) < threshold:
            current_line.append(text)
        else:
            lines.append(" ".join(current_line))
            current_line = [text]
        previous_y = y

    # Add the last line
    if current_line:
        lines.append(" ".join(current_line))

    return [line.strip() for line in lines if line.strip()]



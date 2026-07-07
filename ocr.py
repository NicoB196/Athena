import easyocr
from PIL import Image
import numpy as np

reader = easyocr.Reader(["en"])


def extract_run_data(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    result = reader.readtext(image_array)

    text = ""

    for item in result:
        text += item[1] + "\n"

    return text
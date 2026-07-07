import re

import easyocr
from PIL import Image
import numpy as np

reader = easyocr.Reader(["en"])


def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    result = reader.readtext(image_array)

    text = ""

    for item in result:
        text += item[1] + "\n"

    return text


def extract_run_data(uploaded_file):
    text = extract_text_from_image(uploaded_file)

    data = {
        "raw_text": text,
        "kilometer": None,
        "dauer": None,
        "pace": None,
        "puls": None,
        "hoehenmeter": 0,
        "kalorien": None,
    }

    distance_match = re.search(r"(\d+,\d+|\d+\.\d+)\s*km", text)
    if distance_match:
        data["kilometer"] = float(distance_match.group(1).replace(",", "."))

    duration_match = re.search(r"(\d+)\s*Min.*?(\d+)\s*Sek", text)
    if duration_match:
        minutes = int(duration_match.group(1))
        seconds = int(duration_match.group(2))
        data["dauer"] = round(minutes + seconds / 60, 2)

    pace_match = re.search(r"(\d+)[\'’´`](\d+)", text)
    if pace_match:
        minutes = int(pace_match.group(1))
        seconds = int(pace_match.group(2))
        data["pace"] = f"{minutes}:{seconds:02d}"

    kcal_match = re.search(r"(\d+)\s*kcal", text)
    if kcal_match:
        data["kalorien"] = int(kcal_match.group(1))

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "bpm" in line.lower() and index > 0:
            possible_pulse = re.search(r"(\d+)", lines[index - 1])
            if possible_pulse:
                data["puls"] = int(possible_pulse.group(1))
                break

    return data
import easyocr

reader = easyocr.Reader(["en"])


def extract_run_data(image):
    result = reader.readtext(image)

    text = ""

    for item in result:
        text += item[1] + "\n"

    return text
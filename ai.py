import base64
import json

import streamlit as st
from openai import OpenAI

from config import OPENAI_MODEL
from prompts import FITBIT_SCREENSHOT_PROMPT


def _image_to_base64(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    return base64.b64encode(image_bytes).decode("utf-8")


def analyze_fitbit_screenshot(uploaded_file):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    image_base64 = _image_to_base64(uploaded_file)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": FITBIT_SCREENSHOT_PROMPT,
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    raw_text = response.output_text.strip()

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError(f"KI-Antwort war kein gültiges JSON: {raw_text}")

    return {
        "kilometer": data.get("kilometer"),
        "dauer": data.get("dauer"),
        "pace": data.get("pace"),
        "puls": data.get("puls"),
        "hoehenmeter": data.get("hoehenmeter", 0),
        "kalorien": data.get("kalorien"),
    }
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import cv2
import time
import os
import numpy as np

from google import genai
from google.genai.types import Part
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

# ==== Setup ====

app = Flask(__name__)
CORS(app)

transcript_buffer = []

@app.route("/api/transcript", methods=["GET"])
def get_transcript():
    return jsonify(transcript_buffer)

def add_to_transcript_buffer(line: str):
    if line and (not transcript_buffer or transcript_buffer[-1] != line):
        transcript_buffer.append(line)


# ==== Gemini Transcription Logic ====

class Response(BaseModel):
    problem: str
    position: str
    added_text: str

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
client = genai.Client()

cap = cv2.VideoCapture(0)

def capture_frame() -> np.ndarray:
    ret, f = cap.read()
    _, f = cv2.imencode(".png", f)
    return f

def transcribe(interval: int):
    last_image = None
    current_section = ""

    while True:
        frame = capture_frame()
        image = Part.from_bytes(data=frame.tobytes(), mime_type="image/png")

        content = filter(lambda x: x is not None, [
            "Look at these two images, output what is new in the second image compared to the first image.",
            "If the image is not of a board or lecture with text, please output 'INVALID' in the problem field.",
            "If the board has been cleared or the slide changed, please output 'CLEARED' in the problem field.",
            "Output only those words, or exactly what has been added between the two pictures.",
            "If there is no previous picture, output everything in the only picture available.",
            "If there are no changes. Output 'NO CHANGES' in the problem field.",
            "If there is an obstruction, output 'OBSTRUCTED' in the problem field.",
            "If there is no problem put '' in the problem field.",
            "If there is no problem I would like you to also tell me where the new text is.",
            "For the position you should output either: 'END', or 'BEFORE <text>' or 'AFTER <text>'",
            "Output '' for anything not applicable.",
            f"The current content of the board is believed to be as follows: '{current_section}'",
            f"If this is incorrect, in the position field put 'REPLACE' and write all the text.",
            f"If Math is present, write it in latex. Make sure to include spaces in added_text as needed.",
            last_image,
            image
        ])

        try:
            raw = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=content,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Response
                }
            )
            response = raw.parsed
        except Exception as e:
            print("Gemini error:", e)
            time.sleep(interval)
            continue

        if response.problem == '':
            where = response.position
            if where == 'END':
                current_section += response.added_text
            elif where.startswith('BEFORE'):
                current_section = current_section.replace(where[7:], f'{response.added_text}' + where[7:])
            elif where.startswith('AFTER'):
                current_section = current_section.replace(where[6:], where[6:] + f'{response.added_text}')
            elif where == 'REPLACE':
                current_section = response.added_text

        print("\033c", end="")  # clear console
        print(current_section)

        if response.problem not in ['OBSTRUCTED', 'NO CHANGES']:
            last_image = image

        if response.problem == 'CLEARED':
            add_to_transcript_buffer(current_section.strip())
            current_section = ""

        time.sleep(interval)


# ==== App Runner ====

if __name__ == "__main__":
    threading.Thread(target=transcribe, args=(4,), daemon=True).start()
    app.run(port=5000, debug=True)

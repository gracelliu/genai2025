from time import sleep

import cv2
import asyncio

import numpy as np
from google import genai
from google.genai.types import Part
from pydantic import BaseModel
import os

from googledocs import authenticate_google_docs, add_to_doc, create_doc_with_text


class Response(BaseModel):
    problem: str
    position: str
    added_text: str

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def clear_console():
    if os.getenv('TERM'):
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\n" * 100)

def setup():
    service = authenticate_google_docs()
    # Check id doc-id file exists
    if os.path.exists("doc-id"):
        with open("doc-id", "r") as f:
            doc_identifier = f.read()
    else:
        # Create a new document
        doc_identifier = create_doc_with_text(service, "Transcribed Doc", "...")
        with open("doc-id", "w") as f:
            f.write(doc_identifier)
    return service, doc_identifier

cap: cv2.VideoCapture = cv2.VideoCapture(0)
docs_service, doc_id = setup()

def capture_frame() -> np.ndarray:
    ret, f = cap.read()
    # Encode to png
    _, f = cv2.imencode(".png", f)
    return f

def consume_section(section: str):
    if section == '':
        return
    add_to_doc(docs_service, doc_id, section)

def transcribe(interval: int):
    last_image = None

    sections = []
    current_section = ""

    while True:
        frame = capture_frame()
        image = Part.from_bytes(data=frame.tobytes(), mime_type="image/png")
        content = filter(lambda x: x is not None, [
            "Look at these two images, output what is new in the second image compared to the first image."
            "If the image is not of a board or lecture with text, please output 'INVALID' in the problem field."
            "If the board has been cleared or the slide changed, please output 'CLEARED' in the problem field."
            "Output only those words, or exactly what has been added between the two pictures."
            "If there is no previous picture, output everything in the only picture available."
            "If there are no changes. Output 'NO CHANGES' in the problem field."
            "If there is an obstruction, output 'OBSTRUCTED' in the problem field."
            "If there is no problem put '' in the problem field."
            "If there is no problem I would like you to also tell me where the new text is."
            "For the position you should output either: 'END', or 'BEFORE <text> or 'AFTER <text>'"
            "Output '' for anything not applicable."
            f"The current content of the board is believed to be as follows: '{current_section}'"
            f"If this is incorrect, in the position field put 'REPLACE' and write all the text."
            f"If Math is present, write it in latex. Make sure to include spaces in added_text as needed.",
            last_image, image])
        raw = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=content,
            config={
                "response_mime_type": "application/json",
                "response_schema": Response
            }
        )
        response = raw.parsed

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

        clear_console()
        print(current_section)

        if response.problem not in ['OBSTRUCTED', 'NO CHANGES']:
            last_image = image
        if response.problem == 'CLEARED':
            consume_section(current_section)
            current_section = ""
        sleep(interval)

transcribe(4)

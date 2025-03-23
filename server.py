from time import sleep

import asyncio

from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from google import genai
from google.genai.types import Part
from pydantic import BaseModel
import os
import tempfile
import subprocess
from flask import send_file
from sqlalchemy.orm import Session

from document import create_session, get_user_by_name, get_documents_by_user, Document, get_document_by_id, create_user, \
    create_document, update_document

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

sections = []
current_section = ""
last_image = None
session: Session | None = None

class Response(BaseModel):
    notes: str
    problem: str
    update_notes: bool

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def clear_console():
    if os.getenv('TERM'):
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\n" * 100)

@app.route('/api/new_image', methods=['POST'])
def new_image():
    global current_section, sections, last_image

    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400

    uploaded_file = request.files['image']
    image_data = uploaded_file.read()
    image = Part.from_bytes(data=image_data, mime_type="image/png")

    prompt = (
        "Look at these two images, if the image is not of a board or lecture with text, set problem to 'INVALID'"
        "Otherwise, perform the following task:"
        "Decide if there is anything added or removed in the second image that is not in the first image. You are also"
        "provided with the current notes recorded, if they are incomplete or there is new content images are different,"
        "then make notes (like a college student) on the content in the second image and output them in the notes field."
        "These notes should contain the full content of the lecture and nothing else."
        "Output notes in valid markdown format that will be rendered with marked js. Do not"
        "put anything except for notes in the notes field. If there is no change between the images, and the notes are up to date"
        " then set problem to '' and update_notes to false but STILL output the notes. Additionally, if the board is obstructed, "
        "set problem to 'OBSTRUCTED'. If the two images are of different slides or boards, "
        "set problem to 'NEW_SECTION' to indicate that we are dealing with a different part of the lecture now, importantly though, "
        "if the board has not update_notes but is just not in view or obstructed. Output 'OBSTRUCTED' as the problem, only output NEW_SECTION "
        "once there is a new slide or board."
        " and return notes on this new lecture piece. Use problem=NEW_SECTION sparingly, only when "
        "the images are two different slides/lessons. To ensure consistency, you must not"
        " output NEW_SECTION before the slide changes. Make sure the section notes are always up to date. Only"
        "set update_notes to true if the notes have been updated from what I give you below."
    )

    content = filter(lambda x: x is not None, [prompt, f"Here is the current version of this section of the notes: '''{current_section}''' If this is wrong or missing anything, output new notes taken from the 2nd image and set update_notes to true.", last_image, image])
    raw = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=content,
        config={
            "response_mime_type": "application/json",
            "response_schema": Response
        }
    )
    response = raw.parsed

    new_section_flag = False

    if response.problem == 'NEW_SECTION':
        sections.append(current_section)
        current_section = response.notes
        new_section_flag = True
    elif response.update_notes:
        current_section = response.notes

    if response.problem not in ['OBSTRUCTED', 'INVALID'] and response.update_notes:
        last_image = image

    print(f"Problem: {response.problem}")
    print(f"Edits: {response.update_notes}")
    print(f"Notes: {response.notes}")

    return {
        "new_section": new_section_flag,
        "current_section": current_section,
        "problem": response.problem
    }

@app.route('/api/document/list', methods=['GET'])
def endpoint_get_documents():
    global session
    user = get_user_by_name(session, 'Grace')
    if user is None:
        return jsonify([])
    documents = get_documents_by_user(session, user)

    return jsonify([{
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "group": document.group
    } for document in documents])

@app.route('/api/document/create', methods=['POST'])
def endpoint_create_document():
    global session
    user = get_user_by_name(session, 'Grace')
    data = request.json
    document = create_document(session, user, data['title'], data['content'], data['group'])

    return jsonify({
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "group": document.group
    })

@app.route('/api/document/update', methods=['POST'])
def endpoint_update_document():
    global session
    data = request.json
    document = get_document_by_id(session, data['id'])
    title = data['title'] if 'title' in data else document.title
    content = data['content'] if 'content' in data else document.content
    group = data['group'] if 'group' in data else document.group
    update_document(session, document, title, content, group)


# Run app
if __name__ == '__main__':
    session = create_session()
    create_user(session, 'Grace')
    app.run(host='localhost', port=8000)
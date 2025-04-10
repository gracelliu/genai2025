import sys
import time
from platform import system
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
from dotenv import load_dotenv

load_dotenv()

from document import create_session, get_user_by_name, get_documents_by_user, Document, get_document_by_id, create_user, \
    create_document, update_document, delete_document

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

requests_this_day = 0
# day is just time millis / 86400000
day = int(time.time() / (24 * 60 * 60))
sections = []
last_image = None
session: Session | None = None

class Response(BaseModel):
    notes: str
    thinking: str
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
    global sections, last_image, requests_this_day, day

    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400

    if requests_this_day >= 2500:
        return {"error": "Rate limit exceeded"}, 429

    requests_this_day += 1
    curr_day = int(time.time() / (24 * 60 * 60))
    if curr_day != day:
        requests_this_day = 0
        day = curr_day

    uploaded_file = request.files['image']
    current_section = request.form['current_section']
    image_data = uploaded_file.read()
    image = Part.from_bytes(data=image_data, mime_type="image/png")

    prompt = (
        "Look at these two images, the second of which is the current most up-to-date version."
        "If the image is not of a board, lecture with text, book, or paper, set problem to 'INVALID'"
        "Otherwise, perform the following task:"
        "Decide if there is anything added or removed in the second image that is not in the first image. You are also"
        "provided with the current notes recorded, if they are incomplete or there is new content images are different,"
        "then make notes (like a college student) on the content in the second image and output them in the notes field."
        "These notes should contain the full content of the lecture and nothing else."
        "Output notes in valid markdown format that will be rendered with marked js. Do not"
        "put anything except for notes in the notes field. If there is no change between the images, and the notes are up to date"
        " then set problem to '' and update_notes to false but STILL output the notes. Additionally, if the board is obstructed, "
        "set problem to 'OBSTRUCTED'. If the two images are of different slides, boards or pages, "
        "set problem to 'NEW_SECTION' to indicate that we are dealing with a different part of the lecture now, importantly though, "
        "if the board is just not in view or obstructed. Output 'OBSTRUCTED' as the problem, only output NEW_SECTION "
        "once there is a new slide, board or page."
        " and return notes on this new lecture piece. Use problem=NEW_SECTION sparingly, only when "
        "the images are two different slides/lessons/pages. To ensure consistency, you must not"
        " output NEW_SECTION before the slide changes. Make sure the section notes are always up to date. Only"
        "set update_notes to true if the notes have been updated from what I give you below. If the content is"
        "confusing, elaborate a bit, they should be readable notes."
        ""
        "Schema: (output in this order)"
        "notes: str - What you see from the second image, as notes. Fully and fresh updated by you."
        "thinking: str - A short explanation of why you put the values you did for the three other fields."
        "problem: str - The problem with the images, if any"
        "update_notes: bool - Whether you have update the notes to be up to date"
        ""
        "The next message will contain what is currently in the notes."
    )

    content = filter(lambda x: x is not None, [prompt, f"Here is the current/old version of this section of the notes: \n\"\"\"\n{current_section}\n\"\"\"\n If this is wrong or missing anything, output new notes taken from the 2nd image and set update_notes to true.", last_image, image])
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

    print('\n\n\n')
    print(f"Problem: {response.problem}")
    print(f"Edits: {response.update_notes}")
    print(f"Explanation: {response.thinking}")
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

    if user is None:
        print("❌ No user 'Grace' found!")
        return jsonify({"error": "User not found"}), 400

    try:
        data = request.json
        print("✅ Incoming request data:", data)
        document = create_document(session, user, data['title'], data['content'], data['group'])
        return jsonify({
            "id": document.id,
            "title": document.title,
            "content": document.content,
            "group": document.group
        })
    except Exception as e:
        print("🔥 Exception while creating document:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/document/update', methods=['POST'])
def endpoint_update_document():
    global session
    data = request.json
    document = get_document_by_id(session, data['id'])
    title = data['title'] if 'title' in data else document.title
    content = data['content'] if 'content' in data else document.content
    group = data['group'] if 'group' in data else document.group
    update_document(session, document, title, content, group)
    return jsonify({
        "id": document.id,
        "title": title,
        "content": content,
        "group": group
    })

@app.route('/api/document/delete', methods=['DELETE'])
def endpoint_delete_document():
    global session
    data = request.json
    document = get_document_by_id(session, data['id'])
    delete_document(session, document)
    return jsonify({"success": True})


# Run app
if __name__ == '__main__':
    session = create_session()
    create_user(session, 'Grace')
    app.run(host='localhost', port=8080)
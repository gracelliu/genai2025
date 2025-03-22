import os
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ==== SETUP ====

SCOPES = ['https://www.googleapis.com/auth/documents']

def load_gemini_api_key():
    with open(os.getenv("GENAI_API_KEY"), 'r') as f:
        return f.read().strip()

def authenticate_google_docs():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('docs', 'v1', credentials=creds)

# ==== GOOGLE DOCS UTILS ====

def extract_text_from_doc(service, doc_id):
    doc = service.documents().get(documentId=doc_id).execute()
    content = doc.get('body', {}).get('content', [])
    text = ''
    for elem in content:
        if 'paragraph' in elem:
            for p_elem in elem['paragraph'].get('elements', []):
                text += p_elem.get('textRun', {}).get('content', '')
    return text.strip()

def create_doc_with_text(service, title, text):
    doc = service.documents().create(body={'title': title}).execute()
    doc_id = doc['documentId']
    requests = [
        {
            'insertText': {
                'location': {'index': 1},
                'text': text
            }
        },
        {
            'updateTextStyle': {
                'range': {'startIndex': 1, 'endIndex': 1 + len(text)},
                'textStyle': {
                    'weightedFontFamily': {'fontFamily': 'Lexend'},
                    'fontSize': {'magnitude': 14, 'unit': 'PT'}
                },
                'fields': 'weightedFontFamily,fontSize'
            }
        }
    ]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return doc_id

def add_to_doc(service, doc_id, text_to_add):
        # Get the current document to find its length
        doc = service.documents().get(documentId=doc_id).execute()
        end_index = doc['body']['content'][-1]['endIndex']

        requests = [
            {
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': text_to_add
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': end_index - 1,
                        'endIndex': end_index - 1 + len(text_to_add)
                    },
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Lexend'},
                        'fontSize': {'magnitude': 14, 'unit': 'PT'}
                    },
                    'fields': 'weightedFontFamily,fontSize'
                }
            }
        ]

        service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()


# ==== GEMINI AI STEP ====

def organize_text_with_gemini(raw_text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
You are a helpful writing assistant. I will give you some unstructured or messy text. 
Reorganize it into something well-structured and clean:
- Add clear headings
- Use bullet points where appropriate
- Correct grammar and typos
- Keep the meaning the same
Here is the text:
\"\"\"
{raw_text}
\"\"\"
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# ==== MAIN ====

def main():
    # --- Step 1: Authenticate Docs
    service = authenticate_google_docs()

    # --- Step 2: Choose source document
    source_doc_id = input("Enter the Google Doc ID you want to improve: ")

    # --- Step 3: Extract text
    print("Extracting original content...")
    original_text = extract_text_from_doc(service, source_doc_id)

    # --- Step 4: Run through Gemini
    print("Sending to Gemini for reorganization...")
    api_key = load_gemini_api_key()
    improved_text = organize_text_with_gemini(original_text, api_key)

    # --- Step 5: Create new Doc
    print("Creating new Google Doc...")
    new_doc_id = create_doc_with_text(service, "Organized Doc (Gemini)", improved_text)

    print(f"\n✅ Done! View your new document:\nhttps://docs.google.com/document/d/{new_doc_id}/edit")

if __name__ == '__main__':
    main()

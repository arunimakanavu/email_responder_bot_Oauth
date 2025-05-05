import base64
import email
import os
from email.mime.text import MIMEText

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from transformers import pipeline

# === 1. OAuth Authentication ===
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Use custom path to client secret
CLIENT_SECRET_PATH = os.path.join('secrets', 'client_secret.json')

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
creds = flow.run_local_server(port=0)
service = build('gmail', 'v1', credentials=creds)

# === 2. Load Hugging Face Model ===
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# === 3. Function to Create Email Message ===
def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

# === 4. Get Unread Emails ===
results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
messages = results.get('messages', [])

for msg in messages:
    message = service.users().messages().get(userId='me', id=msg['id']).execute()
    headers = message['payload']['headers']

    sender = next(h['value'] for h in headers if h['name'] == 'From')
    subject = next(h['value'] for h in headers if h['name'] == 'Subject')

    payload = message['payload']
    parts = payload.get('parts', [])
    if parts:
        body = base64.urlsafe_b64decode(parts[0]['body']['data']).decode()
    else:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode()

    # === 5. Generate Reply ===
    prompt = f"Reply to this email professionally:\nSubject: {subject}\n\nBody: {body}"
    reply = generator(prompt, max_length=150, do_sample=False)[0]['generated_text']

    print(f"\n New email from: {sender}")
    print(f"Subject: {subject}")
    print(f"\n Suggested Reply:\n{reply}")

    approve = input("\n Send this reply? (y/n): ").strip().lower()
    if approve == 'y':
        message_to_send = create_message(sender, f"RE: {subject}", reply)
        service.users().messages().send(userId='me', body=message_to_send).execute()
        print("Sent!")
    else:
        print("Skipped.")

    # === 6. Mark as Read ===
    service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()

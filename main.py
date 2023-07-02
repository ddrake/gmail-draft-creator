from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import os
import base64
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def create_draft(email, name, subject, template):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(template)
    message['to'] = email
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    raw_message = raw_message.decode()
    body = {'message': {'raw': raw_message}}

    draft = service.users().drafts().create(userId='me', body=body).execute()

create_draft('iloveitaly@gmail.com', 'Mike', 'Test', 'Hello, World!')
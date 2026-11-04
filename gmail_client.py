from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import base64

SCOPES =["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

    return creds

def get_unread_emails():
    creds = authenticate_gmail()

    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId = "me",
        labelIds =["UNREAD"],
        maxResults=5
    ).execute()

    return results

def get_email_details(message_id):
    creds = authenticate_gmail()

    service = build("gmail", "v1", credentials=creds)

    message = service.users().messages().get(userId="me", id=message_id).execute()

    return message

def extract_email_metadata(email_data):
    headers = email_data["payload"]["headers"]
    subject = None
    sender = None

    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"]
        elif header["name"] == "From":
            sender = header["value"]

    return {"subject": subject, "sender": sender}

#Base64 decodes gmail images, text, html, attachments
def extract_email_body(email_data):
    parts = email_data["payload"].get("parts",[])

    for part in parts:

        if part["mimeType"] == "text/plain":

            data = part["body"].get("data")

            if data:

                decoded_bytes = base64.urlsafe_b64decode(data)

                return decoded_bytes.decode("utf-8")
    return None

def build_email_object(email_data):
    metadata = extract_email_metadata(email_data)
    body = extract_email_body(email_data)

    return {"subject": metadata["subject"],
            "sender": metadata["sender"],
            "body": body}
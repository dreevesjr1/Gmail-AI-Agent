from gmail_client import (get_unread_emails, get_email_details, extract_email_metadata, extract_email_body, \
    build_email_object)
from config import OPENAI_API_KEY
from summarizer import summarize_email
import json, os

def load_existing_analyses():
    if not os.path.exists("email_digest.json"):
        return []
    with open("email_digest.json","r") as file:
        return json.load(file)

def save_analyses(analyses):
    with open("email_digest.json", "w") as file:
        json.dump(analyses,file, indent=4)

def main():
    emails = get_unread_emails()

    analyses = load_existing_analyses()

    existing_ids = {analysis["message_id"] for analysis in analyses}

    for email in emails["messages"]:
        message_id = email["id"]

        details = get_email_details(message_id)

        email_object = build_email_object(details)

        analysis = summarize_email(email_object)
        analysis["message_id"] = message_id

        if message_id not in existing_ids:
            analyses.append(analysis)
            existing_ids.add(message_id)

    analyses.sort(key=lambda x:x["priority_score"], reverse=True)

    save_analyses(analyses)

if __name__ == "__main__":
    main()
from gmail_client import (get_unread_emails, get_email_details, extract_email_metadata, extract_email_body, \
    build_email_object)
from config import OPENAI_API_KEY
from summarizer import summarize_email
import json, os



def main():
    emails = get_unread_emails()

    analyses = []

    for email in emails["messages"]:
        message_id = email["id"]

        details = get_email_details(message_id)

        email_object = build_email_object(details)

        analysis = summarize_email(email_object)
        analysis["message_id"] = message_id

        print(analysis)
        analyses.append(analysis)

    analyses.sort(key=lambda x:x["priority_score"], reverse=True)

    for analysis in analyses:
        print("-" * 50)
        print(f"Message ID: {analysis['message_id']}")
        print(f"Category: {analysis['category']}")
        print(f"Priority: {analysis['priority_score']}")
        print(f"Reason: {analysis['priority_reason']}")
        print(f"Summary: {analysis['summary']}")
        print(f"Action items: {analysis['action_items']}")

if __name__ == "__main__":
    main()
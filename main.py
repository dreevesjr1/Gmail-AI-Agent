from gmail_client import get_unread_emails, get_email_details, extract_email_metadata, extract_email_body

def main():
    emails = get_unread_emails()

    first_email = emails["messages"][0]

    message_id = first_email["id"]

    details = get_email_details(message_id)

    metadata = extract_email_metadata(details)

    body = extract_email_body(details)

    print(metadata)

    print("\nEMAIL BODY:\n")

    print(body)

if __name__ == "__main__":
    main()
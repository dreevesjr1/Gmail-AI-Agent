from gmail_client import (get_unread_emails, get_email_details, extract_email_metadata, extract_email_body, \
    build_email_object)


def main():
    emails = get_unread_emails()

    first_email = emails["messages"][0]

    message_id = first_email["id"]

    details = get_email_details(message_id)

    email = build_email_object(details)

    print(email)

if __name__ == "__main__":
    main()
from gmail_client import get_unread_emails, get_email_details

def main():
    emails = get_unread_emails()

    first_email = emails["messages"][0]

    message_id = first_email["id"]

    details = get_email_details(message_id)

    print(details)

if __name__ == "__main__":
    main()
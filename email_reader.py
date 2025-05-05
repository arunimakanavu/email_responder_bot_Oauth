import os
from imapclient import IMAPClient
import pyzmail36
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")

def get_unread_emails():
    with IMAPClient(IMAP_SERVER, ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder("INBOX", readonly=False)

        messages = client.search(["UNSEEN"])
        unread_emails = []

        for msgid, data in client.fetch(messages, ["ENVELOPE", "RFC822"]).items():
            message = pyzmail36.PyzMessage.factory(data[b"RFC822"])
            subject = message.get_subject()
            from_address = message.get_addresses("from")[0][1]
            if message.text_part:
                body = message.text_part.get_payload().decode(message.text_part.charset)
            elif message.html_part:
                body = message.html_part.get_payload().decode(message.html_part.charset)
            else:
                body = ""
            unread_emails.append((msgid, subject, from_address, body))

        return unread_emails, client

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")

def send_email(to_address, subject, body):
    msg = EmailMessage()
    msg["Subject"] = f"Re: {subject}"
    msg["From"] = EMAIL
    msg["To"] = to_address
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
        print(f"✅ Reply sent to {to_address}")

from email_reader import get_unread_emails
from email_sender import send_email
from ai_responder import generate_response

def main():
    emails, client = get_unread_emails()

    for msgid, subject, from_address, body in emails:
        print(f"\n📨 New Email From: {from_address}")
        print(f"📌 Subject: {subject}")
        print(f"📃 Body:\n{body}\n")

        prompt = f"Reply to this email:\n\n{body}"
        ai_reply = generate_response(prompt)

        print("\n🤖 Suggested Reply:")
        print("=" * 60)
        print(ai_reply)
        print("=" * 60)

        user_input = input("👉 Do you want to send this reply? (yes/no/edit): ").strip().lower()

        if user_input == "yes":
            send_email(from_address, subject, ai_reply)
        elif user_input == "edit":
            print("✏️ Paste your edited reply below. Press Enter twice to finish.")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            edited_reply = "\n".join(lines)
            send_email(from_address, subject, edited_reply)
        else:
            print("🚫 Skipped sending reply.")

        client.set_flags(msgid, [b'\\Seen'])

    client.logout()

if __name__ == "__main__":
    main()

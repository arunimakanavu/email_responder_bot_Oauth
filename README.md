
# AI Email Responder Bot

An automation tool that reads unread emails from your Gmail inbox, generates intelligent replies using Hugging Face transformers, and optionally sends responses using the Gmail API with OAuth2 authentication.

---

## Features

- Automatically reads unread emails from Gmail via IMAP  
- Uses AI models (GPT-2 or FLAN-T5) to generate professional responses  
- Allows manual review, editing, and approval before sending replies  
- Sends replies through Gmail API using OAuth2  
- Marks emails as read after processing

---

## Project Structure

```
.
├── main.py                  # User-interactive script to handle email processing
├── email_reader.py         # Fetch unread emails using IMAP
├── email_sender.py         # Send emails using Gmail API
├── ai_responder.py         # Generate AI-based responses using transformers
├── oauth_responderbot.py   # Standalone bot with Gmail OAuth and FLAN-T5
├── requirements.txt        # Python dependencies
└── secrets/
    └── client_secret.json  # OAuth client credentials (excluded from version control)
```

---

## How It Works

1. **main.py**
   - Retrieves unread emails using `get_unread_emails`
   - Uses `generate_response` to create a suggested reply
   - Prompts the user to approve, edit, or skip sending the reply
   - Sends the email and marks it as read

2. **oauth_responderbot.py**
   - Uses Google OAuth2 to authenticate
   - Fetches unread Gmail messages
   - Generates replies with `google/flan-t5-base`
   - Sends the message via Gmail API if approved

---

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/email-responder-bot.git
cd email-responder-bot
```

2. **Create and Activate a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**

Create a `.env` file in the root directory with:

```ini
EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
IMAP_SERVER=imap.gmail.com
```

For Gmail, enable 2FA and generate an App Password to use in place of your actual password.

5. **OAuth Setup for Gmail API**

- Go to the [Google Cloud Console](https://console.cloud.google.com/)
- Create a project and enable the Gmail API
- Create OAuth credentials and download the `client_secret.json` file
- Save the file in the `secrets/` folder

---

## Usage

### Option 1: Manual Approval Mode

```bash
python main.py
```

- Displays unread emails
- Generates AI replies using GPT-2
- Asks you whether to send, skip, or edit each response

### Option 2: OAuth Gmail Bot (Automated Flow)

```bash
python oauth_responderbot.py
```

- Uses Google OAuth to fetch and respond to unread emails
- Generates replies using FLAN-T5
- Sends replies if you confirm

---

## AI Models Used

- `gpt2` for basic response generation (`ai_responder.py`)
- `google/flan-t5-base` for more refined replies (`oauth_responderbot.py`)

Models can be switched easily by changing the `pipeline` configuration.

---

## Example Output

```
New Email From: john@example.com
Subject: Meeting Follow-up
Body:
Hi, can we reschedule our meeting to next Monday?

Suggested Reply:
Hi John, sure! Next Monday works for me. Let me know what time suits you best.

Do you want to send this reply? (yes/no/edit):
```

---

## Security Notes

- Do not upload `.env` or `client_secret.json` to version control.
- Add sensitive files to `.gitignore` to keep them private.

---

## Dependencies

See `requirements.txt` for the full list of packages.

Core libraries:

- `transformers`
- `torch`
- `imapclient`
- `pyzmail36`
- `google-auth-oauthlib`
- `python-dotenv`

---

## Potential Improvements

- Add support for attachments
- Improve conversation memory (context-aware responses)
- Background processing (cron job or serverless deployment)
- Logging and analytics for responses

---

## Author

Developed by [Your Name](https://github.com/yourusername)

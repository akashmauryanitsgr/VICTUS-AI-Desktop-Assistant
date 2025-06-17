import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re, os, sys,subprocess
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
EMAIL_ADDRESS = env_vars.get("your_gmail.com")
EMAIL_PASSWORD = env_vars.get("your_app_password")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"



import re



def send_email(query: str):
    """
    Sends an email by prompting the user for the recipient and message if not provided in the initial query.
    """
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Backend.SpeechToText import SpeechRecognition
    from Backend.TextToSpeech import TextToSpeech
    from Frontend.Input import get_user_input
    # If the query is too vague and just says "send email"
    #if "send email" in query.lower() and len(query.split()) == 2:
    if query:
        TextToSpeech("Please tell the recipient's email address.")    
        result = subprocess.run(
             ['python', r'C:\Jarvis\Jarvis\Frontend\Input.py', 'email'], 
             capture_output=True, 
             text=True)
        recipient = result.stdout.strip()
        print(f"this is your email{recipient}")
        TextToSpeech("Now, please tell me the message you want to send to {recipient}.")
        body = SpeechRecognition()  # Capture the message
        TextToSpeech("What would you like the subject to be?")
        subject = SpeechRecognition()  # Capture the subject

    else:
        # Handle queries like "send email john@example.com about Hello there! with subject Greetings"
        try:
            match = re.match(r"(.*?) about (.*?) with subject (.*)", query)
            if not match:
                TextToSpeech(f"Email command format incorrect.")
                return

            recipient, body, subject = match.groups()
            TextToSpeech("Sending email to: {recipient}\nSubject: {subject}\nBody: {body}")

        except Exception as e:
            TextToSpeech(f"Failed to parse the query: {e}")
            return

    try:
        # Send email process
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient.strip()
        msg['Subject'] = subject.strip()

        msg.attach(MIMEText(body.strip(), 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        TextToSpeech("Email sent successfully to {recipient}!")
        print("Email sent successfully!")

    except Exception as e:
        TextToSpeech(f"Failed to send email: {str(e)}")
        print(f"Failed to send email: {str(e)}")

        


import imaplib
import email
import html
import quopri
from bs4 import BeautifulSoup


def clean_html(content: str) -> str:
    """Strip HTML tags and decode HTML entities."""
    content = html.unescape(content)
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    return ''.join([i if ord(i) < 128 else '' for i in text])  # Remove non-ASCII chars

def decode_encoded_text(content: str) -> str:
    """Decode subject/content if MIME encoded."""
    try:
        decoded_fragments = email.header.decode_header(content)
        return ''.join([
            fragment.decode(encoding if encoding else 'utf-8') if isinstance(fragment, bytes) else fragment
            for fragment, encoding in decoded_fragments
        ])
    except:
        return content

def extract_email_body(msg):
    """Extract the plain text body from an email message."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                except:
                    continue
    else:
        try:
            return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")
        except:
            return ""
    return ""

def read_email(criteria: str, max_emails: int = 3):
     
    from Backend.SpeechToText import SpeechRecognition
    from Backend.TextToSpeech import TextToSpeech
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        # Set criteria
        if "from " in criteria:
            sender_email = criteria.split("from ")[1].strip()
            search_criteria = f'(FROM "{sender_email}")'
        elif "unread" in criteria:
            search_criteria = '(UNSEEN)'
        else:
            search_criteria = 'ALL'

        result, data = mail.search(None, search_criteria)
        mail_ids = data[0].split()

        if not mail_ids:
            TextToSpeech("No emails found matching your criteria.")
            return

        latest_ids = mail_ids[-max_emails:]
        email_summaries = []

        for mail_id in reversed(latest_ids):
            result, msg_data = mail.fetch(mail_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = decode_encoded_text(msg["subject"] or "No Subject")
            sender = decode_encoded_text(msg["from"] or "Unknown sender")
            body = extract_email_body(msg)
            body = clean_html(body)[:200]  # Clean and limit preview

            summary = f"Email from {sender}. Subject: {subject}. Message: {body}"
            email_summaries.append((sender, subject, extract_email_body(msg), summary))
            TextToSpeech(summary)

        TextToSpeech("Which email would you like to read in full? Please Say the number.")
        '''for index, summary in enumerate(email_summaries):
            print(f"{index+1 }: {summary[3]}")
            ShowTextToScreen(f"{index+1 }: {summary[3]}")
            #ShowTextToScreen(index+1 + summary[3]) '''
        response_file_path = r"C:\Jarvis\Jarvis\Frontend\Files\Responses.data"

        with open(response_file_path, "w", encoding='utf-8') as file:
            for index, summary in enumerate(email_summaries):
                print(f"{index+1 }: {summary[3]}")
                file.write(f"{index + 1}: {summary[3]}\n")


        email_choice =int(SpeechRecognition()) # Simulate input for now
        if email_choice < 1 or email_choice > len(email_summaries):
            TextToSpeech("Invalid choice. Please try again.")
            return

        selected = email_summaries[email_choice - 1]
        sender, subject, body, _ = selected
        full_email = f"Full email from {sender}. Subject: {subject}. Body: {body.strip()}"
        TextToSpeech(full_email)
        TextToSpeech(f"Reading full email from {sender}. Subject: {subject}. Body: {body.strip()}")
        mail.logout()

    except Exception as e:
        TextToSpeech(f"Failed to read email: {e}")


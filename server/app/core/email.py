from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)
from app.core.config import settings
import base64
from dotenv import load_dotenv
import os
import requests

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")


def send_email(
    subject: str, to_emails: str, html_content: str, attachment_url: str = None
):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
    )
    if attachment_url:
        attachment = Attachment(
            FileContent(
                base64.b64encode(requests.get(attachment_url).content).decode()
            ),
            FileName(os.path.basename(attachment_url)),
            FileType("application/pdf"),
            Disposition("attachment"),
        )
        message.attachment = attachment
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.headers)
    except Exception as e:
        print(str(e))

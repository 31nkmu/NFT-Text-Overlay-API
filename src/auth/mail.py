import aiosmtplib
from email.message import EmailMessage

from src.config import SMTP_SERVER, SMTP_PORT, \
    SMTP_USERNAME, SMTP_PASSWORD, SMTP_SENDER


async def send_email(to_email: str, subject: str, content: str):
    message = EmailMessage()
    message.set_content(content)
    message['Subject'] = subject
    message['From'] = SMTP_SENDER
    message['To'] = to_email

    async with aiosmtplib.SMTP(SMTP_SERVER,
                               port=SMTP_PORT, use_tls=True) as server:
        await server.login(SMTP_USERNAME, SMTP_PASSWORD)
        await server.send_message(message)

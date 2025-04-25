import aiosmtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..interfaces import CtCommunicationsContainer


def send_email_factory(container: CtCommunicationsContainer):
    async def func(
        receiver: str,
        subject: str,
        body: str,
        sender: str,
    ) -> str | None:
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = subject
        message.attach(MIMEText(body, "html", "utf-8"))

        await aiosmtplib.send(
            message,
            hostname=container.settings.communications.smtp_host,
            port=int(container.settings.communications.smtp_port),
            username=container.settings.communications.smtp_username,
            password=container.settings.communications.smtp_password,
        )

        return "none"
    return func

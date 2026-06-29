import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.settings import settings

logger = logging.getLogger(__name__)

OTP_EMAIL_SUBJECT = "Your OTP Code"

OTP_EMAIL_BODY_TEMPLATE = """\
Hi,

Your one-time password is:

    {code}

This code expires in {expiry_minutes} minutes. Do not share it with anyone.

— App
"""


async def send_otp_email(to_email: str, code: str, expiry_minutes: int = 5) -> None:
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD, settings.SMTP_FROM_EMAIL]):
        logger.warning("SMTP is not configured — skipping OTP email to %s", to_email)
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = OTP_EMAIL_SUBJECT
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    msg["To"] = to_email

    body = OTP_EMAIL_BODY_TEMPLATE.format(code=code, expiry_minutes=expiry_minutes)
    msg.attach(MIMEText(body, "plain"))

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )
    logger.info("OTP email sent to %s", to_email)

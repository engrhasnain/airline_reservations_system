import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_email(to: str, subject: str, body: str):
    """Send a simple plain-text email using configured SMTP settings."""
    host = getattr(settings, 'SMTP_HOST', None)
    port = getattr(settings, 'SMTP_PORT', None)
    user = getattr(settings, 'SMTP_USER', None)
    password = getattr(settings, 'SMTP_PASSWORD', None)
    use_ssl = getattr(settings, 'SMTP_USE_SSL', True)
    sender = getattr(settings, 'EMAIL_FROM', user)

    if not host or not port:
        # SMTP not configured - in demo mode, just log and return
        print(f"SMTP not configured; skipping email to {to}: {subject}\n{body}")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.set_content(body)

    try:
        if use_ssl:
            with smtplib.SMTP_SSL(host, int(port)) as server:
                if user and password:
                    server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, int(port)) as server:
                server.starttls()
                if user and password:
                    server.login(user, password)
                server.send_message(msg)
    except Exception as e:
        # Log error but do not raise to avoid disrupting flow
        print(f"Failed to send email to {to}: {e}")
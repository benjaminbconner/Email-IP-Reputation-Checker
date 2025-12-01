import smtplib
import os
from email.mime.text import MIMEText

OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")

def send_alert(ip, score, reports):
    recipient = OUTLOOK_EMAIL  # send to yourself for now
    msg = MIMEText(
        f"Suspicious IP detected:\n\n"
        f"IP: {ip}\n"
        f"Abuse Confidence Score: {score}\n"
        f"Reports: {reports}"
    )
    msg["Subject"] = "🚨 AbuseIPDB Alert"
    msg["From"] = OUTLOOK_EMAIL
    msg["To"] = recipient

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False

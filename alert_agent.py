import os
import smtplib
from email.mime.text import MIMEText

EMAIL_USER = "rgechef@gmail.com"
EMAIL_PASS = os.environ.get("EMAIL_PASSWORD")  # Set this in your terminal, do not hard-code
EMAIL_TO = "rgechef@gmail.com"

def send_alert(message):
    subject = "3DShapeSnap.AI Dev Agent Alert"
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        print("[OK] Alert email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

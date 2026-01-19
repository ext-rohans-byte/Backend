import smtplib
from email.message import EmailMessage
import getpass

EMAIL = input("Enter Gmail address: ")
PASSWORD = getpass.getpass("Enter App Password (hidden): ")

msg = EmailMessage()
msg["Subject"] = "Direct SMTP Test"
msg["From"] = EMAIL
msg["To"] = EMAIL
msg.set_content("If you see this email, SMTP auth works.")

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()
    print("✅ EMAIL SENT SUCCESSFULLY")
except Exception as e:
    print("❌ FAILED:", e)

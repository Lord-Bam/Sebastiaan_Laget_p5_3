import smtplib
from email.mime.text import MIMEText
import configparser
import imaplib
import email
from email.header import decode_header
from pydantic import BaseModel


class EmailMessage(BaseModel):
    subject: str
    body: str


class Mail:
    def __init__(self, config: configparser.ConfigParser):
        self.sender: str = config["MAIL"]["sender"]
        self.password: str = config["MAIL"]["password"]
        self.smtp: str = config["MAIL"]["smtp"]
        self.port: str = config["MAIL"]["port"]
        self.imap: str = config["MAIL"]["imap"]

    def send_email(self, subject: str, body: str, recipient: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = ", ".join([recipient])
        with smtplib.SMTP_SSL(self.smtp, int(self.port)) as smtp_server:
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, [recipient], msg.as_string())
        print("Message sent!")

    def get_last_mail(self):
        try:
            mail = imaplib.IMAP4_SSL(self.imap)
            mail.login(self.sender, self.password)
            mail.select("inbox")

            status, messages = mail.search(None, "ALL")
            mail_ids = messages[0].split()

            if not mail_ids:
                print("No emails found!")
                return

            latest_email_id = mail_ids[-1]
            status, data = mail.fetch(latest_email_id, "(RFC822)")

            for response_part in data:
                if isinstance(response_part, tuple):
                    # Parse the raw email
                    msg = email.message_from_bytes(response_part[1])

                    # Decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # If it's a bytes object, decode to a string
                        subject = subject.decode(encoding or "utf-8")

                    # Decode the sender's email address
                    from_ = msg.get("From")

                    print(f"Subject: {subject}")
                    print(f"From: {from_}")

                    # If the email isn't multipart
                    try:
                        body = msg.get_payload(decode=True).decode()
                        print(f"Body: {body}")
                    except Exception as e:
                        print(f"Error decoding email body: {e}")

                    return EmailMessage(body=body.strip(), subject=subject.strip())

            # Close the connection
            mail.logout()

        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_all_mail(self):
        try:
            mail = imaplib.IMAP4_SSL(self.imap)
            mail.login(self.sender, self.password)
            mail.select("inbox")

            status, messages = mail.search(None, "ALL")
            mail_ids = messages[0].split()

            if not mail_ids:
                print("No emails found!")
                return

            for mail_id in mail_ids:
                mail.store(mail_id, "+FLAGS", "\\Deleted")

            # Permanently delete the marked emails
            mail.expunge()
            mail.logout()
        except Exception as e:
            print(f"An error occurred: {e}")
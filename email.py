import ssl
import smtplib
from pathlib import Path
from email import encoders
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import os
import re

class Email():

    REPORT = 'REPORT'
    REPORT_EMAIL = 'EMAIL'

    EMAIL_BODY = """
            <meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
            <div style="color:#4c4f52;
                font-family:sans-serif;
                font-size:13px;
                font-style:normal;
                letter-spacing:normal;">
                <p>Dear Concern,</p>
                <p> 
                    <b> <i> Greetings from ADC Reports! </i> </b>
                </p>
                <p> Please find {report_name} in the attachment. </p>
                <p style="color: rgb(203, 87, 110);">
                    <b>
                        N.B: Do not reply to this email. This is an automated email from ADC Reports Application. For any issues regarding the data we
                        suggest you to contact the concerned team.
                    </b>
                </p>
            </div>
            """


    def __init__(self, body, to=None, cc=None, subject=None, report=None, user=None, type=REPORT, attachment_path=None, mail_type=0) -> None:
        self.type=type
        self.body=body
        self.report=report
        self.user=user
        self.mail_type = mail_type
        self.attachment_path=attachment_path
        self.smtp_host = settings.MAIL_HOST if self.mail_type == 0 else settings.OUTBOUND_MAIL_HOST
        self.smtp_port = settings.MAIL_PORT if self.mail_type == 0 else settings.OUTBOUND_MAIL_PORT
        self.smtp_user = settings.MAIL_HOST_USER
        self.smtp_pass = settings.MAIL_HOST_PASS
        self.ssl_cert_path = settings.MAIL_SSL_CERT if self.mail_type == 0 else settings.OUTBOUND_MAIL_SSL_CERT
        self.ssl_key_path = settings.MAIL_SSL_KEY if self.mail_type == 0 else settings.OUTBOUND_MAIL_SSL_KEY
        self.to = to
        self.subject = subject
        self.cc = cc
        


    def send_mail(self):
        if self.type == Email.REPORT:
            # print("send_mail_fn")
            return self.__send_custom_mail()


    def __send_email(ssl_cert, # type: ignore
                     ssl_key,
                     smtp_host,
                     smtp_port,
                     smtp_user,
                     smtp_pass,
                     rcpt,
                     multipart):
        smtp = smtplib.SMTP(smtp_host, smtp_port)
        print(ssl_cert)
        print(ssl_key)
        if ssl_cert and ssl_key:
            context = ssl._create_unverified_context()
            context.set_ciphers('DEFAULT')
            context.load_cert_chain(ssl_cert, ssl_key) # type: ignore
            smtp.starttls(context=context)
            # smtp.login(smtp_user, smtp_pass, initial_response_ok=True)
        
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        for email in rcpt:
            if not email_regex.match(email):
                print(f"Invalid email address: {email}")
            else:
                print("valid email address")

        print('Sending email.....')
        
        try:
            smtp.sendmail(smtp_user, rcpt, multipart.as_string())
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            smtp.quit()


    def prepare_email(to, from_mail, subject, body, attachment_path=None, cc=None): # type: ignore
        multipart = MIMEMultipart('alternative')
        multipart['From'] = from_mail
        multipart['To'] = to # type: ignore
        multipart['Subject'] = subject
        # print(attachment_path)

        rcpt = to.split(",") # type: ignore
        print(rcpt)
        if cc:
            multipart['Cc'] = cc
            rcpt += cc.split(",")
            print(rcpt)

        multipart.attach(MIMEText(body, 'html'))

        if attachment_path:
            part = MIMEBase('application', "octet-stream")
            
            with open(attachment_path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}'.format(Path(attachment_path).name))
            multipart.attach(part)
            print("pass")

        return multipart, rcpt


    def __send_custom_mail(self):
        try:
            print("File is readable: ", os.access(self.attachment_path, os.R_OK)) # type: ignore
            multipart, rcpt = Email.prepare_email(
                to=self.to, # type: ignore
                from_mail=self.smtp_user,
                subject=self.subject,
                body=self.body,
                cc=self.cc,
                attachment_path=self.attachment_path
            )

            Email.__send_email(
                ssl_cert=self.ssl_cert_path,
                ssl_key=self.ssl_key_path,
                smtp_host=self.smtp_host,
                smtp_port=self.smtp_port,
                smtp_user=self.smtp_user,
                smtp_pass=self.smtp_pass,
                rcpt=rcpt,
                multipart=multipart
            )
            print("pass")
            return True
        except Exception as E:
            print(E)
            return False

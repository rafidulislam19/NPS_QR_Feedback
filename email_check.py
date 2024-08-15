from helpers.email import Email
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'NPS Feedback Report'

    def handle(self, *args, **kwargs):
        attachment_path='/var/www/qrinsight/local/report/customer_feedback_Test_ATM_2024-06-26.xlsx'
        if not os.path.exists(attachment_path):
            print(f"File not found: {attachment_path}")
        else:
            print(f"File found: {attachment_path}")
        email = Email(body=Email.EMAIL_BODY.format(report_name="REPORT"),
            subject='[UAT] NPS Feedback Report',
            type=Email.REPORT,
            to='mszaman.shabit@bracbank.com',
            cc='mszaman.shabit@bracbank.com',
            attachment_path='/var/www/qrinsight/local/report/customer_feedback_Test_ATM_2024-06-26.xlsx')
        
        email_sent = email.send_mail()
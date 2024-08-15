import json
import pandas as pd
from django.core.management.base import BaseCommand
from feedbacks.models.customer_responses import CustomerResponses
from feedbacks.models.sources import Source
from django.conf import settings
import os
from datetime import datetime, timedelta
import pytz
from helpers.email import Email
from log.models.job_logs import (JobLog, 
                                 JOBLOG_BODY, 
                                 ERROR, 
                                 ERROR_MSG, 
                                 COMPLETED, 
                                 MAIL_SENT, 
                                 FILE_UPLOADED,
                                 EXECUTED_QUERY,
                                 CREATED_EXCEL)
from log.models.task_logs import TaskLog

class Command(BaseCommand):
    help = 'Generate Customer Feedback Report'

    def handle(self, *args, **kwargs):
        REPORT_FOLDER = 'report'
        sources = Source.objects.all()
        # print(sources)
        # Create the report directory if it does not exist
        os.makedirs(os.path.join(settings.LOCAL_FOLDER, REPORT_FOLDER), exist_ok=True)
        atm_responses = []
        branch_responses = []
        REPORT_PATH_ATM = os.path.join(settings.LOCAL_FOLDER, REPORT_FOLDER, f'customer_feedback_ATM_{datetime.now().strftime("%Y-%m-%d")}.xlsx')
        REPORT_NAME_ATM=f'customer_feedback_ATM_{datetime.now().strftime("%Y-%m-%d")}.xlsx'


        REPORT_PATH_BRANCH = os.path.join(settings.LOCAL_FOLDER, REPORT_FOLDER, f'customer_feedback_BRANCH_{datetime.now().strftime("%Y-%m-%d")}.xlsx')
        REPORT_NAME_BRANCH=f'customer_feedback_BRANCH_{datetime.now().strftime("%Y-%m-%d")}.xlsx'

        try:
            for source in sources:
                print(source)
                responses = CustomerResponses.objects.filter(
                    source=source,
                    created__gte=datetime.now(tz=pytz.timezone('Asia/Dhaka')) - timedelta(days=1)
                )

                log = None

                print(responses)

                if responses.exists():
                    log = TaskLog(
                        name=f'generate_feedback_report',
                        task_id='001',
                        jobs=responses.count()
                    )
                    log.save()
                    
                    # try:
                    email_sent = uploaded = False 
                    joblog = JobLog(
                        name=f'generate_feedback_report',
                        task=log,
                    )
                    joblog.save()
                    joblog_description = JOBLOG_BODY.copy()
                    for response in responses:
                        # print(response.source.source_type) # type: ignore
                        if response.source.source_type == 'ATM': # type: ignore
                            data = response.response
                            if 'cash_note' in data.keys():
                                if data['cash_note'] == 'True':
                                    data['cash_note'] = 'Satisfactory'
                                elif data['cash_note'] == 'False':
                                    data['cash_note'] = 'Unsatisfactory'
                            if 'guard_present' in data.keys():
                                if data['guard_present'] == 'True':
                                    data['guard_present'] = 'Yes'
                                elif data['guard_present'] == 'False':
                                    data['guard_present'] = 'No'

                            data['response_sent_time'] = response.created
                            print(data['response_sent_time'])
                            data['atm_id'] = source.source_id              #changes for report column
                            data['atm_name'] = source.source_name
                            data['atm_location'] = source.source_address
                            atm_responses.append(data)

                        if response.source.source_type == 'BRANCH': # type: ignore
                            data = response.response
                            if 'astha_app_service' in data.keys():
                                if data['astha_app_service'] == 'True':
                                    data['astha_app_service'] = 'Yes'
                                elif data['astha_app_service'] == 'False':
                                    data['astha_app_service'] = 'No'
                            data['response_sent_time'] = response.created
                            data['branch_id'] = source.source_id               #changes for report column
                            data['branch_name'] = source.source_name
                            data['branch_location'] = source.source_address                        
                            branch_responses.append(data)

            print(f"atm_responses: {atm_responses}")
            print(f"branch_responses: {branch_responses}")
                    
            df_atm = pd.DataFrame(atm_responses)
            df_branch = pd.DataFrame(branch_responses)
            
            if not df_atm.empty:
                df_atm['response_sent_time'] = df_atm['response_sent_time'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
                df_atm.sort_values('atm_id').reset_index(drop=True).to_excel(REPORT_PATH_ATM, index=True, index_label='SL')    #changes for report sort by atm id
                print(df_atm)
                print(f"Generated ATM report: {REPORT_PATH_ATM}")
                email_ATM = Email(body=Email.EMAIL_BODY.format(report_name=REPORT_NAME_ATM),
                    subject='[UAT] NPS Feedback Report',
                    type=Email.REPORT,
                    #to='mszaman.shabit@bracbank.com',
                    #cc='mszaman.shabit@bracbank.com',
                    to='ayesha.siddika21932@bracbank.com,rashik.raihan@bracbank.com',
                    cc='mszaman.shabit@bracbank.com,mostafijur.rahman27389@bracbank.com,zakirhossain.haider@bracbank.com',
                    attachment_path=REPORT_PATH_ATM)
                email_sent = email_ATM.send_mail()

            if not df_branch.empty:
                df_branch['response_sent_time'] = df_branch['response_sent_time'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
                df_branch.sort_values('branch_id').reset_index(drop=True).to_excel(REPORT_PATH_BRANCH, index=True, index_label='SL')  #changes for report sort by branch id
                print(df_atm)
                print(f"Generated ATM report: {REPORT_PATH_ATM}")
                email_BRANCH = Email(body=Email.EMAIL_BODY.format(report_name=REPORT_NAME_BRANCH),
                    subject='[UAT] NPS Feedback Report',
                    type=Email.REPORT,
                    #to='mszaman.shabit@bracbank.com',
                    #cc='mszaman.shabit@bracbank.com',
                    to='ayesha.siddika21932@bracbank.com,rashik.raihan@bracbank.com',
                    cc='mszaman.shabit@bracbank.com,mostafijur.rahman27389@bracbank.com,zakirhossain.haider@bracbank.com',
                    attachment_path=REPORT_PATH_BRANCH)
                email_sent = email_BRANCH.send_mail()
           
            # email = Email(body=Email.EMAIL_BODY.format(report_name=REPORT_NAME),
            #                         subject='[UAT] NPS Feedback Report',
            #                         type=Email.REPORT,
            #                         to='mszaman.shabit@bracbank.com',
            #                         cc='mszaman.shabit@bracbank.com',
            #                         attachment_path=REPORT_PATH)
            # attachment_path=REPORT_PATH
            # print(attachment_path)
            # if not os.path.exists(attachment_path):
            #     print(f"File not found: {attachment_path}")
            # else:
            #     print(f"File found: {attachment_path}")

        except Exception as E:
            joblog_description[ERROR] = True
            joblog_description[ERROR_MSG] = str(E)
            joblog.description = json.dumps(joblog_description)
            joblog.save()
            raise E
        
        finally:
            if joblog_description[ERROR] == True:
                joblog_description[COMPLETED] = False
            else:
                joblog_description[COMPLETED] = True


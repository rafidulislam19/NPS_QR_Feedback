import json
from django.db import models
from django.contrib import admin
from log.models.task_logs import TaskLog
from unfold.admin import ModelAdmin


ERROR = 'error'
ERROR_MSG = 'error_message'
COMPLETED = 'completed'
MAIL_SENT = 'email_sent'
FILE_UPLOADED = 'file_uploaded'
EXECUTED_QUERY = 'executed_query'
CREATED_EXCEL = 'created_excel'

JOBLOG_BODY = {
    ERROR: False,
    ERROR_MSG: "",
    COMPLETED: True,
    MAIL_SENT: False,
    FILE_UPLOADED: False,
    EXECUTED_QUERY: False,
    CREATED_EXCEL: False,
}



class JobLog(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    task = models.ForeignKey(TaskLog, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, default=json.dumps(JOBLOG_BODY))
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Job ID: {self.pk}"

    def time(self):
        return self.finished - self.started
    
    @property
    def show_description(self):
        return self.description


class JobLogAdmin(ModelAdmin):
    list_display = ['name', 'task', 'show_description', 'started', 'finished', 'time']
    search_fields = ['name', 'description']
    list_filter = ('task', 'name')
    ordering = ['-finished']

    def has_change_permission(self, request, obj=None) -> bool:
        return False
    
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user.is_superuser:
            return True
        else:
            return False
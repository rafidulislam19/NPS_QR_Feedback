from django.contrib import admin
from .models.activity_logs import LogEntry, LogEntryAdmin
from .models.user_activity_logs import UserActivityLogs, UserActivityLogsAdmin
from .models.task_logs import TaskLog, TaskLogAdmin 
from .models.job_logs import JobLog, JobLogAdmin
# Register your models here.


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(UserActivityLogs, UserActivityLogsAdmin)
admin.site.register(TaskLog, TaskLogAdmin)
admin.site.register(JobLog, JobLogAdmin)


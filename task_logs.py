from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import NonrelatedTabularInline

class TaskLog(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, default=None)
    task_id = models.CharField(max_length=10,blank=True, null=True, default=None)
    jobs = models.IntegerField(blank=True, null=True)
    error = models.BooleanField(default=False, verbose_name='Error Faced')
    completed = models.BooleanField(default=False, verbose_name='Completed Task')
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)
    
    def time(self):
        return self.finished - self.started
    
    def __str__(self) -> str:
        return f"{self.task_id}-{self.pk}" if self.task_id else str(self.pk)    

class JobLogsInLine(NonrelatedTabularInline):
    from log.models.job_logs import JobLog
    verbose_name = "Job"
    verbose_name_plural = "Jobs"
    model = JobLog
    # 
    
 
class TaskLogAdmin(ModelAdmin):
    list_display = ['name', 'task_id', 'jobs', 'error', 'completed', 'started', 'finished', 'time']
    search_fields = ['name', 'task_id']
    list_filter = ('name', )
    ordering = ['-finished']
    inlines = [JobLogsInLine, ]
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False
    
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user.is_superuser:
            return True
        else:
            return False

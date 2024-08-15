from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin

class UserActivityLogs(models.Model):
    user = models.CharField(max_length=30, blank=True, null=True, default=None)
    ip_address = models.CharField(max_length=20, blank=False, null=False, verbose_name='User IP')
    activity = models.CharField(max_length=512, blank=False, null=False)
    time = models.DateTimeField(
        auto_now_add=True, editable=False, blank=True, null=True)

class UserActivityLogsAdmin(ModelAdmin):
    ordering = ('-time', )
    date_hierarchy = 'time'
    search_fields = ['user', 'ip_address']
    list_display=['id', 'user', 'ip_address', 'activity', 'time']
    list_filter = ('activity', 'time')
    
    def has_delete_permission(self, request, obj=None):
        return False
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

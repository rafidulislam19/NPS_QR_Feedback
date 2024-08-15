from uuid import uuid4
from django.db import models
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from .sources import Source
from unfold.decorators import display
from django.contrib import admin
# from feedbacks.encoders import PrettyJSONEncoder


class CustomerResponses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    response = models.JSONField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class CustomCustomerResponseAdmin(ModelAdmin):
    list_display = ['id', 'show_source_name', 'response', 'created']
    ordering = ("-created", )

    @admin.display(
        description="Source", 
        ordering='source__source_name'
    )
    def show_source_name(self, obj):
        return obj.source.source_name
    
#    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
#        return False
    
#    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
#        return False
    

# SERVICE_CHOICES = [
#         ('Cash Deposit / Withdrawl', 'নগদ টাকা তোলা / জমা দেওয়া'),
#         ('General Service', 'জেনারেল সার্ভিস'),
#         ('Information', 'তথ্য সংগ্রহ'),
#         ('Foreign Currency', 'বৈদেশিক মুদ্রা সম্পর্কিত সার্ভিস'),
#     ]

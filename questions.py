# from uuid import uuid4
# from django import forms
# from django.db import models
# from datetime import datetime
# from django.utils import timezone
# from django.forms import Form, ValidationError
# from django.http import HttpRequest
# from django.contrib import admin
# from unfold.admin import ModelAdmin
# from unfold.decorators import display
# from unfold.decorators import action
# from .sources import Source

# class QuestionType(models.TextChoices):
#     SELECT = "SELECT", "Yes / NO Mark"
#     TEXT = "TEXT", "Text Field"

# class Question(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     question = models.CharField(max_length=255, blank=False, null=False)
#     type = models.CharField(choices=QuestionType, max_length=50, blank=False, null=False) # type: ignore
#     source = models.ForeignKey(Source, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
# class QuestionType(models.TextChoices):
#     SELECT = "SELECT", "Yes / NO Mark"
#     TEXT = "TEXT", "Text Field"

# class QuestionAdmin(ModelAdmin):
#     list_display = ['id', 'display_question_type', 'show_source_name', 'created']

#     @display(
#         description="Question Type",
#         label={
#             QuestionType.SELECT: "warning",
#             QuestionType.TEXT: "success",
#         },
#     )
#     def display_question_type(self, instance: Question):
#         if instance.type:
#             return instance.type

#         return None
    
#     @display(
#         description="Source", label=True
#     )
#     def show_source_name(self, obj):
#         return obj.source.source_name
from uuid import uuid4
from django import forms
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.forms import Form, ValidationError
from django.http import HttpRequest
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.decorators import action
from .sources import Source

class QuestionType(models.TextChoices):
    SELECT = "SELECT", "Yes / NO Mark"
    TEXT = "TEXT", "Text Field"

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    question = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(choices=QuestionType.choices, max_length=50, blank=False, null=False)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class QuestionAdmin(ModelAdmin):
    list_display = ['id', 'display_question_type', 'show_source_name', 'created']

    @display(
        description="Question Type",
        label={
            QuestionType.SELECT: "warning",
            QuestionType.TEXT: "success",
        },
    )
    def display_question_type(self, instance: Question):
        if instance.type:
            return instance.type

        return None
    
    @display(
        description="Source", label=True
    )
    def show_source_name(self, obj):
        return obj.source.source_name


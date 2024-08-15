from django.contrib import admin
from django.urls import path, include
from .views.feedback import feedback_request_handler

urlpatterns = [path('response/<uuid:uuid>', feedback_request_handler, name='customer_feedback')]
from django.urls import path
from .views import CustomPasswordChangeView

urlpatterns = [
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
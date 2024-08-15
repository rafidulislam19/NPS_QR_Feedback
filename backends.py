from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        if not user.is_active:
            return False
        if not user.password_last_changed:
            return False
        if timezone.now() - user.password_last_changed > timedelta(days=90):
            return False
        return True
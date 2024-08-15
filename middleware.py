from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from datetime import timedelta

class PasswordChangeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.password_last_changed or \
               (timezone.now() - request.user.password_last_changed > timedelta(days=90)):
                # print(request.user.password_last_changed)
                if request.path != reverse('password_change'):
                    return redirect('password_change')
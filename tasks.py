from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

def send_password_expiry_notifications():
    users = User.objects.filter(password_last_changed__lte=timezone.now() - timedelta(days=90))
    for user in users:
        send_mail(
            'Password Expiry Notification',
            'Your password has expired. Please change your password.',
            'admin@example.com',
            [user.email],
            fail_silently=False,
        )
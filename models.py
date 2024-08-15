from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import date, timedelta

class User(AbstractUser):
    
    class Meta:
        verbose_name = 'Access Management'
        verbose_name_plural = 'Access Management'
    
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    pin = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique = False)
    phone_no = models.CharField(max_length = 20)
    password_last_changed = models.DateTimeField(null=True, blank=True, default=None)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    
    def __str__(self):
        return "{}".format(self.username)
    
    def save(self, *args, **kwargs):
        # if self.pk:
        #     self.password_last_changed = timezone.now()
        super().save(*args, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    
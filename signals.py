from django.dispatch import receiver
from helpers.ip import get_client_ip
from log.models.user_activity_logs import UserActivityLogs
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):    
    ip = get_client_ip(request)
    user_log = UserActivityLogs(user=user.username, 
                                ip_address=ip, 
                                activity='LOG-IN')
    print("user_logged_in_callback: ", user_log)
    user_log.save()
    

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs): 
    ip = get_client_ip(request)
    user_log = UserActivityLogs(user=user.username if user else '', 
                                ip_address=ip,
                                activity='LOG-OUT')
    print("user_logged_out_callback: ", user_log)
    user_log.save()
 

@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    ip = get_client_ip(request)
    user_log = UserActivityLogs(user=credentials['username'], 
                                ip_address=ip, 
                                activity='FAILED') 
    print("user_login_failed_callback: ", user_log)
    user_log.save()
from django.http import HttpResponseForbidden
from django.shortcuts import render
from feedbacks.views.feedback import http_403_custom
import re

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if re.match(r'^/admin_access_VK!aAq/login/\?next=/admin_access_VK%21aAq/.+', request.get_full_path()):
            # Check if the user is authenticated and has the required permission
            if not request.user.is_authenticated:
                return HttpResponseForbidden(http_403_custom(request))
        return self.get_response(request)

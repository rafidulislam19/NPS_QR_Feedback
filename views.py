from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import render, redirect


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.password_last_changed = timezone.now()
        self.request.user.save()
        # print(self.request.user.save())
        logout(self.request)
        return redirect('/admin_access_VK!aAq')

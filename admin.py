
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from .models import User
from django.contrib import admin
from unfold.admin import ModelAdmin
# from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):  
    pass

class UserAdmin(BaseUserAdmin, ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', )}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'pin', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined', 'password_last_changed')}),
            (('user_info'), {'fields': ['phone_no']}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'reset_password']
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username', )

    def reset_password(self, request):
        reset_url = reverse('admin:auth_user_password_change', args=[request.pk])
        return format_html('<a class="button" href="{}">Reset Password</a>', reset_url)
    
    reset_password.short_description = 'Reset Password'
    reset_password.allow_tags = True
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/reset_password/',
                self.admin_site.admin_view(self.reset_password),
                name='auth_user_password_reset',
            ),
        ]
        return custom_urls + urls
    

admin.site.register(User, UserAdmin)
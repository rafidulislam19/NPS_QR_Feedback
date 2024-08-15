"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin_access_VK!aAq/', admin.site.urls),
    path('feedbacks/', include('feedbacks.urls')),
    path('access_management/', include('access_management.urls')),
    path('access_management/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


handler404 = 'feedbacks.views.feedback.http_404_custom'
handler500 = 'feedbacks.views.feedback.http_500_custom'

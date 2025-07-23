"""
URL configuration for automatic_feeder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user/', create_user),
    path('login/', login_user),
    path('forgot_password/', forgot_password),
    path('reset_password/', reset_password),
    path('reset-password/', reset_password_page),
    path('auto_feeder_post/', auto_feeder_data_post),
    path('auto_feeder_get/', get_auto_feeder_data),
    path('manual_feeder_post/', manual_feeder_data_post),
    path('manual_feeder_get/', get_manual_feeder_data),
    path('get_alert/', latest_alerts),
    
]

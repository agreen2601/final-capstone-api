"""eventtranspotracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from trackerapp.models import *
from trackerapp.views import *
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'entries', Entries, 'entry')
router.register(r'events', Events, 'event')
router.register(r'locations', Locations, 'location')
router.register(r'routes', Routes, 'route')
router.register(r'users', Users, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register/', register_user),
    path('login/', login_user),
    path('get_user/', get_user),
    path('api-token-auth/', obtain_auth_token),
]

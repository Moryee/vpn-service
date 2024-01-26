from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda req: redirect('/sites/')),
    path('admin/', admin.site.urls),
    path('auth/', include('auth_templates.urls')),
    path('profile/', include('user_profile.urls')),
    path('sites/', include('sites.urls')),
    path('proxy/', include('proxy.urls')),
]

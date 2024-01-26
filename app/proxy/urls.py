from django.urls import path
from .views import ProxyIndexView

app_name = 'proxy'
urlpatterns = [
    path('', ProxyIndexView.as_view(), name='index'),
]

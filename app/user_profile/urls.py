from django.urls import path
# from .views import OrderList, OrderDelete
from .views import Index

app_name = 'user_profile'
urlpatterns = [
    path('', Index.as_view(), name='index'),
]

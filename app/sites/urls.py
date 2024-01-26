from django.urls import path
from .views import SiteListView, SiteDetailView, SiteCreateView, SiteUpdateView, SiteDeleteView


app_name = 'sites'
urlpatterns = [
    path('', SiteListView.as_view(), name='site-list'),
    path('<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
    path('create/', SiteCreateView.as_view(), name='site-create'),
    path('<int:pk>/update/', SiteUpdateView.as_view(), name='site-update'),
    path('<int:pk>/delete/', SiteDeleteView.as_view(), name='site-delete'),
]

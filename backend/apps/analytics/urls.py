from django.urls import path
from .views import admin_analytics, seller_analytics

urlpatterns = [
    path('admin/', admin_analytics, name='admin-analytics'),
    path('seller/', seller_analytics, name='seller-analytics'),
]

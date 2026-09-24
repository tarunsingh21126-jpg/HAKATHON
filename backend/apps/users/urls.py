from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterView, profile_view, list_users, list_sellers

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth-login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('profile/', profile_view, name='auth-profile'),
    path('users/', list_users, name='admin-users'),
    path('sellers/', list_sellers, name='admin-sellers'),
]

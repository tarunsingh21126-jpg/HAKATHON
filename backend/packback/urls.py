"""
PackBack Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/containers/', include('apps.containers.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/returns/', include('apps.returns.urls')),
    path('api/deposits/', include('apps.deposits.urls')),
    path('api/rewards/', include('apps.rewards.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

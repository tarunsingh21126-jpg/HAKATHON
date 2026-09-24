from django.urls import path
from .views import ContainerListCreateView, ContainerDetailView, container_by_code

urlpatterns = [
    path('', ContainerListCreateView.as_view(), name='container-list'),
    path('<int:pk>/', ContainerDetailView.as_view(), name='container-detail'),
    path('qr/<str:code>/', container_by_code, name='container-by-code'),
]

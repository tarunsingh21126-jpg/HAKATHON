from django.urls import path
from .views import ReturnListCreateView, ReturnDetailView, DropOffLocationListView

urlpatterns = [
    path('', ReturnListCreateView.as_view(), name='return-list'),
    path('<int:pk>/', ReturnDetailView.as_view(), name='return-detail'),
    path('dropoff-locations/', DropOffLocationListView.as_view(), name='dropoff-list'),
]

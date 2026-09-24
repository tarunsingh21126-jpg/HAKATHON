from django.urls import path
from .views import DepositListView

urlpatterns = [
    path('', DepositListView.as_view(), name='deposit-list'),
]

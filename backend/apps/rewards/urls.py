from django.urls import path
from .views import RewardHistoryView, reward_balance

urlpatterns = [
    path('', reward_balance, name='reward-balance'),
    path('history/', RewardHistoryView.as_view(), name='reward-history'),
]

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from .models import Reward
from .serializers import RewardSerializer


class RewardHistoryView(generics.ListAPIView):
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reward.objects.filter(customer=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reward_balance(request):
    total = Reward.objects.filter(customer=request.user).aggregate(
        total=Sum('points')
    )['total'] or 0
    earned = Reward.objects.filter(customer=request.user, transaction_type='earned').aggregate(
        total=Sum('points')
    )['total'] or 0
    redeemed = Reward.objects.filter(customer=request.user, transaction_type='redeemed').aggregate(
        total=Sum('points')
    )['total'] or 0
    return Response({
        'balance': total,
        'total_earned': earned,
        'total_redeemed': abs(redeemed),
        'coupons': [
            {'points': 100, 'value': '₹20 coupon', 'id': 'c100'},
            {'points': 250, 'value': '₹50 coupon', 'id': 'c250'},
            {'points': 500, 'value': 'Partner reward', 'id': 'c500'},
        ]
    })

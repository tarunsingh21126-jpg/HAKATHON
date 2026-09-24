from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Deposit
from .serializers import DepositSerializer


class DepositListView(generics.ListAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Deposit.objects.all()
        return Deposit.objects.filter(customer=user)

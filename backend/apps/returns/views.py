from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Return, DropOffLocation
from .serializers import ReturnSerializer, DropOffLocationSerializer


class ReturnListCreateView(generics.ListCreateAPIView):
    serializer_class = ReturnSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Return.objects.all()
        elif user.role == 'seller' and hasattr(user, 'seller_profile'):
            return Return.objects.filter(container__seller=user.seller_profile)
        return Return.objects.filter(customer=user)

    def get_serializer_context(self):
        return {'request': self.request}


class ReturnDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ReturnSerializer
    permission_classes = [IsAuthenticated]
    queryset = Return.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class DropOffLocationListView(generics.ListAPIView):
    serializer_class = DropOffLocationSerializer
    permission_classes = [AllowAny]
    queryset = DropOffLocation.objects.filter(is_active=True)

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['delivery_status', 'seller', 'customer']
    search_fields = ['order_number']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all()
        elif user.role == 'seller' and hasattr(user, 'seller_profile'):
            return Order.objects.filter(seller=user.seller_profile)
        else:
            return Order.objects.filter(customer=user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

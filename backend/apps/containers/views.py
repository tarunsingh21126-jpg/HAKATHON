from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Container
from .serializers import ContainerSerializer, ContainerCreateSerializer


class ContainerListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'condition', 'seller']
    search_fields = ['container_code']
    ordering_fields = ['created_at', 'usage_count']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ContainerCreateSerializer
        return ContainerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Container.objects.all()
        elif user.role == 'seller' and hasattr(user, 'seller_profile'):
            return Container.objects.filter(seller=user.seller_profile)
        else:
            return Container.objects.filter(current_customer=user)

    def get_serializer_context(self):
        return {'request': self.request}


class ContainerDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContainerSerializer

    def get_queryset(self):
        return Container.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
@permission_classes([AllowAny])
def container_by_code(request, code):
    """Public QR scan endpoint — look up container by code."""
    try:
        container = Container.objects.get(container_code=code)
        serializer = ContainerSerializer(container, context={'request': request})
        return Response(serializer.data)
    except Container.DoesNotExist:
        return Response({'error': 'Container not found'}, status=404)

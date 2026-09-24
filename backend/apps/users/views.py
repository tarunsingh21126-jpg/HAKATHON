from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, SellerProfile
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer, SellerProfileSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Account created successfully',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user).data)
    elif request.method == 'PATCH':
        allowed_fields = ['name', 'phone']
        data = {k: v for k, v in request.data.items() if k in allowed_fields}
        for field, value in data.items():
            setattr(request.user, field, value)
        request.user.save()
        return Response(UserSerializer(request.user).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    if request.user.role != 'admin':
        return Response({'error': 'Forbidden'}, status=403)
    users = User.objects.all()
    return Response(UserSerializer(users, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_sellers(request):
    if request.user.role != 'admin':
        return Response({'error': 'Forbidden'}, status=403)
    sellers = SellerProfile.objects.select_related('user').all()
    return Response(SellerProfileSerializer(sellers, many=True).data)

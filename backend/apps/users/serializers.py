from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, SellerProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    business_name = serializers.CharField(required=False, allow_blank=True)
    business_address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'role', 'password', 'business_name', 'business_address']

    def create(self, validated_data):
        business_name = validated_data.pop('business_name', '')
        business_address = validated_data.pop('business_address', '')
        user = User.objects.create_user(**validated_data)
        if user.role == 'seller':
            SellerProfile.objects.create(
                user=user,
                business_name=business_name or user.name,
                business_address=business_address or 'Not provided',
            )
        return user


class UserSerializer(serializers.ModelSerializer):
    seller_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'role', 'created_at', 'seller_profile']

    def get_seller_profile(self, obj):
        if obj.role == 'seller' and hasattr(obj, 'seller_profile'):
            return {
                'business_name': obj.seller_profile.business_name,
                'business_address': obj.seller_profile.business_address,
                'status': obj.seller_profile.status,
            }
        return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class SellerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SellerProfile
        fields = '__all__'

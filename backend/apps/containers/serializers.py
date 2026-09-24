from rest_framework import serializers
from .models import Container
from apps.users.serializers import SellerProfileSerializer, UserSerializer


class ContainerSerializer(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Container
        fields = [
            'id', 'container_code', 'qr_code_url', 'seller', 'seller_name',
            'current_customer', 'customer_name', 'status', 'deposit_amount',
            'usage_count', 'condition', 'notes', 'created_at', 'updated_at',
            'last_delivered_at', 'last_returned_at',
        ]
        read_only_fields = ['container_code', 'usage_count', 'created_at', 'updated_at']

    def get_seller_name(self, obj):
        return obj.seller.business_name if obj.seller else None

    def get_customer_name(self, obj):
        return obj.current_customer.name if obj.current_customer else None

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code_image and request:
            return request.build_absolute_uri(obj.qr_code_image.url)
        return None


class ContainerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['seller', 'deposit_amount', 'condition', 'notes']

    def create(self, validated_data):
        return Container.objects.create(**validated_data)

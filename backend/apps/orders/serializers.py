from rest_framework import serializers
from .models import Order
from apps.containers.models import Container
from apps.deposits.models import Deposit


class OrderSerializer(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    container_code = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'seller', 'seller_name', 'customer', 'customer_name',
            'container', 'container_code', 'customer_address', 'delivery_status',
            'notes', 'created_at', 'delivered_at',
        ]
        read_only_fields = ['order_number', 'created_at', 'seller']

    def get_seller_name(self, obj):
        return obj.seller.business_name if obj.seller else None

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None

    def get_container_code(self, obj):
        return obj.container.container_code if obj.container else None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'seller_profile'):
            validated_data['seller'] = request.user.seller_profile
        order = Order.objects.create(**validated_data)
        # Assign container to customer and create deposit
        if order.container:
            container = order.container
            container.current_customer = order.customer
            container.status = 'assigned'
            container.usage_count += 1
            container.save()
            # Create deposit record
            Deposit.objects.create(
                customer=order.customer,
                container=container,
                amount=container.deposit_amount,
                status='held',
            )
        return order

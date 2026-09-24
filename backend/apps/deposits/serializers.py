from rest_framework import serializers
from .models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    container_code = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Deposit
        fields = ['id', 'customer', 'customer_name', 'container', 'container_code',
                  'amount', 'status', 'created_at', 'refunded_at']
        read_only_fields = ['created_at']

    def get_container_code(self, obj):
        return obj.container.container_code

    def get_customer_name(self, obj):
        return obj.customer.name

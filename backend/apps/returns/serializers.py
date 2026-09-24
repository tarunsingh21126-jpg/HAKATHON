from rest_framework import serializers
from .models import Return, DropOffLocation
from apps.containers.models import Container
from apps.deposits.models import Deposit
from apps.rewards.models import Reward
from django.utils import timezone


class DropOffLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropOffLocation
        fields = '__all__'


class ReturnSerializer(serializers.ModelSerializer):
    container_code = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    dropoff_location_name = serializers.SerializerMethodField()

    class Meta:
        model = Return
        fields = [
            'id', 'container', 'container_code', 'customer', 'customer_name',
            'method', 'pickup_address', 'pickup_date', 'pickup_time',
            'dropoff_location', 'dropoff_location_name', 'status', 'notes',
            'requested_at', 'completed_at',
        ]
        read_only_fields = ['requested_at', 'completed_at', 'customer']

    def get_container_code(self, obj):
        return obj.container.container_code

    def get_customer_name(self, obj):
        return obj.customer.name

    def get_dropoff_location_name(self, obj):
        return str(obj.dropoff_location) if obj.dropoff_location else None

    def create(self, validated_data):
        request = self.context['request']
        validated_data['customer'] = request.user
        return_obj = Return.objects.create(**validated_data)
        # Update container status
        container = return_obj.container
        container.status = 'return_requested'
        container.save()
        return return_obj

    def update(self, instance, validated_data):
        old_status = instance.status
        instance = super().update(instance, validated_data)
        new_status = instance.status

        # When return is completed, process deposit + reward
        if old_status != 'completed' and new_status == 'completed':
            instance.completed_at = timezone.now()
            instance.save()

            container = instance.container
            container.status = 'available'
            container.current_customer = None
            container.last_returned_at = timezone.now()
            container.save()

            # Refund deposit
            deposit = Deposit.objects.filter(
                customer=instance.customer,
                container=container,
                status='held'
            ).first()
            if deposit:
                deposit.status = 'refunded'
                deposit.refunded_at = timezone.now()
                deposit.save()

            # Add reward points
            Reward.objects.create(
                customer=instance.customer,
                points=50,
                transaction_type='earned',
                description=f'Return of {container.container_code}',
            )

        return instance

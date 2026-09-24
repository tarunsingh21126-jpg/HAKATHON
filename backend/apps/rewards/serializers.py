from rest_framework import serializers
from .models import Reward


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'
        read_only_fields = ['created_at', 'customer']

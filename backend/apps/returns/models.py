from django.db import models
from apps.users.models import User
from apps.containers.models import Container


class DropOffLocation(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dropoff_locations'

    def __str__(self):
        return f'{self.name} — {self.city}'


class Return(models.Model):
    METHOD_CHOICES = [
        ('pickup', 'Pickup'),
        ('dropoff', 'Drop-off'),
    ]

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('pickup_assigned', 'Pickup Assigned'),
        ('collected', 'Collected'),
        ('inspection', 'Inspection'),
        ('cleaning', 'Cleaning'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='returns')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='returns')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    pickup_address = models.TextField(blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    dropoff_location = models.ForeignKey(
        DropOffLocation, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    notes = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'returns'
        ordering = ['-requested_at']

    def __str__(self):
        return f'Return {self.container.container_code} by {self.customer.name}'

from django.db import models
from apps.users.models import User, SellerProfile
from apps.containers.models import Container


class Order(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_number = models.CharField(max_length=30, unique=True)
    customer_address = models.TextField()
    delivery_status = models.CharField(max_length=15, choices=DELIVERY_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f'ORD-{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)

from django.db import models
from apps.users.models import User
from apps.containers.models import Container


class Deposit(models.Model):
    STATUS_CHOICES = [
        ('held', 'Held'),
        ('refunded', 'Refunded'),
        ('forfeited', 'Forfeited'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='held')
    created_at = models.DateTimeField(auto_now_add=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'deposits'
        ordering = ['-created_at']

    def __str__(self):
        return f'Deposit {self.amount} for {self.container.container_code}'

from django.db import models
from apps.users.models import User


class Reward(models.Model):
    TRANSACTION_CHOICES = [
        ('earned', 'Earned'),
        ('redeemed', 'Redeemed'),
        ('expired', 'Expired'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rewards'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer.name} — {self.transaction_type} {self.points} pts'

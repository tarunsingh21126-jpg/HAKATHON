import uuid
import qrcode
import os
from io import BytesIO
from django.db import models
from django.core.files import File
from apps.users.models import User, SellerProfile


class Container(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('delivered', 'Delivered'),
        ('return_requested', 'Return Requested'),
        ('pickup_assigned', 'Pickup Assigned'),
        ('collected', 'Collected'),
        ('inspection', 'Inspection'),
        ('cleaning', 'Cleaning'),
        ('damaged', 'Damaged'),
        ('retired', 'Retired'),
    ]

    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('damaged', 'Damaged'),
    ]

    container_code = models.CharField(max_length=30, unique=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    seller = models.ForeignKey(SellerProfile, on_delete=models.SET_NULL, null=True, related_name='containers')
    current_customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='active_containers'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2, default=100.00)
    usage_count = models.PositiveIntegerField(default=0)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='excellent')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_delivered_at = models.DateTimeField(null=True, blank=True)
    last_returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'containers'
        ordering = ['-created_at']

    def __str__(self):
        return self.container_code

    def generate_qr_code(self):
        """Generate QR code image for this container."""
        qr_url = f'http://localhost:5173/containers/{self.container_code}'
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        filename = f'{self.container_code}.png'
        self.qr_code_image.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.container_code:
            year = __import__('datetime').datetime.now().year
            uid = str(uuid.uuid4())[:6].upper()
            self.container_code = f'PB-{year}-{uid}'
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.qr_code_image:
            self.generate_qr_code()
            super().save(update_fields=['qr_code_image'])
